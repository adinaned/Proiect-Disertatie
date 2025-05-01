from src.controllers.controller import BaseController
from src.models.email import Email
from src.schemas import EmailCreate, EmailResponse


class EmailController(BaseController):
    def __init__(self):
        super().__init__(Email, EmailCreate, EmailResponse)


email_controller = EmailController()