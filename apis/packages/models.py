from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, NVARCHAR, TIMESTAMP
from sqlalchemy.orm import relationship
from packages.database import engine

metadata = MetaData()

user_table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('name', NVARCHAR(255)),
    Column('username', String(255)),
    Column('password', String(255)),
    Column('email', String(255)),
    Column('is_admin', Integer),
    autoload=True, autoload_with=engine, extend_existing=True
)

url_table = Table(
    'urls',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('url', String(300)),
    Column('type', Integer),
    autoload=True, autoload_with=engine, extend_existing=True
)

history_table = Table(
    'scan_history',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('scan_time', TIMESTAMP),
    Column('result', Integer),
    Column('url', String(300)),
    Column('user_id', Integer, ForeignKey("users.iduser")),
    autoload=True, autoload_with=engine, extend_existing=True
)

blacklist_table = Table(
    'blacklist',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('url', String(300)),
    Column('added_time', TIMESTAMP),
    Column('user_id', Integer, ForeignKey("users.iduser")),
    autoload=True, autoload_with=engine, extend_existing=True
)
