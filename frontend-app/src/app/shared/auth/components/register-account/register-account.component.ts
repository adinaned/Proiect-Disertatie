import { Component, ViewEncapsulation } from '@angular/core';
import { Router } from '@angular/router';

@Component({
    selector: 'app-register-account',
    imports: [],
    templateUrl: './register-account.component.html',
    styleUrls: ['../../../../components/app.component.css', '../shared/auth-form.component.css'],
    encapsulation: ViewEncapsulation.Emulated,
})
export class RegisterAccountComponent {
    constructor(private router: Router) {
    }

    email: string = '';
    password: string = '';

    handleLogin() {
        console.log("Switching to 'Log In' tab");
        this.router.navigate(['/login']);
    }

    handleRegister() {
        console.log('Email:', this.email);
        console.log('Password:', this.password);
        console.log('User created');
        this.router.navigate(['/register-profile']);
    }
}

export class AppComponent {
    title = 'software-voting-app';
}
