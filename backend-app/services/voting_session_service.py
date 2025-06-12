from datetime import datetime, timezone, timedelta
from apscheduler.triggers.date import DateTrigger
from dateutil import parser
import pytz
import traceback
import logging

from encryption import generate_ring
from models import VotingSession, db, Organization, Role
from schemas.voting_session_schema import VotingSessionResponse

logger = logging.getLogger(__name__)


def save_ring_to_session(voting_session_id):
    from routes.app_routes import app
    with app.app_context():
        session = db.session.get(VotingSession, voting_session_id)
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


def validate_start_datetime(start_datetime, minimum_delta):
    now = datetime.now(timezone.utc)
    if start_datetime < now:
        raise ValueError("The 'start_datetime' cannot be in the past.")
    # if start_datetime < now + minimum_delta:
    #     raise ValueError("The 'start_datetime' must be at least 30 minutes from now.")


def validate_end_datetime(start_datetime, end_datetime, minimum_delta):
    if end_datetime <= start_datetime:
        raise ValueError("The 'end_datetime' must be after 'start_datetime'.")
    if end_datetime < start_datetime + minimum_delta:
        raise ValueError("The 'end_datetime' must be at least 30 minutes after the 'start_datetime'.")


def parse_datetime(value: str):
    try:
        dt = parser.isoparse(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=pytz.UTC)
        else:
            dt = dt.astimezone(pytz.UTC)
        return dt
    except Exception:
        raise ValueError("Invalid datetime format. Please use ISO 8601 (e.g., '2025-06-08T08:24:47')")


def create_voting_session(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data:
        raise ValueError("You cannot manually set the 'id' field.")

    required_fields = ["title", "question", "start_datetime", "end_datetime", "role_id", "organization_id"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")

    title = data["title"].strip()
    question = data["question"].strip()
    role_id = data["role_id"].strip()
    organization_id = data["organization_id"].strip()

    if not title:
        raise ValueError("The 'title' field must not be empty.")
    if len(title) > 50:
        raise ValueError("The 'title' must not exceed 50 characters.")
    if len(title) < 3:
        raise ValueError("The 'title' must be at least 3 characters long.")

    if not question:
        raise ValueError("The 'question' field must not be empty.")
    if len(question) > 255:
        raise ValueError("The 'question' must not exceed 255 characters.")
    if len(question) < 10:
        raise ValueError("The 'question' must be at least 10 characters long.")

    organization = db.session.get(Organization, organization_id)
    if not organization:
        raise ValueError(f"Organization with id '{organization_id}' does not exist.")

    role = db.session.get(Role, role_id)
    if not role:
        raise ValueError(f"Role with id '{role_id}' does not exist.")

    if role.organization_id != organization_id:
        raise ValueError(f"Role '{role.name}' does not belong to organization '{organization.name}'.")

    try:
        start_datetime = parse_datetime(data["start_datetime"])
        end_datetime = parse_datetime(data["end_datetime"])
    except Exception:
        raise ValueError("Invalid datetime format. Use ISO 8601 format.")

    minimum_delta = timedelta(minutes=30)
    validate_start_datetime(start_datetime, minimum_delta)
    validate_end_datetime(start_datetime, end_datetime, minimum_delta)

    if "key_ring" in data:
        raise ValueError("You cannot manually set the 'key_ring'. It is system generated.")

    voting_session = VotingSession(
        title=title,
        question=question,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
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


def get_voting_session_by_id(voting_session_id):
    try:
        session = db.session.get(VotingSession, voting_session_id)
        if not session:
            return None
        return VotingSessionResponse.model_validate(session).model_dump()
    except Exception as e:
        traceback.print_exc()
        raise e


def get_ring_by_voting_session(voting_session):
    return voting_session["key_ring"]


def get_all_voting_sessions_by_organization_id(organization_id):
    try:
        sessions = VotingSession.query.filter_by(organization_id=organization_id).all()
        return [VotingSessionResponse.model_validate(s).model_dump() for s in sessions]
    except Exception as e:
        traceback.print_exc()
        raise e


def get_all_voting_sessions_by_organization_id_and_role_id(organization_id, role_id):
    try:
        sessions = VotingSession.query.filter(
            VotingSession.organization_id == organization_id,
            VotingSession.role_id == role_id
        ).all()
        return [VotingSessionResponse.model_validate(s).model_dump() for s in sessions]
    except Exception as e:
        traceback.print_exc()
        raise e


def update_voting_session(voting_session_id, data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object.")

    forbidden_fields = {"id", "organization_id", "role_id"}
    present_forbidden = forbidden_fields & data.keys()
    if present_forbidden:
        raise ValueError(f"You are not allowed to modify the following field(s): {', '.join(present_forbidden)}")

    voting_session = db.session.get(VotingSession, voting_session_id)
    if not voting_session:
        raise ValueError("Voting session not found")

    if "title" in data:
        new_title = data["title"].strip()
        if not new_title:
            raise ValueError("The 'title' must not be empty.")
        if len(new_title) > 50:
            raise ValueError("The 'title' must not exceed 50 characters.")
        voting_session.title = new_title

    if "question" in data:
        new_question = data["question"].strip()
        if not new_question:
            raise ValueError("The 'question' must not be empty.")
        if len(new_question) > 255:
            raise ValueError("The 'question' must not exceed 255 characters.")
        voting_session.question = new_question

    start_datetime = voting_session.start_datetime
    minimum_delta = timedelta(minutes=30)
    if "start_datetime" in data:
        start_datetime = parse_datetime(data["start_datetime"])

        validate_start_datetime(start_datetime, minimum_delta)
        voting_session.start_datetime = start_datetime
    if "end_datetime" in data:
        end_datetime = parse_datetime(data["end_datetime"])
        validate_end_datetime(start_datetime, end_datetime, minimum_delta)
        voting_session.end_datetime = end_datetime

    if "key_ring" in data:
        raise ValueError("You cannot manually set the 'key_ring'. It is system generated.")

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return VotingSessionResponse.model_validate(voting_session).model_dump()


def delete_voting_session(voting_session_id):
    logger.debug("Trying to delete voting session with id: %s", voting_session_id)
    voting_session = db.session.get(VotingSession, voting_session_id)

    if not voting_session:
        logger.warning("Voting session not found for id: %s", voting_session_id)
        return {"message": "Voting session not found"}

    start_dt = voting_session.start_datetime
    if start_dt.tzinfo is None:
        start_dt = start_dt.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    if start_dt <= now:
        logger.warning("Cannot delete voting session %s because it has already started", voting_session_id)
        return {"message": "Cannot delete a voting session that has already started."}

    try:
        num_options = len(voting_session.options)
        db.session.delete(voting_session)
        db.session.commit()
        logger.info("Deleted voting session %s and %d options", voting_session_id, num_options)

        return {
            "message": f"Voting session deleted. {num_options} option(s) also removed.",
            "data": {"id": voting_session_id}
        }
    except Exception:
        logger.exception("Exception while deleting voting session")
        db.session.rollback()
        raise
