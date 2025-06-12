import {Injectable} from '@angular/core';
import {map, Observable} from "rxjs";
import {HttpClient} from '@angular/common/http';
import {VoteService} from "./votes/vote.service";

@Injectable({providedIn: 'root'})
export class VotingSessionFormService {
    private baseUrl = 'http://127.0.0.1:5000';

    constructor(private http: HttpClient, private voteService: VoteService) {
    }

    getSessionById(id: string): any {
        return this.http.get<any>(`${this.baseUrl}/voting_sessions/${id}`).pipe(
            map(res => res.data)
        );
    }

    getOptionsByVotingSessionId(session_id: string): Observable<any> {
        return this.http.get(`${this.baseUrl}/options/voting_session/${session_id}`);
    }
}
