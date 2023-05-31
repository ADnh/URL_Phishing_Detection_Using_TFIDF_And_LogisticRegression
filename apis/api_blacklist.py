from fastapi import APIRouter, HTTPException
from packages.database import SessionLocal, blacklist, users
from packages.schemas import BlackListAdded
from datetime import datetime
from api_scan import is_valid_url

router = APIRouter()
db = SessionLocal()

@router.get("/")
async def get_blacklist():
    blacklist_ = db.query(blacklist).all()
    return blacklist_

@router.get("/get/{user_id}")
async def get_url(user_id: int):
    blacklist_ = db.query(blacklist).filter(blacklist.user_id == user_id).first()
    if not blacklist_:
        raise HTTPException(status_code=404, detail="Black-list not found")
    return blacklist_

# Thêm url vào danh sách đen
@router.post("/{user_id}-{url}-toBlackList")
async def toBlackList(toBlackList: BlackListAdded):
    user = db.query(users).get(toBlackList.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if is_valid_url(toBlackList.url) == True:
        new_blacklist = blacklist(
            user_id=toBlackList.user_id,
            url=toBlackList.url,
            added_time=datetime.now()
            )
        try:
            db.add(new_blacklist)
            db.commit()
            db.refresh(new_blacklist)
            return new_blacklist
        except:
            db.rollback()
            raise
        finally:
            db.close()
    else:
        return "Url doesn't exist !!"

@router.delete("/delete/{id}")
async def delete_url(id: int):
    url = db.query(blacklist).filter(blacklist.id == id).first()
    if not url:
        raise HTTPException(status_code=404, detail="Url not found")
    try:
        db.delete(url)
        db.commit()
        return {"message": "Url deleted successfully"}
    except:
        db.rollback()
        raise
    finally:
        db.close()



