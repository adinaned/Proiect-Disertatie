from src.controllers.controller import BaseController
from src.models.profile_status import ProfileStatus
from src.schemas import ProfileStatusResponse, ProfileStatusCreate


class ProfileStatusController(BaseController):
    def __init__(self):
        super().__init__(ProfileStatus, ProfileStatusCreate, ProfileStatusResponse)


profile_status_controller = ProfileStatusController()