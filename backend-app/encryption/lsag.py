import hashlib
import json
from typing import Dict
from ecdsa import SECP256k1, ellipticcurve

from models import db, PublicKey, VotingSession

CURVE = SECP256k1
ORDER = CURVE.order
G = CURVE.generator


def int_from_hash(data: bytes) -> int:
    return int.from_bytes(hashlib.sha3_256(data).digest(), "big") % ORDER


def hash_point(P: ellipticcurve.Point) -> ellipticcurve.Point:
    return int_from_hash(P.x().to_bytes(32, "big") + P.y().to_bytes(32, "big")) * G


def generate_ring(session_id: int, *_):
    print(f"Generating ring for session {session_id}")
    session = db.session.query(VotingSession).filter_by(id=session_id).first()
    if not session:
        raise ValueError("Voting session not found")

    public_keys = db.session.query(PublicKey.public_key_x, PublicKey.public_key_y). \
        filter(PublicKey.session_id == session_id).all()

    ring = {"ring": [{"x": x, "y": y} for i, (x, y) in enumerate(public_keys)]}
    return ring

def lsag_verify(message: bytes, sig: Dict) -> bool:
    ring = [
        ellipticcurve.Point(CURVE.curve, int(xy["x"], 16), int(xy["y"], 16))
        for xy in sig["ring"]
    ]
    n = len(ring)
    I = ellipticcurve.Point(CURVE.curve, int(sig["I"]["x"], 16), int(sig["I"]["y"], 16))
    if I == ellipticcurve.INFINITY:
        return False

    c = [0] * (n + 1)
    c[0] = sig["c0"]
    r = sig["r"]

    for i in range(n):
        L_i = r[i] * G + c[i] * ring[i]
        R_i = r[i] * hash_point(ring[i]) + c[i] * I
        c[i + 1] = int_from_hash(
            message +
            L_i.x().to_bytes(32, "big") + L_i.y().to_bytes(32, "big") +
            R_i.x().to_bytes(32, "big") + R_i.y().to_bytes(32, "big")
        )
    return c[0] == c[n]

def calculate_ring_hash(session_id) -> str:
    voting_session = db.session.query(VotingSession).filter_by(id=session_id).first()
    ring = voting_session.key_ring

    sorted_ring = sorted(ring)
    ring_json = json.dumps(sorted_ring, separators=(',', ':'), sort_keys=True)
    return hashlib.sha256(ring_json.encode()).hexdigest()
