import status
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import User
from auth import create_jwt, decode_jwt, verify_password, hash_password
from pydantic import BaseModel, EmailStr
from fastapi import Request, Form, status
from starlette.responses import RedirectResponse
import python_multipart
import bcrypt



app = FastAPI()
init_db()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
templates = Jinja2Templates(directory="templates")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str

class UserRegisterResponse(BaseModel):
    message: str

class UserLoginRequest(BaseModel):
    username: EmailStr
    password: str

class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"




@app.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserRegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        return JSONResponse(
            status_code=400,
            content={"error": "Пользователь уже существует"}
        )
    new_user = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    return JSONResponse(content={"message": "Пользователь успешно зарегистрирован"})



@app.post("/token", response_model=UserLoginResponse)
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

    token = create_jwt({"sub": user.email})
    response = JSONResponse(
        content={"access_token": token, "token_type": "bearer"}
    )
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response


def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return token

@app.get("/me")
def get_me(token: str = Depends(get_token_from_cookie), db: Session = Depends(get_db)):
    payload = decode_jwt(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"email": user.email, "active": user.is_active}



if __name__ == "__main__":
    uvicorn.run("register_and_login:app", port=8004, reload=True)