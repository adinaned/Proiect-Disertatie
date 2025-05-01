from src.controllers.controller import BaseController
from src.models.role import Role
from src.schemas import RoleCreate, RoleResponse


class RoleController(BaseController):
    def __init__(self):
        super().__init__(Role, RoleCreate, RoleResponse)


role_controller = RoleController()