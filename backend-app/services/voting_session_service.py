import traceback
from datetime import date
from models import VotingSession, db
from schemas.voting_session_schema import VotingSessionResponse
from encryption import generate_ring
from apscheduler.triggers.date import DateTrigger
from dateutil import parser
import pytz
from datetime import timezone
import traceback


def save_ring_to_session(session_id):
    from routes.app_routes import app
    with app.app_context():
        session = db.session.get(VotingSession, session_id)
        if session:
            ring = generate_ring(session.id, session.role_id, session.organization_id)
            session.key_ring = ring
            db.session.commit()


def schedule_ring_generation(session):
    run_time = session.start_datetime
    if run_time.tzinfo is None:
        run_time = run_time.replace(tzinfo=timezone.utc)
    else:
        run_time = run_time.astimezone(timezone.utc)

    trigger = DateTrigger(run_date=run_time)
    from services.scheduler import scheduler
    scheduler.add_job(
        func=save_ring_to_session,
        args=[session.id],
        trigger=trigger,
        id=f"generate_ring_{session.id}",
        replace_existing=True
    )

    print(f"Scheduled job for session {session.id} at {run_time}")


def create_voting_session(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data:
        raise ValueError("You cannot manually set protected fields: id")

    title = data.get("title")
    if not title or not isinstance(title, str):
        raise ValueError("The 'title' field is required and must be a non-empty string")
    if len(title) > 255:
        raise ValueError("The 'title' must not exceed 50 characters")

    question = data.get("question")
    if not question or not isinstance(question, str):
        raise ValueError("The 'question' field is required and must be a non-empty string")
    if len(title) > 255:
        raise ValueError("The 'question' must not exceed 255 characters")

    role_id = data.get("role_id")
    organization_id = data.get("organization_id")

    start_datetime = data.get("start_datetime")
    end_datetime = data.get("end_datetime")

    voting_session = VotingSession(
        title=title.strip(),
        question=question.strip(),
        start_datetime=parser.isoparse(start_datetime).astimezone(pytz.utc),
        end_datetime=parser.isoparse(end_datetime).astimezone(pytz.utc),
        role_id=role_id,
        organization_id=organization_id,
        key_ring=None
    )

    db.session.add(voting_session)

    try:
        db.session.commit()
        schedule_ring_generation(voting_session)
    except Exception as e:
        db.session.rollback()
        raise e

    return VotingSessionResponse.model_validate(voting_session).model_dump()


def get_voting_session_by_id(session_id):
    voting_session = db.session.get(VotingSession, session_id)
    if not voting_session:
        return None

    return VotingSessionResponse.model_validate(voting_session).model_dump()


def get_ring_by_voting_session(voting_session):
    return voting_session.get("key_ring")


def get_all_voting_sessions():
    voting_sessions = VotingSession.query.all()
    if not voting_sessions:
        return []

    return [VotingSessionResponse.model_validate(session).model_dump() for session in voting_sessions]


def update_voting_session(session_id, data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a non-empty dictionary")

    if "id" in data:
        raise ValueError("You cannot modify protected fields: id")

    voting_session = db.session.get(VotingSession, session_id)
    if not voting_session:
        raise ValueError("Voting session not found")

    if "title" in data:
        new_title = data["title"]
        if not isinstance(new_title, str) or not new_title.strip():
            raise ValueError("The 'title' field must be a non-empty string")
        if len(new_title) > 50:
            raise ValueError("The 'title' must not exceed 50 characters")
        voting_session.title = new_title.strip()

    if "question" in data:
        new_question = data["question"]
        if not isinstance(new_question, str) or not new_question.strip():
            raise ValueError("The 'question' field must be a non-empty string")
        if len(new_question) > 255:
            raise ValueError("The 'question' must not exceed 255 characters")
        voting_session.question = new_question.strip()

    if "end_data" in data:
        new_end_data = data["end_data"]
        if not isinstance(new_end_data, date):
            raise ValueError("The 'end_data' field must be a valid date")

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return VotingSessionResponse.model_validate(voting_session).model_dump()


def delete_voting_session(session_id):
    voting_session = db.session.get(VotingSession, session_id)
    if not voting_session:
        return {"message": "Voting session not found"}

    db.session.delete(voting_session)

    try:
        db.session.commit()
        return {"message": "Voting session deleted successfully"}
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        raise e
