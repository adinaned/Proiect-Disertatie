import {Injectable} from '@angular/core';
import {sha256} from '@noble/hashes/sha256';
import {ProjectivePoint, CURVE, utils} from '@noble/secp256k1';
import {bytesToHex} from '@noble/hashes/utils';


@Injectable({providedIn: 'root'})
export class LsagService {
    private ORDER = CURVE.n;
    private G = ProjectivePoint.BASE;

    async generateLSAGSignature(
        message: string,
        ring: { x: string; y: string }[],
        voterIndex: number,
        privateKeyHex: string
    ): Promise<any> {
        const ringPoints = ring.map(p =>
            new ProjectivePoint(BigInt("0x" + p.x), BigInt("0x" + p.y), 1n)
        );
        const Hp = this.hashPoint(ringPoints[voterIndex]);
        const sk = BigInt('0x' + privateKeyHex);
        const I = Hp.multiply(sk);

        const c: bigint[] = new Array(ring.length).fill(0n);
        const r: bigint[] = new Array(ring.length).fill(0n);

        const uBytes = utils.randomPrivateKey();
        const u = BigInt('0x' + bytesToHex(uBytes));

        const L = this.G.multiply(u);
        const R = Hp.multiply(u);

        c[(voterIndex + 1) % ring.length] = this.hashAll(message, L, R);

        let i = (voterIndex + 1) % ring.length;
        while (i !== voterIndex) {
            const riBytes = utils.randomPrivateKey();
            r[i] = BigInt('0x' + bytesToHex(riBytes));

            const L_i = this.G.multiply(r[i]).add(ringPoints[i].multiply(c[i]));
            const R_i = this.hashPoint(ringPoints[i]).multiply(r[i]).add(I.multiply(c[i]));

            c[(i + 1) % ring.length] = this.hashAll(message, L_i, R_i);
            i = (i + 1) % ring.length;
        }

        r[voterIndex] = (u - sk * c[voterIndex]) % this.ORDER;
        if (r[voterIndex] < 0n) {
            r[voterIndex] += this.ORDER;
        }

        return {
            ring,
            I: {x: I.x.toString(), y: I.y.toString()},
            c0: c[0].toString(),
            r: r.map(v => v.toString())
        };
    }

    generateKeyImage(publicKey: { x: string; y: string }, privateKeyHex: string): { x: string; y: string } {
        const point = new ProjectivePoint(BigInt("0x" + publicKey.x), BigInt("0x" + publicKey.y), 1n);
        const Hp = this.hashPoint(point);
        const sk = BigInt('0x' + privateKeyHex);
        const I = Hp.multiply(sk);
        return {
            x: I.x.toString(),
            y: I.y.toString()
        };
    }

    private hashPoint(P: ProjectivePoint): ProjectivePoint {
        const data = this.textToBytes(P.x.toString() + P.y.toString());
        const hash = sha256(data);
        const scalar = BigInt('0x' + bytesToHex(hash)) % this.ORDER;
        return this.G.multiply(scalar);
    }

    private hashAll(message: string, L: ProjectivePoint, R: ProjectivePoint): bigint {
        const input = message + L.x.toString() + L.y.toString() + R.x.toString() + R.y.toString();
        const data = this.textToBytes(input);
        const hash = sha256(data);
        return BigInt('0x' + bytesToHex(hash)) % this.ORDER;
    }

    private textToBytes(text: string): Uint8Array {
        return new TextEncoder().encode(text);
    }
}
