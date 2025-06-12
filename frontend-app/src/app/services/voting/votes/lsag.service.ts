import {Injectable} from '@angular/core';
import {sha3_256} from '@noble/hashes/sha3';
import {ProjectivePoint, CURVE, utils, getPublicKey} from '@noble/secp256k1';
import {bytesToHex} from '@noble/hashes/utils';

@Injectable({providedIn: 'root'})
export class LsagService {
    private ORDER = CURVE.n;
    private G = ProjectivePoint.BASE;
    private encoder = new TextEncoder();

    async generateKeypair(): Promise<{ privateKey: bigint; publicKey: { x: bigint; y: bigint } }> {
        const privateKeyBytes = utils.randomPrivateKey();
        const privateKey = BigInt('0x' + bytesToHex(privateKeyBytes));
        const pubBytes = getPublicKey(privateKeyBytes, false);

        const x = BigInt('0x' + bytesToHex(pubBytes.slice(1, 33)));
        const y = BigInt('0x' + bytesToHex(pubBytes.slice(33, 65)));

        return {
            privateKey,
            publicKey: {x, y}
        };
    }

    async generateLSAGSignature(
        message: string,
        ring: { x: bigint; y: bigint }[],
        voterIndex: number,
        privateKey: bigint
    ): Promise<any> {
        const n = ring.length;
        const ringPoints = ring.map(p => new ProjectivePoint(BigInt(p.x), BigInt(p.y), 1n));
        const Hp = this.hashPoint(ringPoints[voterIndex]);
        const I = Hp.multiply(privateKey);

        const c: bigint[] = new Array(n).fill(0n);
        const r: bigint[] = new Array(n).fill(0n);

        const u = this.getRandomScalar(this.ORDER);
        const L = this.G.multiply(u);
        const R = Hp.multiply(u);

        c[(voterIndex + 1) % n] = this.hashAll(message, L, R);

        let i = (voterIndex + 1) % n;
        while (i !== voterIndex) {
            r[i] = this.getRandomScalar(this.ORDER);
            const L_i = this.G.multiply(r[i]).add(ringPoints[i].multiply(c[i]));
            const R_i = this.hashPoint(ringPoints[i]).multiply(r[i]).add(I.multiply(c[i]));
            c[(i + 1) % n] = this.hashAll(message, L_i, R_i);
            i = (i + 1) % n;
        }

        r[voterIndex] = (u - privateKey * c[voterIndex]) % this.ORDER;
        if (r[voterIndex] < 0n) {
            r[voterIndex] += this.ORDER;
        }

        return {
            ring: ring.map(p => ({x: p.x.toString(), y: p.y.toString()})),
            I: {x: I.x.toString(), y: I.y.toString()},
            c0: c[0].toString(),
            r: r.map(val => val.toString())
        };
    }

    generateKeyImage(publicKey: { x: bigint; y: bigint }, privateKey: bigint): { x: string; y: string } {
        const point = new ProjectivePoint(publicKey.x, publicKey.y, 1n);
        const Hp = this.hashPoint(point);
        const I = Hp.multiply(privateKey);
        return {
            x: I.x.toString(),
            y: I.y.toString()
        };
    }

    private hashPoint(P: ProjectivePoint): ProjectivePoint {
        const data = new Uint8Array([
            ...this.toBytes32(P.x),
            ...this.toBytes32(P.y),
        ]);
        const hash = sha3_256(data);
        const scalar = BigInt('0x' + bytesToHex(hash)) % this.ORDER;
        return this.G.multiply(scalar);
    }

    private hashAll(message: string, L: ProjectivePoint, R: ProjectivePoint): bigint {
        const lAffine = L.toAffine();
        const rAffine = R.toAffine();
        const data: Uint8Array = new Uint8Array([
            ...this.encoder.encode(message),
            ...this.toBytes32(lAffine.x),
            ...this.toBytes32(lAffine.y),
            ...this.toBytes32(rAffine.x),
            ...this.toBytes32(rAffine.y),
        ]);
        const hashBytes = sha3_256(data);
        return BigInt('0x' + bytesToHex(hashBytes)) % this.ORDER;
    }

    private toBytes32(n: bigint): Uint8Array {
        const hex = n.toString(16).padStart(64, '0');
        const bytes = new Uint8Array(32);
        for (let i = 0; i < 32; i++) {
            bytes[i] = parseInt(hex.substring(i * 2, i * 2 + 2), 16);
        }
        return bytes;
    }

    private bytesToHex(uint8a: Uint8Array): string {
        return Array.from(uint8a).map(b => b.toString(16).padStart(2, '0')).join('');
    }

    private getRandomScalar(order: bigint): bigint {
        while (true) {
            const bytes = utils.randomPrivateKey();
            const num = BigInt('0x' + bytesToHex(bytes));
            if (num > 0n && num < order) {
                return num;
            }
        }
    }
}