import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {utils, getPublicKey} from '@noble/secp256k1';

@Injectable({providedIn: 'root'})
export class VoteService {
    private baseUrl = 'http://127.0.0.1:5000';

    constructor(private http: HttpClient) {
    }

    async generateKeypair(): Promise<{ privateKey: string; publicKey: { x: string; y: string } }> {
        const privateKey = utils.randomPrivateKey();
        const publicKey = getPublicKey(privateKey, false);

        return {
            privateKey: this.bytesToHex(privateKey),
            publicKey: {
                x: this.bytesToHex(publicKey.slice(1, 33)),
                y: this.bytesToHex(publicKey.slice(33, 65))
            }
        };
    }

    getEmailObj(email: string): Observable<any> {
        return this.http.get(`${this.baseUrl}/emails/${email}`);
    }

    submitPublicKey(sessionId: number, userId: number, publicKey: { x: string, y: string }) {
        const payload = {
            session_id: sessionId,
            user_id: userId,
            public_key_x: publicKey.x,
            public_key_y: publicKey.y
        };
        console.log(JSON.stringify(payload));
        return this.http.post(`${this.baseUrl}/public-keys`, payload);
    }

    getPublicKey(sessionId: number, userId: number) {
        const url = `${this.baseUrl}/public-keys/${sessionId}/${userId}`;
        console.log("Fetching public key from:", url);

        return this.http.get<{ public_key_x: string, public_key_y: string }>(url);
    }

    getRing(sessionId: number): Observable<{ ring: { x: string, y: string }[] }> {
        const url = `http://127.0.0.1:5000/voting_sessions/${sessionId}/ring`;
        console.log("Fetching ring from:", url);

        return this.http.get<{ ring: { x: string, y: string }[] }>(url);
    }


    submitVote(data: any) {
        return this.http.post(`${this.baseUrl}/votes`, data);
    }

    private bytesToHex(uint8a: Uint8Array): string {
        return Array.from(uint8a)
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
    }
}
