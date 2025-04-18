from src.controllers.controller import BaseController
from src.models.voting_session import VotingSession
from src.schemas import VotingSessionCreate, VotingSessionResponse


class VotingSessionController(BaseController):
    def __init__(self):
        super().__init__(VotingSession, VotingSessionCreate, VotingSessionResponse)


voting_session_controller = VotingSessionController()