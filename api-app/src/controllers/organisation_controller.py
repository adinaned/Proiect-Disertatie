from src.controllers.controller import BaseController
from src.models.organisation import Organisation
from src.schemas import OrganisationCreate, OrganisationResponse


class OrganisationController(BaseController):
    def __init__(self):
        super().__init__(Organisation, OrganisationCreate, OrganisationResponse)


organisation_controller = OrganisationController()