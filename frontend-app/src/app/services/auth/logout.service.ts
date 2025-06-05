import {Injectable} from '@angular/core';
import {Router} from '@angular/router';

@Injectable({providedIn: 'root'})
export class LogoutService {
    constructor(private router: Router) {
    }

    logout() {
        localStorage.clear();

        this.router.navigate(['/login']).then(success => {
            if (success) {
                console.log('Navigated to login!');
            } else {
                console.warn('Navigation to login failed.');
            }
        });
    }
}
