import uuid
import json
from pprint import pprint

from encryption.lsag import calculate_ring_hash, lsag_verify
from models import Vote, Option, VotingSession, db
from schemas.vote_schema import VoteResponse
from datetime import datetime, timezone


def create_vote(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data or "submission_timestamp" in data or "token" in data:
        raise ValueError("You cannot manually set 'id', 'token' or 'submission_timestamp'")

    session_id = data.get("session_id")
    option_id = data.get("option_id")

    if not isinstance(session_id, int):
        raise ValueError("The 'session_id' field is required and must be an integer")
    if not db.session.get(VotingSession, session_id):
        raise ValueError("Voting session not found")

    if not isinstance(option_id, int):
        raise ValueError("The 'option_id' field is required and must be an integer")
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

    pprint(signature)

    message = str(option_id).encode()
    if not lsag_verify(message, signature):
        raise ValueError("Invalid LSAG signature")

    vote = Vote(
        session_id=session_id,
        option_id=option_id,
        token=str(uuid.uuid4()),
        key_image=json.dumps(key_image),
        signature=json.dumps(signature),
        ring_hash=calculate_ring_hash(session_id),
        submission_timestamp=datetime.now(timezone.utc)
    )

    db.session.add(vote)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return VoteResponse.model_validate(vote).model_dump()


def get_vote_by_token(vote_token):
    vote = db.session.get(Vote, vote_token)
    if not vote:
        return None

    return VoteResponse.model_validate(vote).model_dump()


def get_all_votes():
    votes = Vote.query.all()
    return [
        {
            "id": vote.id,
            "session_id": vote.session_id,
            "ring_hash": vote.ring_hash,
            "key_image": vote.key_image,
            "signature": vote.signature,
            "option_id": vote.option_id,
            "submission_timestamp": vote.submission_timestamp
        }
        for vote in votes
    ]
