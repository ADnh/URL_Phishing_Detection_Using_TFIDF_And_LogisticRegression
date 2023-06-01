from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, NVARCHAR, TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
# Đường dẫn url link db
db_url = 'mysql+pymysql://root:Ducanh23%40@localhost:3306/urldb'
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
Base.metadata.create_all(engine)

class users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(NVARCHAR(255))
    username = Column(String(255))
    password = Column(String(255))
    email = Column(String(255))
    is_admin = Column(Integer)
    scan_history = relationship("scan_history", back_populates="user")

class urls(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255))
    type = Column(Integer)

class scan_history(Base):
    __tablename__ = 'scan_history'
    id = Column(Integer, primary_key=True, index=True)
    scan_time = Column(TIMESTAMP)
    result = Column(Integer)
    url = Column(String(255))
    user_id = Column(Integer, ForeignKey(users.id))
    user = relationship("users", back_populates="scan_history")

class blacklist(Base):
    __tablename__ = 'blacklist'
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255))
    added_time = Column(TIMESTAMP)
    user_id = Column(Integer, ForeignKey(users.id))
