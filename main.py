import json
from contextlib import asynccontextmanager
from typing import Optional

import uvicorn
from fastapi import Depends, Query
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse

from auth.security import decode_jwt
from databases.database import init_db, get_db
from models import User, Game
from schemas import GameCreate, GameUpdate
from websocket.router import redis_manager
from websocket.router import ws_router as websocket_router
from auth.router import router as auth_router, oauth2_scheme

templates = Jinja2Templates(directory="templates")


##########################################часть з регистрацией#################################################################


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    init_db()
    print("Application started")
    yield
    await redis_manager.close()
    print("Application shutdown")


app = FastAPI(lifespan=lifespan)
app.include_router(websocket_router, tags=['websocket'])
app.include_router(auth_router,  tags=['auth'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9000", 'http://localhost:8001'],  # або конкретно ["http://localhost:9000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/cha", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("cha.html", {"request": request})


@app.get("/me")
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_jwt(token)
    email = payload.get("sub")
    if not email:
        return JSONResponse(status_code=401, content={"error": "Invalid token"})
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return JSONResponse(status_code=404, content={"error": "User not found"})
    return {"email": user.email}


############################################круд обявление для игр############################################


@app.get("/games")
def get_games(
        game: Optional[str] = Query(None),
        category: Optional[str] = Query(None),
        db: Session = Depends(get_db),
        summary="Список игр",
        description="Получить список игр, фильтруя по названию или категории",


):
    query = db.query(Game)
    if game:
        query = query.filter(Game.game == game)
    if category:
        query = query.filter(Game.category == category)

    result = query.all()
    return [{"id": g.id, "name": g.name, "author": g.author} for g in result]


@app.get("/games/id", )
def get_game_by_id(
        id: int = Query(...),
        game: str = Query(...),
        category: str = Query(...),
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db),
        summary="Получить игру по ID",
        description="Возвращает подробную информацию об игре. Требует авторизации.",

):
    decoded = decode_jwt(token)
    email = decoded.get("sub")

    if not email:
        return JSONResponse(status_code=401, content={"error": "Invalid token"})

    user = db.query(User).filter(User.email == email).first()
    if not user:
        return JSONResponse(status_code=404, content={"error": "User not found"})

    db_game = db.query(Game).filter(
        Game.id == id,
        Game.game == game,
        Game.category == category
    ).first()

    if not db_game:
        return JSONResponse(status_code=404, content={"error": "Game not found"})

    return {
        "name": db_game.name,
        "description": db_game.description,
        "author": db_game.author,
        "is_author": db_game.author == user.username,
        "created_at": db_game.created_at
    }


@app.post("/games/add")
def add_game(payload: GameCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), summary="Добавить игру",
    description="Создаёт новую игру от имени авторизованного пользователя"):
    decoded = decode_jwt(token)
    if not decoded:
        return JSONResponse(status_code=401, content={"error": "Invalid token"})
    email = decoded.get("sub")
    if not email:
        return JSONResponse(status_code=401, content={"error": "Invalid token"})
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return JSONResponse(status_code=404, content={"error": "User  not found"})
    new_game = Game(
        name=payload.name,
        description=payload.description,
        author=user.username,
        game=payload.game,
        category=payload.category
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return {"message": f"Game '{new_game.name}' created successfully"}


@app.put("/games")
def update_game(payload: GameUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db),summary="Обновить игру",
    description="Позволяет автору обновить игру по ID"):
    decoded = decode_jwt(token)
    email = decoded.get("sub")

    if not email:
        return JSONResponse(status_code=401, content={"error": "Invalid token"})

    user = db.query(User).filter(User.email == email).first()
    if not user:
        return JSONResponse(status_code=404, content={"error": "User not found"})

    db_game = db.query(Game).filter(Game.id == payload.id).first()
    if not db_game:
        return JSONResponse(status_code=404, content={"error": "Game not found"})

    if db_game.author != user.username:
        return JSONResponse(status_code=403, content={"error": "Not your game"})

    if payload.name:
        db_game.name = payload.name
    if payload.description:
        db_game.description = payload.description

    db.commit()
    db.refresh(db_game)
    return {"message": f"Game '{db_game.name}' updated successfully"}


@app.delete("/games")
def delete_game(id: int = Query(...), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), summary="Удалить игру",
    description="Удаляет игру, если текущий пользователь является автором"):
    decoded = decode_jwt(token)
    email = decoded.get("sub")

    if not email:
        return JSONResponse(status_code=401, content={"error": "Invalid token"})

    user = db.query(User).filter(User.email == email).first()
    if not user:
        return JSONResponse(status_code=404, content={"error": "User not found"})

    db_game = db.query(Game).filter(Game.id == id).first()
    if not db_game:
        return JSONResponse(status_code=404, content={"error": "Game not found"})

    if db_game.author != user.username:
        return JSONResponse(status_code=403, content={"error": "Not your game"})

    db.delete(db_game)
    db.commit()
    return {"message": f"Game '{db_game.name}' deleted successfully"}


@app.get("/history/{room_id}")
async def get_redis_history(room_id: str, summary="История чата",
    description="Получить историю сообщений по ID комнаты из Redis"):
    key = f"chat:{room_id}"
    messages = await redis_manager.redis_client.lrange(key, 0, -1)
    parsed_messages = [json.loads(msg) for msg in messages]
    return {"count": len(parsed_messages), "messages": parsed_messages}





if __name__ == "__main__":
    uvicorn.run("main:app", port=8001, reload=True)
