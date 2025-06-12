from models import PublicKey, VotingSession, db
from schemas.public_key_schema import PublicKeyResponse
# from exceptions import PublicKeyAlreadyExists
from encryption.lsag import generate_ring


def create_public_key(data):
    voting_session_id = data.get("voting_session_id")
    print(voting_session_id)

    session = db.session.query(VotingSession).filter_by(id=voting_session_id).first()
    if not session:
        raise ValueError("Voting session not found")

    user_id = data.get("user_id")
    public_key_x = data.get("public_key_x")
    public_key_y = data.get("public_key_y")

    public_key = PublicKey(
        voting_session_id=voting_session_id,
        public_key_x=public_key_x,
        public_key_y=public_key_y
    )

    db.session.add(public_key)
    db.session.commit()

    from services import create_registration
    create_registration(voting_session_id, user_id)
    generate_ring(voting_session_id, session.role_id, session.organization_id)

    return PublicKeyResponse.model_validate(public_key).model_dump()


def get_public_key_by_session_id(voting_session_id):
    public_key = db.session.query(PublicKey).filter_by(
        voting_session_id=voting_session_id,
    ).first()

    if not public_key:
        return None

    return PublicKeyResponse.model_validate(public_key).model_dump()
