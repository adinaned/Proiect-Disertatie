import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable, map} from 'rxjs';

@Injectable({providedIn: 'root'})
export class ViewProfileService {
    private baseUrl = 'http://127.0.0.1:5000';

    constructor(private http: HttpClient) {
    }

    getUserDetails(userId: string): Observable<any> {
        return this.http.get<any>(`${this.baseUrl}/users/${userId}`).pipe(
            map(res => res?.data || '')
        );
    }

    getProfileStatus(userId: string): Observable<any> {
        return this.http.get<any>(`${this.baseUrl}/profile_statuses/${userId}`).pipe(
            map(res => res?.data || '')
        );
    }

    getCountryName(id: string): Observable<string> {
        return this.http.get<any>(`${this.baseUrl}/countries/${id}`).pipe(
            map(res => res?.data.name || '')
        );
    }

    getOrganizationName(id: string): Observable<string> {
        return this.http.get<any>(`${this.baseUrl}/organizations/${id}`).pipe(
            map(res => res?.data.name || '')
        );
    }

    getRoleName(id: string): Observable<string> {
        return this.http.get<any>(`${this.baseUrl}/roles/${id}`).pipe(
            map(res => res?.data.name || '')
        );
    }

    getEmail(userId: string): Observable<any> {
        return this.http.get<any>(`${this.baseUrl}/emails/user/${userId}`).pipe(
            map(res => res?.data || '')
        );
    }
}
