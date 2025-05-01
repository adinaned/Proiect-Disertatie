from models import ProfileStatus, db
from schemas.profile_status_schema import ProfileStatusResponse


def create_profile_status(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data:
        raise ValueError("You cannot manually set the ID")

    name = data.get("name")
    updated_at = data.get("updated_at")

    if not name or name not in ProfileStatus.__table__.c.name.type.enums:
        raise ValueError(f"The 'name' field is required and must be one of {ProfileStatus.__table__.c.name.type.enums}")

    profile_status = ProfileStatus(
        name=name,
        updated_at=updated_at
    )

    db.session.add(profile_status)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return ProfileStatusResponse.model_validate(profile_status).model_dump()


def get_profile_status_by_id(profile_status_id):
    profile_status = db.session.get(ProfileStatus, profile_status_id)
    if not profile_status:
        return None

    return ProfileStatusResponse.model_validate(profile_status).model_dump()


def get_all_profile_statuses():
    profile_statuses = ProfileStatus.query.all()
    if not profile_statuses:
        return []

    return [ProfileStatusResponse.model_validate(status).model_dump() for status in profile_statuses]


def update_profile_status(profile_status_id, data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a non-empty dictionary")

    if "id" in data:
        raise ValueError("You cannot modify the ID")

    profile_status = db.session.get(ProfileStatus, profile_status_id)
    if not profile_status:
        raise ValueError("ProfileStatus not found")

    if "name" in data:
        name = data["name"]
        if name not in ProfileStatus.__table__.c.name.type.enums:
            raise ValueError(f"The 'name' field must be one of {ProfileStatus.__table__.c.name.type.enums}")
        profile_status.name = name

    if "updated_at" in data:
        profile_status.updated_at = data["updated_at"]

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return ProfileStatusResponse.model_validate(profile_status).model_dump()


def delete_profile_status(profile_status_id):
    profile_status = db.session.get(ProfileStatus, profile_status_id)
    if not profile_status:
        return {"message": "ProfileStatus not found"}

    db.session.delete(profile_status)

    try:
        db.session.commit()
        return {"message": "ProfileStatus deleted successfully"}
    except Exception as e:
        db.session.rollback()
        raise e
