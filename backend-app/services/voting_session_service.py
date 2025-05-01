from datetime import datetime
from models import VotingSession, db
from schemas.voting_session_schema import VotingSessionResponse


def create_voting_session(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data or "created_at" in data:
        raise ValueError("You cannot manually set protected fields: id or created_at")

    title = data.get("title")
    description = data.get("description")

    if not title or not isinstance(title, str):
        raise ValueError("The 'title' field is required and must be a non-empty string")
    if len(title) > 255:
        raise ValueError("The 'title' must not exceed 255 characters")

    voting_session = VotingSession(
        title=title.strip(),
        description=description.strip() if description else None,
        created_at=datetime.utcnow()
    )

    db.session.add(voting_session)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return VotingSessionResponse.model_validate(voting_session).model_dump()


def get_voting_session_by_id(session_id):
    voting_session = db.session.get(VotingSession, session_id)
    if not voting_session:
        return None

    return VotingSessionResponse.model_validate(voting_session).model_dump()


def get_all_voting_sessions():
    voting_sessions = VotingSession.query.all()
    if not voting_sessions:
        return []

    return [VotingSessionResponse.model_validate(session).model_dump() for session in voting_sessions]


def update_voting_session(session_id, data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a non-empty dictionary")

    if "id" in data or "created_at" in data:
        raise ValueError("You cannot modify protected fields: id or created_at")

    voting_session = db.session.get(VotingSession, session_id)
    if not voting_session:
        raise ValueError("Voting session not found")

    if "title" in data:
        new_title = data["title"]
        if not isinstance(new_title, str) or not new_title.strip():
            raise ValueError("The 'title' field must be a non-empty string")
        if len(new_title) > 255:
            raise ValueError("The 'title' must not exceed 255 characters")
        voting_session.title = new_title.strip()

    if "description" in data:
        new_description = data["description"]
        voting_session.description = new_description.strip() if new_description else None

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
        db.session.rollback()
        raise e
