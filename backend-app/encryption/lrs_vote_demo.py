
"""
Electronic voting with Linkable Ring Signatures (LSAG).

Install reqs:
    pip install ecdsa safe-pysha3 tabulate
"""

import json
import secrets
import hashlib
from typing import List, Dict, Tuple
from collections import Counter
from pprint import pprint

from ecdsa import SECP256k1, ellipticcurve

# --- primitive LSAG  ---------------------------------------------------- #

CURVE = SECP256k1
ORDER = CURVE.order
G = CURVE.generator


def int_from_hash(data: bytes) -> int:
    return int.from_bytes(hashlib.sha3_256(data).digest(), "big") % ORDER


def hash_point(P: ellipticcurve.Point) -> ellipticcurve.Point:
    return int_from_hash(P.x().to_bytes(32, "big") + P.y().to_bytes(32, "big")) * G


def generate_keypair() -> Tuple[int, ellipticcurve.Point]:
    sk = secrets.randbelow(ORDER - 1) + 1
    return sk, sk * G


def lsag_sign(message: bytes,
              ring: List[ellipticcurve.Point],
              idx: int,
              sk: int) -> Dict:
    n = len(ring)
    Hp = hash_point(ring[idx])
    I = sk * Hp

    c = [0] * n
    r = [0] * n
    u = secrets.randbelow(ORDER - 1) + 1

    L = u * G
    R = u * Hp
    c[(idx + 1) % n] = int_from_hash(message +
                                     L.x().to_bytes(32, "big") + L.y().to_bytes(32, "big") +
                                     R.x().to_bytes(32, "big") + R.y().to_bytes(32, "big"))

    i = (idx + 1) % n
    while i != idx:
        r[i] = secrets.randbelow(ORDER - 1) + 1
        L_i = r[i] * G + c[i] * ring[i]
        R_i = r[i] * hash_point(ring[i]) + c[i] * I
        c[(i + 1) % n] = int_from_hash(message +
                                       L_i.x().to_bytes(32, "big") + L_i.y().to_bytes(32, "big") +
                                       R_i.x().to_bytes(32, "big") + R_i.y().to_bytes(32, "big"))
        i = (i + 1) % n

    r[idx] = (u - sk * c[idx]) % ORDER
    return {
        "ring": [(p.x(), p.y()) for p in ring],
        "I": (I.x(), I.y()),
        "c0": c[0],
        "r": r
    }


def lsag_verify(message: bytes, sig: Dict) -> bool:
#     sig = {'I': {'x': '13074389284528552511323402285338647667276661254149489160244677146697334805898',
#        'y': '43842792868475735203114913418711184162033742245500893998593039105223159977367'},
#  'c0': '84628952480769556656275757576152692311422543572798594847116689666615585425986',
#  'r': ['54804158747106022665663901256205797586273591240588263757605645519716278440826',
#        '65498998110329175093637795530584705046196389618318140959749441558081408175026'],
#  'ring': [{'x': '750216288340211c9f207001389753bfb9dee9596f0a50b610f8eec508e53140',
#            'y': '3e04f601cda7009a506cbdb8bcb692b623924a69e3e9ae9f89753163d7754a91'},
#           {'x': 'bf3c38458bb84baf6ccdc689bd70209023208d0bdd2f9616e283baacde5297d8',
#            'y': '446be6d4dc9e3fa1f63def0f756cc057a6d35ef7d39c59cb8f52a16fa0cab05a'}]}

    print("Verifying LSAG signature...")
    pprint(sig)
    ring = [ellipticcurve.Point(CURVE.curve, *xy) for xy in sig["ring"]]
    n = len(ring)
    I = ellipticcurve.Point(CURVE.curve, *sig["I"])
    if I == ellipticcurve.INFINITY:
        return False

    c = [0] * (n + 1)
    c[0] = sig["c0"]
    r = sig["r"]

    for i in range(n):
        L_i = r[i] * G + c[i] * ring[i]
        R_i = r[i] * hash_point(ring[i]) + c[i] * I
        c[i + 1] = int_from_hash(message +
                                 L_i.x().to_bytes(32, "big") + L_i.y().to_bytes(32, "big") +
                                 R_i.x().to_bytes(32, "big") + R_i.y().to_bytes(32, "big"))
    return c[0] == c[n]


# ---  sistem de vot ---------------------------------------------------- #

