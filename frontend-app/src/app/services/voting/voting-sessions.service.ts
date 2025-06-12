import {Injectable} from '@angular/core';
import {Observable, switchMap, forkJoin, map} from "rxjs";
import {HttpClient} from '@angular/common/http';

@Injectable({providedIn: 'root'})
export class VotingSessionsService {
    private baseUrl = 'http://127.0.0.1:5000';

    constructor(private http: HttpClient) {
    }

    getVotingSessionsByOrganization(organizationId: string): Observable<any[]> {
        return this.http.get<any>(`${this.baseUrl}/voting_sessions/organization/${organizationId}`).pipe(
            map(res => res.data)
        );
    }

    getVotingSessionsByOrganizationAndRole(organizationId: string, roleId: string): Observable<any[]> {
        return this.http.get<any>(`${this.baseUrl}/voting_sessions/organization/${organizationId}/role/${roleId}`).pipe(
            map(res => res.data)
        );
    }

    getUserIdByEmail(email: string) {
        return this.http.get<any>(`${this.baseUrl}/emails/${email}`).pipe(
            map(res => res.data)
        )
    }

    getProfileStatus(userId: number) {
        return this.http.get<any>(`${this.baseUrl}/profile_statuses/${userId}`).pipe(
            map(res => res.data)
        )
    }

    deleteVotingSession(votingSessionId: number): Observable<any> {
        return forkJoin([
            this.deleteOptions(votingSessionId),
            this.deletePublicKeys(votingSessionId)
        ]).pipe(
            switchMap(() => this.http.delete(`${this.baseUrl}/voting_sessions/${votingSessionId}`))
        );
    }

    deleteOptions(votingSessionId: number) {
        return this.http.delete<any>(`${this.baseUrl}/options/voting_session/${votingSessionId}`).pipe(
            map(res => res.data)
        )
    }

    deletePublicKeys(votingSessionId: number) {
        return this.http.delete<any>(`${this.baseUrl}/public_keys/voting_session/${votingSessionId}`).pipe(
            map(res => res.data)
        )
    }
}
