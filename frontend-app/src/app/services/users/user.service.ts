import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {map, Observable} from 'rxjs';


@Injectable({providedIn: 'root'})
export class UserService {
    constructor(private http: HttpClient) {
    }

    private baseUrl = 'http://127.0.0.1:5000';

    getUsersByOrganizationId(organizationId: string) {
        return this.http.get<any>(`${this.baseUrl}/users/organization/${organizationId}`).pipe(
            map(res => res.data)
        )
    }

    getProfileStatuses(userId: string): Observable<any> {
        return this.http.get<any>(`${this.baseUrl}/profile_statuses/${userId}`);
    }

    getRoleById(roleId: string) {
        return this.http.get<any>(`${this.baseUrl}/roles/${roleId}`).pipe(
            map(res => res.data)
        )
    }

    getUserById(userId: string) {
        return this.http.get<any>(`${this.baseUrl}/users/${userId}`).pipe(
            map(res => res.data)
        )
    }

    getRolesByOrganizationId(organizationId: string) {
        return this.http.get<any>(`${this.baseUrl}/roles/organization/${organizationId}`).pipe(
            map(res => res?.data)
        );
    }

    getEmail(userId: string): Observable<any> {
        return this.http.get<any>(`${this.baseUrl}/emails/user/${userId}`).pipe(
            map(res => res?.data || '')
        );
    }
}
