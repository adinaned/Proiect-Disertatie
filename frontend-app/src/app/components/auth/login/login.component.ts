import {Component} from '@angular/core';
import {Router} from '@angular/router';
import {LoginService} from '../../../services/auth/login.service';
import {FormsModule} from "@angular/forms";
import {AuthService} from '../../../services/auth/auth.service';

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    imports: [FormsModule],
    styleUrls: ['../shared/auth-form.component.css', '../../../../app.component.css'],
})

export class LoginComponent {
    constructor(private router: Router,
                private loginService: LoginService,
                private authService: AuthService,
    ) {
    }

    email: string = '';
    password: string = '';

    handleLogin() {
        if (!this.email || !this.password) {
            alert('Please fill in both email and password.');
            return;
        }

        this.loginService.loginUser({email: this.email, password: this.password}).subscribe({
            next: (response: any) => {
                console.log('Login successful:', response);

                localStorage.setItem('token', response.token);
                localStorage.setItem('user', JSON.stringify(response.user))
                // this.authService.setUserName(response.user.first_name);

                this.router.navigate(['/voting-sessions']);
            },
            error: (err) => {
                console.error('Login failed:', err);
                alert('Login failed. Please check your credentials.');
            }
        });
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
