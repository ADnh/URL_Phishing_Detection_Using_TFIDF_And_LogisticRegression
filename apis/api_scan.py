from fastapi import APIRouter, HTTPException
from packages.database import SessionLocal, urls, scan_history, users
from datetime import datetime
from prediction import predict
import requests
import re

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
