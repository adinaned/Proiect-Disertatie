from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Password1234@localhost:3306/users"
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
