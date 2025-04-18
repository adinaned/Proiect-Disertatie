from src.controllers.controller import BaseController
from src.models.option import Option
from src.schemas import OptionCreate, OptionResponse


class OptionController(BaseController):
    def __init__(self):
        super().__init__(Option, OptionCreate, OptionResponse)


option_controller = OptionController()