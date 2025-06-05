import {Injectable} from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from '@angular/common/http';

@Injectable({providedIn: 'root'})
export class VotingSessionsService {
    private baseUrl = 'http://127.0.0.1:5000';

    constructor(private http: HttpClient) {
    }

    getAllVotingSessions(): Observable<any> {
        return this.http.get(`${this.baseUrl}/voting_sessions`);
    }

    getUserIdByEmail(email: string) {
        return this.http.get<any>(`http://127.0.0.1:5000/emails/${email}`);
    }

    getUserById(userId: number) {
        return this.http.get<any>(`http://127.0.0.1:5000/users/${userId}`);
    }

    getRoleById(roleId: number) {
        return this.http.get<any>(`http://127.0.0.1:5000/roles/${roleId}`);
    }

    deleteVotingSession(votingSessionId: number): Observable<any> {
        this.deleteOptions(votingSessionId);
        return this.http.delete(`${this.baseUrl}/voting_sessions/${votingSessionId}`);
    }

    deleteOptions(votingSessionId: number): Observable<any> {
        return this.http.delete(`${this.baseUrl}/options/${votingSessionId}`);
    }
}
