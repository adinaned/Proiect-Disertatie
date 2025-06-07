import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';


@Injectable({providedIn: 'root'})
export class UserService {
    constructor(private http: HttpClient) {
    }

    private baseUrl = 'http://127.0.0.1:5000';

    getUsers(): Observable<any[]> {
        return this.http.get<any[]>(`${this.baseUrl}/users`);
    }

    getRoles(): Observable<any[]> {
        return this.http.get<any[]>(`${this.baseUrl}/roles`);
    }

    getProfileStatuses(userId: number): Observable<any> {
        return this.http.get<any>(`${this.baseUrl}/profile_statuses/${userId}`);
    }
}
