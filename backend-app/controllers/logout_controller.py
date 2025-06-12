from flask import jsonify, request
from services import logout


def logout_user():
    return logout()
