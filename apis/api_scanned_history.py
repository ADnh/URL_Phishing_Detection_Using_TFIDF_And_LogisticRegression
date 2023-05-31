from fastapi import APIRouter, HTTPException
from packages.database import SessionLocal, scan_history

router = APIRouter()
db = SessionLocal()

@router.get("/")
async def get_list_url():
    url_list = db.query(scan_history).all()
    return url_list

@router.get("/get/{history_id}")
async def get_user(history_id: int):
    history = db.query(scan_history).filter(scan_history.id == history_id).first()
    if not history:
        raise HTTPException(status_code=404, detail="History not found")
    return history

@router.delete("/delete/{history_id}")
async def delete_history(history_id: int):
    history = db.query(scan_history).filter(scan_history.id == history_id).first()
    if not history:
        raise HTTPException(status_code=404, detail="History not found")
    try:
        db.delete(history)
        db.commit()
        return {"message": "History deleted successfully"}
    except:
        db.rollback()
        raise
    finally:
        db.close()
