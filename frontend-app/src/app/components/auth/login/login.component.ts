import {Component} from '@angular/core';
import {Router} from '@angular/router';
import {FormsModule} from "@angular/forms";

import {LoginService} from '../../../services/auth/login.service';
import {AuthService} from '../../../services/auth/auth.service';

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    imports: [FormsModule],
    styleUrls: ['../shared/auth-form.component.css', '../../../../app.component.css'],
})
export class LoginComponent {
    email: string = '';
    password: string = '';
    loading: boolean = false;

    constructor(private router: Router,
                private loginService: LoginService,
                private authService: AuthService) {
    }

    async handleLogin() {
        if (!this.email || !this.password) {
            alert('Please fill in both email and password.');
            return;
        }

        this.loading = true;

        try {
            const hashedPassword = await this.hashPassword(this.password);

            this.loginService.loginUser({email_address: this.email, password: hashedPassword}).subscribe({
                next: () => {
                    this.loginService.getCurrentUser().subscribe({
                        next: (meResponse: any) => {
                            this.authService.setUser(meResponse.data);
                            this.router.navigate(['/voting-sessions']);
                        },
                        error: (err) => {
                            console.error('Failed to fetch user info:', err);
                            alert('Could not load user info.');
                        },
                        complete: () => {
                            this.loading = false;
                        }
                    });
                },
                error: (err) => {
                    console.error('Login failed:', err);
                    alert('Login failed. Please check your credentials.');
                    this.loading = false;
                }
            });
        } catch (err) {
            console.error('Error hashing password:', err);
            alert('An unexpected error occurred. Please try again.');
            this.loading = false;
        }
    }

    async hashPassword(password: string): Promise<string> {
        const encoder = new TextEncoder();
        const data = encoder.encode(password);
        const hashBuffer = await crypto.subtle.digest('SHA-256', data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }

    handleRegister() {
        this.router.navigate(['/register-account']);
    }

    handleForgotPassword() {
        this.router.navigate(['/forgot-password']);
    }
}


export class AppComponent {
    title = 'software-voting-app';
}
