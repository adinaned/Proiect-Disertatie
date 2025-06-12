from models import VotingSessionRegistration, db
from sqlalchemy.exc import SQLAlchemyError


def create_registration(voting_session_id, user_id):
    existing = VotingSessionRegistration.query.filter_by(
        voting_session_id=voting_session_id,
        user_id=user_id
    ).first()

    if existing:
        return {"message": "User already registered for this session."}, 409

    try:
        new_registration = VotingSessionRegistration(
            voting_session_id=voting_session_id,
            user_id=user_id
        )
        db.session.add(new_registration)
        db.session.commit()
        return {"message": "Registration created successfully.", "data": new_registration.to_dict()}, 201
    except SQLAlchemyError:
        db.session.rollback()
        raise


def get_registration_by_voting_session_id_and_user_id(voting_session_id, user_id):
    registration = VotingSessionRegistration.query.filter_by(
        voting_session_id=voting_session_id,
        user_id=user_id
    ).first()

    if registration:
        return {"message": "Registration found.", "data": registration.to_dict()}, 200
    return {"message": "Registration not found.", "data": None}, 404


def get_all_registrations_by_voting_session_id(voting_session_id):
    registrations = VotingSessionRegistration.query.filter_by(
        voting_session_id=voting_session_id
    ).all()

    data = [r.to_dict() for r in registrations]
    return {"message": "Registrations retrieved successfully.", "data": data}, 200
