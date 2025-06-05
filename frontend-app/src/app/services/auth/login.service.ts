import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';

@Injectable({providedIn: 'root'})
export class LoginService {
    private baseUrl = 'http://127.0.0.1:5000';

    constructor(private http: HttpClient) {
    }

    loginUser(data: { email: string; password: string }): Observable<any> {
        return this.http.post(`${this.baseUrl}/login`, data);
    }
}
