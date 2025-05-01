from src.controllers.controller import BaseController
from src.models.vote import Vote
from src.schemas import VoteCreate, VoteResponse


class VoteController(BaseController):
    def __init__(self):
        super().__init__(Vote, VoteCreate, VoteResponse)


vote_controller = VoteController()