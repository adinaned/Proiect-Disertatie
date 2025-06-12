from datetime import datetime, timezone
import uuid
import json

from encryption.lsag import calculate_ring_hash, lsag_verify
from models import Vote, Option, VotingSession, db
from schemas.vote_schema import VoteResponse
from services.public_key_service import create_public_key

from models import VoteSubmission, User
from sqlalchemy.exc import SQLAlchemyError


def create_vote(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data or "submission_timestamp" in data or "token" in data:
        raise ValueError("You cannot manually set 'id', 'token' or 'submission_timestamp'")

    voting_session_id = data.get("voting_session_id")
    option_id = data.get("option_id")

    if "voting_session_id" not in data:
        raise ValueError("The 'voting_session_id' field is required.")

    voting_session = db.session.get(VotingSession, voting_session_id)
    if not voting_session:
        raise ValueError("Voting session not found.")

    end_dt = voting_session.end_datetime
    if end_dt.tzinfo is None:
        end_dt = end_dt.replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) > end_dt:
        raise ValueError("Voting session has already ended. Cannot submit a vote.")

    if "option_id" not in data:
        raise ValueError("The 'option_id' field is required.")
    if not db.session.get(Option, option_id):
        raise ValueError("Option not found")

    key_image = data.get("key_image")
    signature = data.get("signature")

    if isinstance(signature, str):
        try:
            signature = json.loads(signature)
        except Exception:
            pass

    if isinstance(key_image, str):
        try:
            key_image = json.loads(key_image)
        except Exception:
            pass

    message = str(option_id).encode()
    print(f"message {message}")
    if not lsag_verify(message, signature):
        raise ValueError("Invalid LSAG signature")

    vote = Vote(
        voting_session_id=voting_session_id,
        option_id=option_id,
        token=str(uuid.uuid4()),
        key_image=json.dumps(key_image),
        signature=json.dumps(signature),
        ring_hash=calculate_ring_hash(voting_session_id),
        submission_timestamp=datetime.now(timezone.utc)
    )

    vote_submission = VoteSubmission(
        user_id=user_id,
        voting_session_id=voting_session_id,
        has_voted=True
    )

    try:
        db.session.add(vote)
        db.session.add(vote_submission)
        create_public_key({"user_id": user_id, "voting_session_id": voting_session_id})
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise ValueError(f"Failed to create vote and submission: {str(e)}")

    return VoteResponse.model_validate(vote).model_dump()


def get_vote_by_token(vote_token):
    vote = db.session.get(Vote, vote_token)
    if not vote:
        return {"message": "Vote not found."}

    voting_session = db.session.get(VotingSession, vote.voting_session_id)
    if not voting_session:
        return {"message": "Associated voting session not found."}

    return {
        "message": "Vote retrieved successfully.",
        "data": {
            "id": vote.id,
            "voting_session_id": vote.voting_session_id,
            "option_id": vote.option_id,
            "submission_timestamp": vote.submission_timestamp
        }
    }


def get_all_votes_by_voting_session_id(voting_session_id):
    voting_session = db.session.get(VotingSession, voting_session_id)
    if not voting_session:
        return {"message": "Voting session not found."}

    if datetime.now(timezone.utc) < voting_session.end_datetime:
        return {"message": "Not allowed to view votes before the voting session has ended."}

    votes = Vote.query.filter_by(voting_session_id=voting_session_id).all()
    return {
        "message": f"{len(votes)} vote(s) retrieved.",
        "data": [
            {
                "id": vote.id,
                "voting_session_id": vote.voting_session_id,
                "option_id": vote.option_id,
                "submission_timestamp": vote.submission_timestamp
            }
            for vote in votes
        ]
    }
