from models import Option, VotingSession, db
from schemas.option_schema import OptionResponse

def create_option(data, voting_session_id):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object.")

    if "id" in data:
        raise ValueError("You cannot manually set the ID.")

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("The 'name' field is required and must be a non-empty string.")
    if len(name.strip()) > 250:
        raise ValueError("The 'name' field must not exceed 250 characters.")
    if len(name.strip()) < 3:
        raise ValueError("The 'name' field must have at least 3 characters.")

    voting_session = db.session.get(VotingSession, voting_session_id)
    if not voting_session:
        raise ValueError(f"Voting session with id '{voting_session_id}' does not exist.")

    option = Option(
        name=name.strip(),
        voting_session_id=voting_session_id
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


def get_all_options_by_session_id(voting_session_id):
    options = Option.query.filter_by(voting_session_id=voting_session_id).all()
    if not options:
        return []

    return [OptionResponse.model_validate(option).model_dump() for option in options]


def update_option(option_id, data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a non-empty dictionary")

    if "id" in data:
        raise ValueError("You cannot modify the ID")

    if "voting_session_id" in data:
        raise ValueError("You are not allowed to modify 'voting_session_id'")

    option = db.session.get(Option, option_id)
    if not option:
        raise ValueError("Option not found")

    if "name" in data:
        name = data["name"].strip()
        if not name:
            raise ValueError("The 'name' field must be a non-empty string")
        if len(name) > 250:
            raise ValueError("The 'name' field must not exceed 250 characters")
        if len(name) < 3:
            raise ValueError("The 'name' field must have at least 3 characters")

        if name == option.name:
            raise ValueError("You cannot update the option with the same name it already has.")

        option.name = name

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


def delete_all_options_by_session_id(voting_session_id):
    options = Option.query.filter_by(voting_session_id=voting_session_id).all()
    if not options:
        return {"message": "Options not found"}

    for option in options:
        db.session.delete(option)

    try:
        db.session.commit()
        return [OptionResponse.model_validate(option).model_dump() for option in options]
    except Exception as e:
        db.session.rollback()
        raise e
