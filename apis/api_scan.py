from fastapi import APIRouter, HTTPException
from packages.database import SessionLocal, scan_history, users
from datetime import datetime
from prediction import predict
import requests
import re
from sqlalchemy.sql import func, extract

router = APIRouter()
db = SessionLocal()

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

# Scan của khách: Chỉ scan và hiển thị kết quả
@router.post("/scan-guest")
async def scan_guest_url_(url: str):
    if is_valid_url(url) == True:
        is_phishing = predict(url)
        if is_phishing == 0:
            return "SAFE" 
        if is_phishing == 1:
            return "PHISHING" 
    else:
        return "Url doesn't exist!!"

# Scan của người dùng: Scan và gửi vào lịch sử
@router.post("/{user_id}-scanning")
async def scan_url_(user_id: int, url: str):
    user = db.query(users).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if is_valid_url(url) == True:
        new_scan_history = scan_history(
            scan_time=datetime.now(),
            result=predict(url),
            url=url,
            user_id=user_id
        )
        db.add(new_scan_history)
        db.commit()
        db.refresh(new_scan_history)
        return new_scan_history
    else:
        return "Url doesn't exit!!"

# Kiểm tra số lần quét của người dùng theo ngày, tuần, tháng
@router.get("/{user_id}/{month}/{year}/monthly-scanned")
async def get_scan_history_count(user_id: int, month: int, year: int):
    scan_history_count = db.query(func.count(scan_history.id)).\
        filter(scan_history.user_id == user_id).\
        filter(extract('month', scan_history.scan_time) == month).\
        filter(extract('year', scan_history.scan_time) == year).\
        scalar()
    return {"scan_history_count": scan_history_count}

@router.get("/{user_id}/{year}/week/{week_number}daily-scanned")
async def get_scan_history_count(user_id: int, year: int, week_number: int):
    scan_history_count = db.query(func.count(scan_history.id)). \
        filter(scan_history.user_id == user_id). \
        filter(extract('year', scan_history.scan_time) == year). \
        filter(func.week(scan_history.scan_time) == week_number). \
        scalar()
    return {"scan_history_count": scan_history_count}

@router.get("/{user_id}/{day}/{month}/{year}/daily-scanned")
async def get_scan_history_count(user_id: int, day: int, month: int, year: int):
    scan_history_count = db.query(func.count(scan_history.id)).\
        filter(scan_history.user_id == user_id).\
        filter(extract('day', scan_history.scan_time) == day).\
        filter(extract('month', scan_history.scan_time) == month).\
        filter(extract('year', scan_history.scan_time) == year).\
        scalar()
    return {"scan_history_count": scan_history_count}

# Trả về danh sách lọc đã quét trong tháng
@router.get("/{user_id}/monthly-scanned")
async def getMonthlyScanned(user_id: int, month: int, year: int):
    user = db.query(users).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    scan_ = db.query(scan_history.user_id, scan_history.url, scan_history.result, scan_history.scan_time,).\
        filter(scan_history.user_id == user_id).\
        filter(extract('month', scan_history.scan_time) == month).\
        filter(extract('year', scan_history.scan_time) == year)
    return {"scan_history": scan_.all()}

# Trả về danh sách lọc đã quét trong ngày
@router.get("/{user_id}/daily-scanned")
async def getMonthlyScanned(user_id: int, day:int, month: int, year: int):
    user = db.query(users).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    scan_ = db.query(scan_history.user_id, scan_history.url, scan_history.result, scan_history.scan_time,).\
        filter(scan_history.user_id == user_id).\
        filter(extract('day', scan_history.scan_time) == day).\
        filter(extract('month', scan_history.scan_time) == month).\
        filter(extract('year', scan_history.scan_time) == year)
    return {"scan_history": scan_.all()}