class ElectionSystem:

    def __init__(self, election_id: str, candidates: Dict[int, str]):
        self.election_id = election_id # id-ul sesiunii de vot
        self.candidates = candidates # dictionar de candidati cu id si nume
        self._voters: Dict[str, Tuple[int, ellipticcurve.Point]] = {} # votantii au un dictionar cu numele lor si cheile lor
        self._votes: List[Tuple[int, Dict]] = [] # lista de voturi
        self._seen_imgs: set = set() # set de chei de imagine pentru voturi
        self.closed = False # flag pentru a verifica daca sesiunea de vot este inchisa

    # Inregistrare votant
    def register_voter(self, voter_id: str) -> Tuple[int, ellipticcurve.Point]: # returneaza un tuplu cu cheia privata si publica
        if voter_id in self._voters: # verificam daca votantul este deja inregistrat
            raise ValueError("already registered")
        sk, pk = generate_keypair() # generam o pereche de chei in cazul in care nu este inregistrat votantul
        self._voters[voter_id] = (sk, pk) # adaugam votantul in dictionar
        return sk, pk

    # Manifest
    @property
    def manifest(self) -> Dict:
        pks = [(pk.x(), pk.y()) for (_, pk) in self._voters.values()]
        return {
            "election_id": self.election_id,
            "candidates": self.candidates,
            "pubkeys": pks,
            "pubkeys_sha256": hashlib.sha256(json.dumps(pks, sort_keys=True).encode()).hexdigest()
        }

    def _message(self, candidate_id: int) -> bytes:
        return f"{self.election_id}|{candidate_id}".encode()

    # Votare
    def submit_vote(self, candidate_id: int, sig: Dict):
        if self.closed:
            raise RuntimeError("poll closed")
        if candidate_id not in self.candidates:
            raise ValueError("bad candidate")

        if not lsag_verify(self._message(candidate_id), sig):
            raise ValueError("invalid signature")

        img_key = json.dumps(sig["I"]).encode()
        if img_key in self._seen_imgs:
            raise ValueError("duplicate vote")
        self._seen_imgs.add(img_key)
        self._votes.append((candidate_id, sig))

    def close_poll(self):
        self.closed = True

    def tally(self) -> Counter:
        if not self.closed:
            raise RuntimeError("poll not closed")
        return Counter(cid for (cid, _) in self._votes)


# --- votant (parte de client) ------------------------------------------------------- #

class Voter:
    def __init__(self, system: ElectionSystem, sk: int, pk: ellipticcurve.Point):
        self.sys = system # sistemul de vot
        self.sk = sk # cheia privata
        self.pk = pk # cheia publica
        # pprint("Voter public key:", pk)
        self.ring = [ellipticcurve.Point(CURVE.curve, *xy) for xy in system.manifest["pubkeys"]] # lista de chei publice a votantilor
        # xy sunt coordonatele punctului de pe curba eliptica

        self.idx = self.ring.index(self.pk) # indexul votantului in lista de chei publice

    def vote(self, candidate_id: int):
        sig = lsag_sign(self.sys._message(candidate_id), self.ring, self.idx, self.sk) # semnatura votului
        self.sys.submit_vote(candidate_id, sig) # trimitem votul la sistemul de vot


# --- Demo --------------------------------------------------------------- #

def main():
    from tabulate import tabulate # for pretty printing

    es = ElectionSystem("Referendum2025", {1: "Da", 2: "Nu"}) # id-ul sesiunii de vot + optiune cu id si numele optiunii
    # Inregistrare votanti
    voters = {} # dictionar de votanti
    for uid in ["ion", "maria", "paul"]: # luam toti votantii la rand
        voters[uid] = es.register_voter(uid) # inregistram votantii

    # Votare
    choices = {"ion": 1, "maria": 2, "paul": 1} # dictionar in care fiecare din votanti isi exprima alegerea
    for uid, cand in choices.items(): # luam fiecare votant si alegerea lui
        sk, pk = voters[uid] # luam cheia privata si publica a votantului
        print("Voter public key:", pk.x(), pk.y())
        print("Voter private key:", sk)
        Voter(es, sk, pk).vote(cand) # votam si semnam votul
        print(f"{uid} voted")

    # Incercare de vot dublu
    try:
        sk, pk = voters["ion"]
        Voter(es, sk, pk).vote(1)
    except ValueError as e:
        print("duplicate vote blocked:", e)

    # Inchide si numara voturi
    es.close_poll()
    res = es.tally()
    print("\nRezultat final:")
    print(tabulate([(es.candidates[k], res[k]) for k in es.candidates],
                   headers=["Optiune", "Voturi"]))



if __name__ == "__main__":
    main()
    # lsag_verify(message ="random", sig={})