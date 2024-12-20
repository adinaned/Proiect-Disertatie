import { Component } from '@angular/core';
import {Router} from '@angular/router';

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    imports: [],
    styleUrls: ['../shared/auth-form.component.css', '../../../../components/app.component.css'],
})

export class LoginComponent {
    constructor(private router: Router) {}

    email: string = '';
    password: string = '';

    handleLogin() {
        console.log('Email:', this.email);
        console.log('Password:', this.password);
        console.log('Login submitted');
    }

    handleRegister() {
        console.log("Switching to 'Register' tab");
        this.router.navigate(['/register-account']);
    }

    handleForgotPassword() {
        console.log("Switching to 'Forgot password' tab");
        this.router.navigate(['/forgot-password']);
    }
}

export class AppComponent {
    title = 'software-voting-app';
}
