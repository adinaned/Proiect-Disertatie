import {Injectable} from '@angular/core';
import {CanActivate, Router, UrlTree} from '@angular/router';
import {AuthService} from '../app/services/auth/auth.service';

@Injectable({providedIn: 'root'})
export class GuestGuard implements CanActivate {
    constructor(private authService: AuthService, private router: Router) {
    }

    async canActivate(): Promise<boolean | UrlTree> {
        return this.authService.isAuthenticatedByCookie().then(isAuth => {
            if (!isAuth) {
                return true;
            } else {
                console.warn('User is already authenticated, redirecting to /voting-sessions');
                return this.router.createUrlTree(['/voting-sessions']);
            }
        });
    }
}
