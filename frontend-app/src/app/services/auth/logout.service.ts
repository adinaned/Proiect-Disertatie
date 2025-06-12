import {Injectable} from '@angular/core';
import {Router} from '@angular/router';
import {HttpClient} from "@angular/common/http";

import {AuthService} from "./auth.service";

@Injectable({providedIn: 'root'})
export class LogoutService {
    private baseUrl = 'http://127.0.0.1:5000';

    constructor(private router: Router,
                private http: HttpClient,
                private authService: AuthService) {
    }

    logout() {
        this.authService.clearUser();

        this.http.post(`${this.baseUrl}/logout`, {}, { withCredentials: true }).subscribe({
            next: () => console.log('Logged out on server.'),
            error: () => console.warn('Logout on server failed (fallback to client-only logout).')
        });

        this.router.navigate(['/login']).then(success => {
            if (success) {
                console.log('Navigated to login!');
            } else {
                console.warn('Navigation to login failed.');
            }
        });
    }
}
