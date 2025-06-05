from models import PublicKey, VotingSession, db
from schemas.public_key_schema import PublicKeyResponse
from exceptions import PublicKeyAlreadyExists
from encryption.lsag import generate_ring


def create_public_key(data):
    session_id = data.get("session_id")
    user_id = data.get("user_id")

    # existing = PublicKey.query.filter_by(session_id=session_id, user_id=user_id).first()
    # if existing:
    #     raise PublicKeyAlreadyExists("Key already exists for this user/session")

    public_key_x = data.get("public_key_x")
    public_key_y = data.get("public_key_y")

    public_key = PublicKey(
        session_id=session_id,
        user_id=user_id,
        public_key_x=public_key_x,
        public_key_y=public_key_y
    )

    db.session.add(public_key)
    db.session.commit()

    session = db.session.query(VotingSession).filter_by(id=session_id).first()
    if not session:
        raise ValueError("Voting session not found")

    generate_ring(session_id, session.role_id, session.organization_id)

    return PublicKeyResponse.model_validate(public_key).model_dump()


def get_public_key_by_session_id_and_user_id(session_id, user_id):
    public_key = db.session.query(PublicKey).filter_by(
        session_id=session_id,
        user_id=user_id
    ).first()

    if not public_key:
        return None

    return PublicKeyResponse.model_validate(public_key).model_dump()
