import hashlib
import json
from typing import Dict
from ecdsa import SECP256k1, ellipticcurve

from models import db, PublicKey, VotingSession

CURVE = SECP256k1
ORDER = CURVE.order
G = CURVE.generator


def int_from_hash(data: bytes) -> int:
    return int.from_bytes(hashlib.sha256(data).digest(), "big") % ORDER


def hash_point(P: ellipticcurve.Point) -> ellipticcurve.Point:
    return int_from_hash(P.x().to_bytes(32, "big") + P.y().to_bytes(32, "big")) * G


def generate_ring(voting_session_id: int, *_):
    print(f"Generating ring for session {voting_session_id}")
    session = db.session.query(VotingSession).filter_by(id=voting_session_id).first()
    if not session:
        raise ValueError("Voting session not found")

    public_keys = db.session.query(PublicKey.public_key_x, PublicKey.public_key_y). \
        filter(PublicKey.voting_session_id == voting_session_id).all()

    ring = {"ring": [{"x": x, "y": y} for i, (x, y) in enumerate(public_keys)]}
    return ring


def lsag_verify(message: bytes, sig: Dict) -> bool:
    from pprint import pprint
    pprint(message)
    pprint(sig)
    ring = [
        ellipticcurve.Point(CURVE.curve, int(xy["x"]), int(xy["y"]))
        for xy in sig["ring"]
    ]
    n = len(ring)
    I = ellipticcurve.Point(CURVE.curve, int(sig["I"]["x"]), int(sig["I"]["y"]))
    if I == ellipticcurve.INFINITY:
        return False

    r = [int(x) for x in sig["r"]]
    c = [None] * (n + 1)
    c[0] = int(sig["c0"])

    for i in range(n):
        Hp = hash_point(ring[i])
        L_i = r[i] * G + c[i] * ring[i]
        R_i = r[i] * Hp + c[i] * I
        c[i + 1] = int_from_hash(
            message +
            L_i.x().to_bytes(32, "big") + L_i.y().to_bytes(32, "big") +
            R_i.x().to_bytes(32, "big") + R_i.y().to_bytes(32, "big")
        )

    return c[0] == c[n]


def calculate_ring_hash(voting_session_id) -> str:
    voting_session = db.session.query(VotingSession).filter_by(id=voting_session_id).first()
    ring = voting_session.key_ring

    sorted_ring = sorted(ring)
    ring_json = json.dumps(sorted_ring, separators=(',', ':'), sort_keys=True)
    return hashlib.sha256(ring_json.encode()).hexdigest()
