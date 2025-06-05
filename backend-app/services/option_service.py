from models import Option, db
from schemas.option_schema import OptionResponse


def create_option(data, session_id):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data:
        raise ValueError("You cannot manually set the ID")

    name = data.get("name")

    if not name or not isinstance(name, str):
        raise ValueError("The 'name' field is required and must be a non-empty string")
    if len(name) > 250:
        raise ValueError("The 'name' field must not exceed 250 characters")

    option = Option(
        name=name.strip(),
        session_id=session_id
    )

    db.session.add(option)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return OptionResponse.model_validate(option).model_dump()


def get_option_by_id(option_id):
    option = db.session.get(Option, option_id)
    if not option:
        return None

    return OptionResponse.model_validate(option).model_dump()

def get_all_options_by_session_id(session_id):
    options = Option.query.filter_by(session_id=session_id).all()
    if not options:
        return []

    return [OptionResponse.model_validate(option).model_dump() for option in options]

def get_all_options():
    options = Option.query.all()
    if not options:
        return []

    return [OptionResponse.model_validate(option).model_dump() for option in options]


def update_option(option_id, data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a non-empty dictionary")

    if "id" in data:
        raise ValueError("You cannot modify the ID")

    option = db.session.get(Option, option_id)
    if not option:
        raise ValueError("Option not found")

    if "name" in data:
        name = data["name"]
        if not isinstance(name, str) or not name.strip():
            raise ValueError("The 'name' field must be a non-empty string")
        if len(name) > 250:
            raise ValueError("The 'name' field must not exceed 250 characters")
        option.name = name.strip()

    if "session_id" in data:
        session_id = data["session_id"]
        if not isinstance(session_id, int):
            raise ValueError("The 'session_id' field must be an integer")
        option.session_id = session_id

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return OptionResponse.model_validate(option).model_dump()


def delete_option(option_id):
    option = db.session.get(Option, option_id)
    if not option:
        return {"message": "Option not found"}

    db.session.delete(option)

    try:
        db.session.commit()
        return {"message": "Option deleted successfully"}
    except Exception as e:
        db.session.rollback()
        raise e
