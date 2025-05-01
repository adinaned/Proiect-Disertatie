from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Password1234@localhost:3306/users"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print("Could not establish DB connection because {}" .format(e))
    finally:
        db.close()

def check_db_connection():
    db_session = None
    try:
        db_session = next(get_db())
        db_session.execute(text('SELECT 1'))
        return {"status": "success", "message": "Connection to the database was successful!"}
    except SQLAlchemyError as e:
        return {"status": "error", "message": f"Could not connect to the database: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}
    finally:
        if db_session:
            db_session.close()

def create_tables():
    Base.metadata.create_all(bind=engine)

def drop_tables():
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped.")