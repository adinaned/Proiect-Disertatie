import {Injectable} from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from '@angular/common/http';
import {VoteService} from "./votes/vote.service";

@Injectable({providedIn: 'root'})
export class VotingSessionFormService {
    private baseUrl = 'http://127.0.0.1:5000';

    constructor(private http: HttpClient, private voteService: VoteService) {
    }

    getSessionById(id: number): Observable<any> {
        return this.http.get(`${this.baseUrl}/voting_sessions/${id}`);
    }

    getOptionsBySessionId(session_id: number): Observable<any> {
        return this.http.get(`${this.baseUrl}/options/session/${session_id}`);
    }
}
