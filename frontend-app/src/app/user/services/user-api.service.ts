import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class UserApiService {
    private baseUrl = 'http://localhost:5000/users';

    constructor(private http: HttpClient) {}

    createUser(data: any): Observable<any> {
        return this.http.post(this.baseUrl, data);
    }

    getUserById(id: number): Observable<any> {
        return this.http.get(`${this.baseUrl}/${id}`);
    }

    updateUser(id: number, data: any): Observable<any> {
        return this.http.put(`${this.baseUrl}/${id}`, data);
    }

    deleteUser(id: number): Observable<any> {
        return this.http.delete(`${this.baseUrl}/${id}`);
    }

    getAllUsers(): Observable<any> {
        return this.http.get(this.baseUrl);
    }
}
