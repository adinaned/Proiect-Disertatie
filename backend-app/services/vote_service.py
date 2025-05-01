from datetime import datetime
import uuid

from models import Vote, Question, Option, VotingSession, db
from schemas.vote_schema import VoteResponse


def create_vote(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data or "submission_timestamp" in data or "token" in data:
        raise ValueError("You cannot manually set 'id', 'token' or 'submission_timestamp'")

    session_id = data.get("session_id")
    question_id = data.get("question_id")
    option_id = data.get("option_id")

    if not isinstance(session_id, int):
        raise ValueError("The 'session_id' field is required and must be an integer")
    if not db.session.get(VotingSession, session_id):
        raise ValueError("Voting session not found")

    if not isinstance(question_id, int):
        raise ValueError("The 'question_id' field is required and must be an integer")
    if not db.session.get(Question, question_id):
        raise ValueError("Question not found")

    if not isinstance(option_id, int):
        raise ValueError("The 'option_id' field is required and must be an integer")
    if not db.session.get(Option, option_id):
        raise ValueError("Option not found")

    vote = Vote(
        session_id=session_id,
        question_id=question_id,
        option_id=option_id,
        token=str(uuid.uuid4()),
        submission_timestamp=datetime.now()
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
            "question_id": vote.question_id,
            "option_id": vote.option_id,
            "submission_timestamp": vote.submission_timestamp
        }
        for vote in votes
    ]
