import smtplib

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
from fastapi.middleware.cors import CORSMiddleware
from email.mime.text import MIMEText
from email_validator import validate_email, EmailNotValidError
import dns.resolver
import random






app = FastAPI()
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9000",'http://localhost:8000'],  # або конкретно ["http://localhost:9000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




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



class EmailVerificationRequest(BaseModel):
    email: EmailStr
    code: str




@app.post("/register")
def register(user: UserRegisterRequest, db: Session = Depends(get_db)):
    try:
        email = validate_email_and_domain(user.email)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return JSONResponse(
            status_code=400,
            content={"error": "Пользователь с таким email уже существует"}
        )

    code = generate_verification_code()
    new_user = User(
        email=email,
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

    return {"message": "Пользователь зарегистрирован. Проверьте почту для подтверждения."}



@app.post("/verify-email")
def verify_email(data: EmailVerificationRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        return JSONResponse(status_code=404, content={"error": "Пользователь не найден"})
    if user.is_verified:
        return {"message": "Email уже подтверждён"}
    if user.verification_code != data.code:
        return JSONResponse(status_code=400, content={"error": "Неверный код подтверждения"})

    user.is_verified = True
    user.verification_code = None
    db.commit()
    return {"message": "Email успешно подтверждён"}



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
        raise JSONResponse(status_code=401, content={"error": "Not authenticated"})
    return token


@app.get("/me")
def get_me(token: str = Depends(get_token_from_cookie), db: Session = Depends(get_db)):
    payload = decode_jwt(token)
    if not payload:
        return JSONResponse(status_code=401, content={"error": "Invalid token"})
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return JSONResponse(status_code=404, content={"error": "User not found"})
    return {"email": user.email, "active": user.is_active}



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



if __name__ == "__main__":
    uvicorn.run("register_and_login:app", port=8000, reload=True)