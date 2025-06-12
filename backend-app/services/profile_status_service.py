from datetime import datetime, timezone
import traceback
import uuid

from models import ProfileStatus, db, User
from schemas.profile_status_schema import ProfileStatusResponse

ALLOWED_STATUS_NAMES = {"ACTIVE", "PENDING", "CLOSED", "SUSPENDED"}


def create_profile_status(obj):
    user_id = obj.get("user_id")
    user = db.session.get(User, user_id)
    if not user:
        return {"message": f"User with ID {user_id} does not exist."}

    name = obj.get("name")
    if not isinstance(name, str) or not name.strip():
        return {"message": "The 'name' field must be a non-empty string."}

    allowed = [v.upper() for v in ProfileStatus.__table__.c.name.type.enums]
    name_upper = name.strip().upper()
    if name_upper not in allowed:
        return {"message": f"The 'name' field must be one of {allowed}"}

    existing = db.session.query(ProfileStatus).filter_by(user_id=user_id).first()
    if existing:
        return {"message": f"ProfileStatus already exists for user ID {user_id}."}

    new_status = ProfileStatus(
        name=name_upper,
        user_id=user_id,
        updated_at= obj.get("updated_at")
    )

    return new_status


def get_profile_status_by_user_id(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return {"message": f"User with ID {user_id} does not exist."}

    profile_status = db.session.query(ProfileStatus).filter_by(user_id=user_id).first()
    if not profile_status:
        return {"message": "Failed to find profile status for the specified user."}

    return {
        "message": "Profile status retrieved successfully.",
        "data": ProfileStatusResponse.model_validate(profile_status).model_dump()
    }


def update_profile_status_by_user_id(user_id, data):
    if not isinstance(data, dict) or not data:
        return {"message": "Payload must be a non-empty dictionary."}

    if "id" in data:
        return {"message": "You cannot modify the ID."}

    user = db.session.get(User, user_id)
    if not user:
        return {"message": f"User with ID {user_id} does not exist."}

    profile_status = db.session.query(ProfileStatus).filter_by(user_id=user_id).first()
    if not profile_status:
        return {"message": f"ProfileStatus not found for user ID {user_id}."}

    if "name" in data:
        name = data["name"].upper().strip()
        allowed = [v.upper() for v in ProfileStatus.__table__.c.name.type.enums]
        if name not in allowed:
            return {"message": f"The 'name' field must be one of {allowed}"}
        profile_status.name = name

    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    profile_status.updated_at = datetime.fromisoformat(data["updated_at"])

    db.session.add(profile_status)

    try:
        db.session.commit()
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        return {"message": f"Failed to update profile status: {str(e)}"}

    return {
        "message": "Profile status updated successfully.",
        "data": ProfileStatusResponse.model_validate(profile_status).model_dump()
    }
