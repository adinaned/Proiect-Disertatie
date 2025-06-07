import {Component} from '@angular/core';
import {Router} from '@angular/router';
import {RouterModule} from '@angular/router';
import {NgIf, NgOptimizedImage} from "@angular/common";
import {LogoutService} from "./app/services/auth/logout.service";
import {AuthService} from './app/services/auth/auth.service';

@Component({
    selector: 'app-root',
    imports: [RouterModule, NgIf, NgOptimizedImage],
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css'],
})
export class AppComponent {
    constructor(
        private router: Router,
        private logoutService: LogoutService,
        public authService: AuthService
    ) {
    }

    showMenu = false;
    title = 'Software Voting Application';
    userName: string = '';
    isAdmin: boolean = false;

    ngOnInit() {
        if (this.authService.isLoggedIn()) {
            const profile = JSON.parse(localStorage.getItem('user') || '{}');
            this.userName = profile.first_name || 'User';

            const roleId = profile.role_id;
            this.isAdmin = roleId === 1;
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
}
