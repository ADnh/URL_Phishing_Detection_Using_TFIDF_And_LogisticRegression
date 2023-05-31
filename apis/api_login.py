from fastapi import APIRouter, HTTPException, Depends
from packages.database import SessionLocal
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from packages.database import users
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

router = APIRouter()
db = SessionLocal()

# Khởi tạo một instance của PWDContext để xác thực mật khẩu
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Thông tin cấu hình cho JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Bảo mật API bằng JWT
bearer_scheme = HTTPBearer()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str, db):
    try:
        user = db.query(users).filter(users.username == username).one()
        if verify_password(password, user.password):
            return user
    except NoResultFound:
        return None

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_token(auth: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if not auth.scheme or auth.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    if not auth.credentials:
        raise HTTPException(status_code=401, detail="Invalid token")
    return auth.credentials

def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        db = SessionLocal()
        user = db.query(users).filter(users.username == username).first()
        db.close()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")


@router.post("/register")
async def register(username: str, password: str, name: str, email: str, db: SessionLocal = Depends(get_db)):
    hashed_password = get_password_hash(password)
    user = users(username=username, password=hashed_password)
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        return {"message": "User registered successfully", "username": user.username}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")

@router.post("/login")
async def login(username: str, password: str, db: SessionLocal = Depends(get_db)):
    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(current_user: users = Depends(get_current_user)):
    # Ghi lại thông tin hoặc thực hiện các thao tác khác liên quan đến việc đăng xuất người dùng
    return {"message": "User logged out successfully"}