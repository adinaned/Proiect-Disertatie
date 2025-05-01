from src.controllers.controller import BaseController
from src.models.user import User
from src.schemas import UserCreate, UserResponse


class UserController(BaseController):
    def __init__(self):
        super().__init__(User, UserCreate, UserResponse)


user_controller = UserController()