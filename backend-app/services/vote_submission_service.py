from models import VoteSubmission, VotingSession, db
from schemas.vote_submission_schema import VoteSubmissionResponse


def create_vote_submission(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data:
        raise ValueError("You cannot manually set the ID")

    user_id = data.get("user_id")
    session_id = data.get("session_id")

    if not user_id or not isinstance(user_id, int):
        raise ValueError("The 'user_id' field is required and must be an integer")
    if not session_id or not isinstance(session_id, int):
        raise ValueError("The 'session_id' field is required and must be an integer")

    if not VotingSession.query.filter_by(id=session_id).first():
        raise ValueError(f"Voting session with id {session_id} does not exist")

    vote_submission = VoteSubmission(
        user_id=user_id,
        session_id=session_id,
        has_voted=False
    )

    try:
        vote_submission.save()
    except Exception as e:
        raise ValueError(f"Failed to create vote submission: {str(e)}")

    return VoteSubmissionResponse.model_validate(vote_submission).model_dump()


def get_vote_submission_by_id(submission_id):
    vote_submission = VoteSubmission.query.filter_by(id=submission_id).first()
    if not vote_submission:
        return None

    return VoteSubmissionResponse.model_validate(vote_submission).model_dump()


def get_all_vote_submissions():
    vote_submissions = VoteSubmission.query.all()
    if not vote_submissions:
        return []

    return [VoteSubmissionResponse.model_validate(submission).model_dump() for submission in vote_submissions]
