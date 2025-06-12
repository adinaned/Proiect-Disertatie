import {HttpClient, HttpResponse} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {map, Observable} from 'rxjs';
import {utils, getPublicKey} from '@noble/secp256k1';

@Injectable({providedIn: 'root'})
export class VoteService {
    private baseUrl = 'http://127.0.0.1:5000';

    constructor(private http: HttpClient) {
    }

    getEmailObj(email: string): Observable<any> {
        return this.http.get(`${this.baseUrl}/emails/${email}`);
    }

    getPublicKey(votingSessionId: string, userId: boolean) {
        const url = `${this.baseUrl}/public_keys/${votingSessionId}/${userId}`;
        console.log("Fetching public key from:", url);

        return this.http.get<any>(url);
    }

    submitPublicKey(votingSessionId: string, userId: string, publicKey: { x: bigint; y: bigint }) {
        const payload = {
            voting_session_id: votingSessionId,
            user_id: userId,
            public_key_x: publicKey.x.toString(),
            public_key_y: publicKey.y.toString()
        };
        console.log(JSON.stringify(payload));
        return this.http.post(`${this.baseUrl}/public_keys`, payload);
    }

    checkIfRegistered(sessionId: string, userId: string): Observable<HttpResponse<any>> {
        return this.http.get<any>(
            `${this.baseUrl}/voting_session_registrations/voting_session/${sessionId}/user/${userId}`,
            {observe: 'response'}
        );
    }

    getRing(votingSessionId: string): Observable<{ x: bigint, y: bigint }[]> {
        const url = `http://127.0.0.1:5000/voting_sessions/${votingSessionId}/ring`;
        console.log("Fetching ring from:", url);

        return this.http.get<any>(url).pipe(
            map((res: { data: { ring: any; }; }) => res?.data?.ring || [])
        );
    }

    submitVote(data: any) {
        return this.http.post(`${this.baseUrl}/votes`, data);
    }
}
