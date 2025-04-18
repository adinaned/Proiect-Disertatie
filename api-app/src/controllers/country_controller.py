from src.controllers.controller import BaseController
from src.models.country import Country
from src.schemas import CountryCreate, CountryResponse


class CountryController(BaseController):
    def __init__(self):
        super().__init__(Country, CountryCreate, CountryResponse)


country_controller = CountryController()
