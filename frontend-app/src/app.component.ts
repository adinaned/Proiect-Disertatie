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
    constructor(private router: Router,
                private logoutService: LogoutService,
                public authService: AuthService) {
    }

    showMenu = false;
    title = 'Software Voting Application';
    userName: string = '';

    ngOnInit() {
        if (this.authService.isLoggedIn()) {
            const profile = JSON.parse(localStorage.getItem('user') || '{}');
            this.userName = profile.first_name || 'User';
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
}