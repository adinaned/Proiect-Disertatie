from src.controllers.controller import BaseController
from src.models.vote_submission import VoteSubmission
from src.schemas import VoteSubmissionCreate, VoteSubmissionResponse


class VoteSubmissionController(BaseController):
    def __init__(self):
        super().__init__(VoteSubmission, VoteSubmissionCreate, VoteSubmissionResponse)


vote_submission_controller = VoteSubmissionController()