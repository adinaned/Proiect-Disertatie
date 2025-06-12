from flask import jsonify

def logout():
    response = jsonify({"message": "Logged out successfully."})
    response.set_cookie("token", "", expires=0, httponly=True, samesite="Lax")
    return response