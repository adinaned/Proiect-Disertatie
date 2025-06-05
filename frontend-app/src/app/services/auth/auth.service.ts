import {Injectable} from '@angular/core';

@Injectable({providedIn: 'root'})
export class AuthService {
    isLoggedIn(): boolean {
        return typeof window !== 'undefined' && !!localStorage.getItem('token');
    }
}
