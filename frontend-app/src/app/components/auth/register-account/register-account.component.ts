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

    async handleRegister(): Promise<void> {
        if (this.password !== this.confirmPassword) {
            alert('Passwords are not the same!');
            return;
        }

        try {
            const hashedPassword = await this.hashPassword(this.password);

            const profileData = {
                first_name: this.firstName,
                last_name: this.lastName,
                email_address: this.email,
                password: hashedPassword,
            };

            this.userDraftService.getEmail(profileData.email_address).subscribe({
                next: (exists) => {
                    if (exists) {
                        alert('This email is already registered. Please use a different email.');
                        return;
                    }
                },
                error: (err) => {
                    if (err.status === 404) {
                        this.userDraftService.setAccountData(profileData);
                        console.log('Profile data being set:', profileData);
                        this.router.navigate(['/register-profile']);
                    } else {
                        console.error('Error checking email existence:', err);
                        alert('An error occurred while checking the email. Please try again.');
                    }
                }
            });
        } catch (err) {
            console.error('Error hashing password:', err);
            alert('An unexpected error occurred. Please try again.');
        }
    }

    private async hashPassword(password: string): Promise<string> {
        const encoder = new TextEncoder();
        const data = encoder.encode(password);
        const hashBuffer = await crypto.subtle.digest('SHA-256', data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }
}
