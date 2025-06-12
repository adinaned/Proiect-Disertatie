import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {map, Observable} from 'rxjs';

@Injectable({providedIn: 'root'})
export class VotingSessionService {
    private apiUrl = 'http://127.0.0.1:5000';

    constructor(private http: HttpClient) {
    }

    getRolesByOrganizationId(organizationId: string): Observable<any[]> {
        return this.http.get<any>(`${this.apiUrl}/roles/organization/${organizationId}`).pipe(
            map(res => res.data)
        )
    }

    createVotingSession(payload: any): Observable<any> {
        return this.http.post<any>(`${this.apiUrl}/voting_sessions`, payload).pipe(
            map(res => res.data)
        )
    }

    createOption(sessionId: number, option: any): Observable<any> {
        return this.http.post<any>(`${this.apiUrl}/options/${sessionId}`, option).pipe(
            map(res => res.data)
        )
    }
}
