from fastapi import FastAPI
from src.routers import country_router, email_router, organisation_router, role_router, option_router, profile_status_router, user_router, vote_router, vote_submission_router, voting_session_router, question_router, password_router
from src.db.database import check_db_connection, create_tables, drop_tables
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    result = check_db_connection()

    if result["status"] == "error":
        raise Exception(f"Database connection failed: {result['message']}")
    else:
        print(result["message"])
        # drop_tables()
        create_tables()
        print("Database tables created (if they don't exist).")

    yield
    print("Application is shutting down")


app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Welcome to the application!"}

app.include_router(country_router.router)
app.include_router(email_router.router)
app.include_router(option_router.router)
app.include_router(organisation_router.router)
app.include_router(password_router.router)
app.include_router(profile_status_router.router)
app.include_router(question_router.router)
# app.include_router(role_router.router)
app.include_router(user_router.router)
app.include_router(vote_router.router)
app.include_router(vote_submission_router.router)
app.include_router(voting_session_router.router)