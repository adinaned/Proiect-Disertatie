import {Component, OnInit} from '@angular/core';
import {Router, RouterOutlet} from '@angular/router';
import {LogoutService} from './app/services/auth/logout.service';
import {AuthService} from './app/services/auth/auth.service';
import {NgIf, NgOptimizedImage} from "@angular/common";
import {UserService} from "./app/services/users/user.service";

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    imports: [
        NgOptimizedImage,
        NgIf,
        RouterOutlet
    ],
    styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
    showMenu = false;
    user: any = null;
    isAdmin: boolean = false;

    constructor(
        private router: Router,
        private logoutService: LogoutService,
        private userService: UserService,
        public authService: AuthService
    ) {
    }

    async ngOnInit() {
        try {
            await this.authService.getCurrentUserFromCookie();

            this.authService.user$.subscribe(user => {
                if (user && user.user_id) {
                    this.user = user;
                    console.log('Auth user updated in AppComponent:', user);
                    this.checkIfUserIsAdmin(user.user_id);
                } else {
                    console.warn('User is null or missing user_id');
                    this.user = null;
                }
            });
        } catch (err) {
            console.error('Error loading user from cookie:', err);
            this.user = null;
        }
    }


    handleHome() {
        console.log("Switching to 'Voting sessions' tab");
        this.router.navigate(['/voting-sessions']).then(success => {
            if (success) {
                console.log('Navigating to Voting sessions page!');
            } else {
                console.warn('Navigation to Voting sessions failed.');
            }
        });
    }

    handleProfile() {
        console.log("Switching to 'Profile' tab");
        this.router.navigate(['/profile']).then(success => {
            if (success) {
                console.log('Navigating to Profile page!');
            } else {
                console.warn('Navigation to Profile failed.');
            }
        });
    }

    handleEditProfile() {
        console.log("Switching to 'Update Password' tab");
        this.router.navigate(['/change-password']).then(success => {
            if (success) {
                console.log('Navigating to Update Password page!');
            } else {
                console.warn('Navigation to Update Password failed.');
            }
        });
    }

    handleLogout() {
        this.logoutService.logout();
    }

    get authenticated(): boolean {
        return !!this.user;
    }

    get userName(): string {
        return this.user?.first_name || 'User';
    }

    checkIfUserIsAdmin(user_id: any): void {
        this.userService.getUserById(user_id).subscribe({
            next: (userRes) => {
                const roleId = userRes?.role_id;
                if (!roleId) return;

                this.userService.getRoleById(roleId).subscribe({
                    next: (roleRes) => {
                        const roleName = roleRes?.name?.toLowerCase();
                        this.isAdmin = roleName === 'admin';
                        console.log("User is admin?", this.isAdmin);
                    },
                    error: () => console.error('Error fetching role info.')
                });
            },
            error: () => console.error('Error fetching user details.')
        });
    }

    createVotingSession() {
        console.log("Navigating to 'Create Voting Session'");
        this.router.navigate(['/create-voting-session']).then(success => {
            if (success) {
                console.log('Navigated to Create Voting Session page!');
            } else {
                console.warn('Navigation to Create Voting Session failed.');
            }
        });
    }

    viewUserProfiles() {
        console.log("Navigating to 'User Profiles'");
        this.router.navigate(['/user-profiles']).then(success => {
            if (success) {
                console.log('Navigated to User Profiles page!');
            } else {
                console.warn('Navigation to User Profiles failed.');
            }
        });
    }

    viewVotingSessions() {
        console.log("Navigating to 'Voting Sessions'");
        this.router.navigate(['/voting-sessions']).then(success => {
            if (success) {
                console.log('Navigated to Voting Sessions page!');
            } else {
                console.warn('Navigation to Voting Sessions failed.');
            }
        });
    }
}
