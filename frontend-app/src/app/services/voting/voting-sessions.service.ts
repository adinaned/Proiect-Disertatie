import {Injectable} from '@angular/core';
import {Observable, switchMap, forkJoin} from "rxjs";
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

    getProfileStatus(userId: number) {
        return this.http.get<any>(`http://127.0.0.1:5000/profile_statuses/${userId}`);
    }

    getRoleById(roleId: number) {
        return this.http.get<any>(`http://127.0.0.1:5000/roles/${roleId}`);
    }

    deleteVotingSession(votingSessionId: number): Observable<any> {
        return forkJoin([
            this.deleteOptions(votingSessionId),
            this.deletePublicKeys(votingSessionId)
        ]).pipe(
            switchMap(() => this.http.delete(`${this.baseUrl}/voting_sessions/${votingSessionId}`))
        );
    }

    deleteOptions(votingSessionId: number): Observable<any> {
        return this.http.delete(`${this.baseUrl}/options/session/${votingSessionId}`);
    }

    deletePublicKeys(votingSessionId: number): Observable<any> {
        return this.http.delete(`${this.baseUrl}/public_keys/${votingSessionId}`);
    }
}
