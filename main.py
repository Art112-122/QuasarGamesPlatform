import smtplib

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import init_db, SessionLocal
from app.auth import create_jwt, decode_jwt, verify_password, hash_password
from app.models import Game, User
from fastapi.middleware.cors import CORSMiddleware
from email.mime.text import MIMEText
from email_validator import validate_email, EmailNotValidError
import dns.resolver
import random
from app.schemas import UserRegisterRequest, UserLoginResponse, EmailVerificationRequest, GameCreate, GameUpdate
from fastapi import Depends,  Query
from typing import Optional







app = FastAPI()
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9000",'http://localhost:8000'],  # або конкретно ["http://localhost:9000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



##########################################часть з регистрацией#################################################################
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/register")
def register(user: UserRegisterRequest, db: Session = Depends(get_db)):
    try:
        email = validate_email_and_domain(user.email)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

    token = create_jwt({"sub": user.email})


    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return JSONResponse(
            status_code=400,
            content={"error": "Пользователь с таким email уже существует"}
        )


    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        return JSONResponse(
            status_code=400,
            content={"error": "Пользователь с таким username уже существует"}
        )

    code = generate_verification_code()
    new_user = User(
        email=email,
        username=user.username,
        hashed_password=hash_password(user.password),
        is_verified=False,
        verification_code=code
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    try:
        send_verification_email(email, code)
    except Exception as e:
        db.delete(new_user)
        db.commit()
        return JSONResponse(
            status_code=500,
            content={"error": f"Не удалось отправить письмо: {str(e)}"}
        )

    return {
        "message": "Пользователь зарегистрирован. Проверьте почту для подтверждения.",
        "access_token": token
    }



@app.post("/verify-email")
def verify_email(data: EmailVerificationRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_jwt(token)
    email = payload.get("sub")
    if not email:
        return JSONResponse(status_code=401, content={"error": "Invalid token"})
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return JSONResponse(status_code=404, content={"error": "Пользыватель не найден"})
    if user.verification_code != data.code:
        return JSONResponse(status_code=400, content={"error": "Неверный код подтверждения"})

    user.is_verified = True
    user.verification_code = None
    db.commit()
    return {"message": "Email успешно подтверждён"}



@app.post("/login", response_model=UserLoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        return JSONResponse(
            status_code=400,
            content={"error": "Неверный email или пароль"}
        )

    token_raw = create_jwt({"sub": user.email})
    token = UserLoginResponse(access_token=token_raw)
    return token




@app.get("/me")
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_jwt(token)
    email = payload.get("sub")
    if not email:
        return JSONResponse(status_code=401, content={"error": "Invalid token"})
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return JSONResponse(status_code=404, content={"error": "User not found"})
    return {"email": user.email, "username": user.username}



def validate_email_and_domain(email: str) -> str:
    try:
        valid = validate_email(email)
        email = valid.normalized
    except EmailNotValidError as e:
        raise Exception(f"Неверный формат email: {str(e)}")
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'MX')
    except Exception:
        raise Exception("Домен не принимает почту (нет MX-записей)")
    return email

def generate_verification_code(length=6) -> str:
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def send_verification_email(to_email: str, code: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "loot.market999@gmail.com"
    smtp_password = "jbqj trld kals wejm"
    subject = "Код подтверждения регистрации"


    html_content = f"""
    <html>
    <head>
      <style>
        .container {{
          max-width: 600px;
          margin: auto;
          padding: 20px;
          font-family: 'Arial', sans-serif;
          background-color: #f9f9f9;
          border-radius: 10px;
          box-shadow: 0 0 10px rgba(0,0,0,0.1);
          text-align: center;
        }}
        .code {{
          font-size: 48px;
          font-weight: bold;
          color: #4CAF50;
          letter-spacing: 10px;
          margin: 20px 0;
        }}
        .header-img {{
          border-radius: 10%;
          width: 100px;
          margin-bottom: 20px;
        }}
        .footer {{
          font-size: 12px;
          color: #888;
          margin-top: 30px;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <img class="header-img" src="https://media.istockphoto.com/id/1560833158/ru/%D1%84%D0%BE%D1%82%D0%BE/%D0%B8%D0%B3%D1%80%D0%BE%D0%B2%D0%BE%D0%B9-%D0%BA%D0%BE%D0%BD%D1%82%D1%80%D0%BE%D0%BB%D0%BB%D0%B5%D1%80-%D1%81-%D0%BA%D0%BB%D0%B0%D0%B2%D0%B8%D0%B0%D1%82%D1%83%D1%80%D0%BE%D0%B9-%D1%81-%D1%84%D0%B8%D0%BE%D0%BB%D0%B5%D1%82%D0%BE%D0%B2%D0%BE%D0%B9-%D0%BF%D0%BE%D0%B4%D1%81%D0%B2%D0%B5%D1%82%D0%BA%D0%BE%D0%B9-%D1%81%D1%80%D0%B5%D0%B4%D0%B8-%D1%80%D0%B0%D0%B7%D0%BB%D0%B8%D1%87%D0%BD%D1%8B%D1%85-%D0%B1%D0%B5%D1%81%D0%BF%D1%80%D0%BE%D0%B2%D0%BE%D0%B4%D0%BD%D1%8B%D1%85-%D1%83%D1%81%D1%82%D1%80%D0%BE%D0%B9%D1%81%D1%82%D0%B2.jpg?s=612x612&w=0&k=20&c=8aeUUhLpZZUTNta-FK5n3TEdb2S6oLeJiR28sIZkbAo=" alt="Verification" />
        <h2>Код подтверждения регистрации</h2>
        <p>Введите следующий код для подтверждения вашего email:</p>
        <div class="code">{code}</div>
        <p>Если вы не запрашивали этот код, просто проигнорируйте это письмо.</p>
        <div class="footer">© 2026 Ваша компания</div>
      </div>
    </body>
    </html>
    """

    msg = MIMEText(html_content, "html")
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())


############################################часть з проверкой на автефикацию############################################





@app.get("/games")
def get_games(
    game: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Game)
    if game:
        query = query.filter(Game.game == game)
    if category:
        query = query.filter(Game.category == category)

    result = query.all()
    return [{"id": g.id, "name": g.name, "author": g.author} for g in result]


@app.get("/games/id")
def get_game_by_id(
    id: int = Query(...),
    token: Optional[str] = Depends(OAuth2PasswordBearer(tokenUrl="login", auto_error=False)),
    db: Session = Depends(get_db)
):
    user = None
    if token:
        decoded = decode_jwt(token)
        if not decoded is None:
            email = decoded.get("sub")
            if email:
                user = db.query(User).filter(User.email == email).first()

    db_game = db.query(Game).filter(
        Game.id == id,
    ).first()

    if not db_game:
        return JSONResponse(status_code=404, content={"error": "Game not found"})

    return {
        "name": db_game.name,
        "description": db_game.description,
        "author": db_game.author,
        "is_author": user and db_game.author == user.username,
        "created_at": db_game.created_at
    }

@app.post("/games/add")
def add_game(payload: GameCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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
def update_game(payload: GameUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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

    if payload.description:
        db_game.description = payload.description

    db.commit()
    db.refresh(db_game)
    return {"message": f"Game '{db_game.name}' updated successfully"}



@app.delete("/games")
def delete_game(id: int = Query(...), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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




if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)