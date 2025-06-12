import {Injectable} from '@angular/core';
import {CanActivate, Router} from '@angular/router';
import {AuthService} from '../app/services/auth/auth.service';
import {VotingSessionsService} from '../app/services/voting/voting-sessions.service';
import {UserService} from "../app/services/users/user.service";
import {firstValueFrom} from 'rxjs';

@Injectable({providedIn: 'root'})
export class AdminGuard implements CanActivate {
    constructor(
        private authService: AuthService,
        private router: Router,
        private userService: UserService
    ) {
    }

    async canActivate(): Promise<boolean> {
        try {
            const user = await this.authService.getCurrentUserFromCookie();
            if (!user?.user_id) {
                this.router.navigate(['/login']);
                return false;
            }

            const userDetails = await firstValueFrom(this.userService.getUserById(user.user_id));
            const roleId = userDetails?.role_id;
            if (!roleId) {
                this.router.navigate(['/login']);
                return false;
            }

            const roleDetails = await firstValueFrom(this.userService.getRoleById(roleId));
            const roleName = roleDetails?.name?.toLowerCase();

            if (roleName === 'admin') {
                return true;
            } else {
                this.router.navigate(['/login']);
                return false;
            }
        } catch (err) {
            console.error('Error in AdminGuard:', err);
            this.router.navigate(['/login']);
            return false;
        }
    }
}
