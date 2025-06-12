import {Injectable} from '@angular/core';
import {CanActivate, Router, UrlTree} from '@angular/router';
import {AuthService} from '../app/services/auth/auth.service';

@Injectable({providedIn: 'root'})
export class AuthGuard implements CanActivate {
    constructor(private authService: AuthService, private router: Router) {
    }

    async canActivate(): Promise<boolean | UrlTree> {
        return this.authService.isAuthenticatedByCookie().then(isAuth => {
            if (isAuth) {
                return true;
            } else {
                console.warn('User is not authenticated via cookie, redirecting...');
                return this.router.createUrlTree(['/login']);
            }
        });
    }
}
