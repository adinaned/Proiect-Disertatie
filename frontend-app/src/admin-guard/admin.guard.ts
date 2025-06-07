import {Injectable} from '@angular/core';
import {CanActivate, Router, UrlTree} from '@angular/router';
import {AuthService} from "../app/services/auth/auth.service";

@Injectable({providedIn: 'root'})
export class AdminGuard implements CanActivate {
    constructor(private authService: AuthService, private router: Router) {
    }

    async canActivate(): Promise<boolean> {
        const isAdmin = await this.authService.isAdmin();
        if (!isAdmin) {
            this.router.navigate(['/login']);
            return false;
        }
        return true;
    }
}

