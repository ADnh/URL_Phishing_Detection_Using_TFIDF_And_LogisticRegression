from fastapi import APIRouter, HTTPException
from packages.database import SessionLocal, urls
from packages.schemas import UrlCreate, UrlUpdate
import re

def is_valid_url(url):
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # Giao thức (http://, https://, ftp://, ftps://)
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # Tên miền
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # Địa chỉ IP
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # Địa chỉ IPv6
        r'(?::\d+)?'  # Cổng
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(url_pattern, url) is not None

router = APIRouter()
db = SessionLocal()

@router.get("/")
async def get_list_url():
    url_list = db.query(urls).all()
    return url_list

@router.post("/create")
async def create_url(url: UrlCreate):
    if is_valid_url(url.url) == True:
        new_url = urls(url=url.url, type=url.type)
        try:
            db.add(new_url)
            db.commit()
            db.refresh(new_url)
            return new_url
        except:
            db.rollback()
            raise
        finally:
            db.close()
    else:
        return "Try again !!"
    
@router.get("/get/{url_id}")
async def get_url(url_id: int):
    url = db.query(urls).filter(urls.id == url_id).first()
    if not url:
        raise HTTPException(status_code=404, detail="Url not found")
    return url

@router.put("/update/{url_id}")
async def update_url(url_id: int, url: UrlUpdate):
    existing_url = db.query(urls).filter(urls.id == url_id).first()
    if not existing_url:
        raise HTTPException(status_code=404, detail="Url not found")
    try:
        if is_valid_url(existing_url.url) == True:
            existing_url.url = url.url
            db.commit()
            db.refresh(existing_url)
            return existing_url
        else:
            return "Url doen't exist!"
    except:
        db.rollback()
        raise
    finally:
        db.close()

@router.delete("/delete/{url_id}")
async def delete_url(url_id: int):
    url = db.query(urls).filter(urls.id == url_id).first()
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



