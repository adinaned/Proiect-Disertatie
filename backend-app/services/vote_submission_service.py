from models import VoteSubmission, VotingSession, User, db
from schemas.vote_submission_schema import VoteSubmissionResponse
from datetime import datetime, timezone


def create_vote_submission(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data:
        raise ValueError("You cannot manually set the ID")
    if "user_id" not in data:
        raise ValueError("The 'user_id' field is required")

    user_id = data.get("user_id")
    voting_session_id = data.get("voting_session_id")

    user = db.session.get(User, user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} does not exist")

    if not isinstance(voting_session_id, str):
        raise ValueError("The 'voting_session_id' field must be a valid UUID string")

    voting_session = db.session.get(VotingSession, voting_session_id)
    if not voting_session:
        raise ValueError(f"Voting session with ID {voting_session_id} does not exist")

    if datetime.now(timezone.utc) > voting_session.end_datetime:
        raise ValueError("You cannot submit a vote after the voting session has ended.")

    user = db.session.get(User, user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} does not exist")

    existing_submission = VoteSubmission.query.filter_by(
        user_id=user_id,
        voting_session_id=voting_session_id
    ).first()

    if existing_submission:
        raise ValueError("This user has already submitted a vote for the specified voting session.")

    vote_submission = VoteSubmission(
        user_id=user_id,
        voting_session_id=voting_session_id
    )

    try:
        db.session.add(vote_submission)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Failed to create vote submission: {str(e)}")

    return VoteSubmissionResponse.model_validate(vote_submission).model_dump()


def get_vote_submission_by_id(submission_id):
    vote_submission = db.session.get(VoteSubmission, submission_id)
    if not vote_submission:
        return {"message": "Vote submission not found."}

    voting_session = db.session.get(VotingSession, vote_submission.voting_session_id)
    if not voting_session:
        return {"message": "Associated voting session not found."}

    return {
        "message": "Vote submission retrieved successfully.",
        "data": {
            "user_id": vote_submission.user_id,
            "voting_session_id": vote_submission.voting_session_id
        }
    }


def get_all_vote_submissions_by_session_id(voting_session_id):
    voting_session = db.session.get(VotingSession, voting_session_id)
    if not voting_session:
        return {"message": f"Voting session with ID {voting_session_id} does not exist."}

    if voting_session.end_datetime > datetime.now(timezone.utc):
        return {
            "message": "Not allowed to view submission before the voting session has ended.",
        }
    vote_submissions = VoteSubmission.query.filter_by(voting_session_id=voting_session_id).all()

    return {
        "message": f"{len(vote_submissions)} vote submission(s) retrieved.",
        "data": [
            {
                "user_id": sub.user_id,
                "voting_session_id": sub.voting_session_id
            }
            for sub in vote_submissions
        ]
    }