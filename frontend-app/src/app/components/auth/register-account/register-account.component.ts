import {Component, ViewEncapsulation} from '@angular/core';
import {Router} from '@angular/router';
import {RegisterAccountService} from '../../../services/auth/register-account.service';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';

@Component({
    selector: 'app-register-account',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './register-account.component.html',
    styleUrls: ['../../../../app.component.css', '../shared/auth-form.component.css'],
    encapsulation: ViewEncapsulation.Emulated,
})
export class RegisterAccountComponent {
    firstName = '';
    lastName = '';
    email = '';
    password = '';
    confirmPassword = '';

    constructor(private router: Router, private userDraftService: RegisterAccountService) {
    }

    handleLogin(): void {
        this.router.navigate(['/login']).then(success => {
            if (success) {
                console.log('Navigated to login!');
            } else {
                console.warn('Navigation to login failed.');
            }
        });
    }

    handleRegister(): void {
        if (this.password !== this.confirmPassword) {
            alert('Passwords are not the same!');
            return;
        }

        const profileData = {
            first_name: this.firstName,
            last_name: this.lastName,
        };

        const emailData = {
            email_address: this.email,
        };

        const passwordData = {
            password: this.password,
        }

        this.userDraftService.getEmail(this.email).subscribe({
            next: (exists) => {
                if (exists) {
                    alert('This email is already registered. Please use a different email.');
                    return;
                }
            },
            error: (err) => {
                if (err.status === 404) {
                    this.userDraftService.setAccountData(profileData, passwordData, emailData);
                    console.log('Profile data being set:', profileData);
                    console.log('Password data being set:', passwordData);
                    console.log('Email data being set:', emailData);
                    this.router.navigate(['/register-profile']);
                } else {
                    console.error('Error checking email existence:', err);
                    alert('An error occurred while checking the email. Please try again.');
                }
            }
        });
    }
}
