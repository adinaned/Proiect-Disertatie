from src.controllers.controller import BaseController
from src.models.question import Question
from src.schemas import QuestionResponse, QuestionCreate


class QuestionController(BaseController):
    def __init__(self):
        super().__init__(Question, QuestionCreate, QuestionResponse)


question_controller = QuestionController()