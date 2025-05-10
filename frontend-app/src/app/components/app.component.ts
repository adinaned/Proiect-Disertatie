import {Component} from '@angular/core';
import {RouterOutlet} from '@angular/router';
import {Router} from '@angular/router';
import {NgIf} from "@angular/common";

@Component({
    selector: 'app-root',
    imports: [RouterOutlet, NgIf],
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css'],
})
export class AppComponent {
    constructor(private router: Router) {
    }

    showMenu = false;
    title = 'Software Voting Application';

    // isAuthenticated = false;
    //
    // constructor(private authService: AuthService) {
    //     this.isAuthenticated = this.authService.isUserLoggedIn();
    // }
    handleHome() {
        console.log("Switching to 'Voting sessions' tab");
        this.router.navigate(['/voting-sessions']);
    }

    handleProfile() {
        console.log("Switching to 'Profile' tab");
        this.router.navigate(['/profile']);
    }

    handleEditProfile() {
        console.log("Switching to 'Edit Profile' tab");
        this.router.navigate(['/edit-profile']);
    }

    handleLogout() {
        console.log("Logging out");
        console.log("Switching to 'Edit Profile' tab");
        this.router.navigate(['/login']);
    }
}