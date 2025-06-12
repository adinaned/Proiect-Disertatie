import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Injectable({providedIn: 'root'})
export class LoginService {
    private baseUrl = 'http://127.0.0.1:5000';

    constructor(private http: HttpClient) {
    }

    loginUser(credentials: { email_address: string; password: string }) {
        return this.http.post(`${this.baseUrl}/login`, credentials, {withCredentials: true});
    }

    getCurrentUser() {
        return this.http.get(`${this.baseUrl}/me`, {withCredentials: true});
    }
}
