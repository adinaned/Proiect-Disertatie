from src.controllers.controller import BaseController
from src.models.password import Password
from src.schemas import PasswordResponse, PasswordCreate


class PasswordController(BaseController):
    def __init__(self):
        super().__init__(Password, PasswordCreate, PasswordResponse)


password_controller = PasswordController()