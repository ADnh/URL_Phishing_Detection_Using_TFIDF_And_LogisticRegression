from fastapi import APIRouter, HTTPException
from packages.database import SessionLocal, users
from packages.schemas import UserCreate, UserUpdate

router = APIRouter()
db = SessionLocal()

@router.get("/")
async def get_list_user():
    user_list = db.query(users).all()
    return user_list

@router.post("/")
async def create_user(user: UserCreate):
    new_user = users(username=user.username, name=user.name, password=user.password, email=user.email, is_admin=user.is_admin)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except:
        db.rollback()
        raise
    finally:
        db.close()

@router.get("/get/{user_id}")
async def get_user(user_id: int):
    user = db.query(users).filter(users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# API endpoint để cập nhật thông tin người dùng dựa trên id
@router.put("/update/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    existing_user = db.query(users).filter(users.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        existing_user.username = user.username
        existing_user.name = user.name
        existing_user.password = user.password
        existing_user.email = user.email
        db.commit()
        db.refresh(existing_user)
        return existing_user
    except:
        db.rollback()
        raise
    finally:
        db.close()

# API endpoint để xóa người dùng dựa trên id
@router.delete("/delete/{user_id}")
async def delete_user(user_id: int):
    user = db.query(users).filter(users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    except:
        db.rollback()
        raise
    finally:
        db.close()

