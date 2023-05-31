from fastapi import APIRouter, HTTPException
from packages.database import SessionLocal
from packages.schemas import 
from datetime import datetime
from prediction import predict
import requests
import re

router = APIRouter()
db = SessionLocal()