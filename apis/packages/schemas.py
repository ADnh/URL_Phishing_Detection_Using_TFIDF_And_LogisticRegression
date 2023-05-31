from pydantic import BaseModel
from datetime import date

# Users
class UserBase(BaseModel):
    username: str
    name: str

class UserCreate(UserBase):
    password: str
    email: str
    is_admin: int

class UserUpdate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# Urls
class UrlBase(BaseModel):
    url: str
    type: int

class UrlCreate(UrlBase):
    url: str
    type: int

class UrlUpdate(UrlBase):
    url: str
    type: int

class Url(UrlBase):
    id: int

    class Config:
        orm_mode = True

# History
class HistoryBase(BaseModel):
    scan_time: date
    result: int
    url: str
    user_id: int


class History(HistoryBase):
    id: int

    class Config:
        orm_mode = True

# Blacklist
class BlackListBase(BaseModel):
    url: str
    added_time: date
    user_id: int

class BlackListAdded(BlackListBase):
    url: str
    added_time: date
    user_id: int

class BlackList(BlackListBase):
    id: int
    class Config:
        orm_mode = True
