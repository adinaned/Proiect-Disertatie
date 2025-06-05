import {Injectable} from '@angular/core';
import {CanActivate, Router, UrlTree} from '@angular/router';
import {AuthService} from '../app/services/auth/auth.service';

@Injectable({providedIn: 'root'})
export class AuthGuard implements CanActivate {
    constructor(private authService: AuthService, private router: Router) {
    }

    canActivate(): boolean | UrlTree {
        if (this.authService.isLoggedIn()) {
            return true;
        } else {
            this.router.navigate(['/login']).then(success => {
                if (success) {
                    console.log('The user is not logged in, redirecting to login page.');
                } else {
                    console.warn('Cannot redirect to login, navigation failed.');
                    this.router.createUrlTree(['/login']);
                }
            });
            return false;
        }
    }
}
