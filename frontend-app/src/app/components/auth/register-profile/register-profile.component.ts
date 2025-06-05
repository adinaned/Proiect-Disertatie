import {Component} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';
import {Router} from '@angular/router';
import {RegisterProfileService} from '../../../services/auth/register-profile.service';
import {RegisterAccountService} from '../../../services/auth/register-account.service';

@Component({
    selector: 'app-register-account-form',
    imports: [CommonModule, FormsModule],
    templateUrl: './register-profile.component.html',
    styleUrls: ['../shared/auth-form.component.css', './register-profile.component.css']
})

export class RegisterProfileComponent {
    date_of_birth = '';
    country_id = 1;
    city = '';
    address = '';
    national_id = '';
    organization_id = 1;
    role_id = 1;
    profile_status_id = 1;

    constructor(
        private router: Router,
        private profileService: RegisterProfileService,
        private accountService: RegisterAccountService,
        private userDraft: RegisterAccountService
    ) {}

    ngOnInit(): void {
        if (!this.accountService.hasValidUserData()) {
            console.log("Please complete the first step before continuing.");
            this.router.navigate(['/register-account']).then(success => {
                if (success) {
                    console.log('Please complete the first step before continuing.');
                } else {
                    console.warn('Please complete the first step before continuing.');
                }
            });
        }
    }

    handleSubmit(): void {
        const draftData = this.userDraft.getProfileDraftData();
        const passwordData = this.userDraft.getPasswordData();
        const emailData = this.userDraft.getEmailData();

        this.validateSubmission(draftData, passwordData, emailData);

        const profileData = {
            first_name: draftData.first_name,
            last_name: draftData.last_name,
            date_of_birth: this.date_of_birth,
            country_id: this.country_id,
            city: this.city,
            address: this.address,
            national_id: Number(this.national_id),
            organization_id: this.organization_id,
            role_id: this.role_id,
            profile_status_id: this.profile_status_id
        };

        console.log('Profile:', profileData);

        this.profileService.registerProfile(profileData, passwordData, emailData).subscribe({
            next: () => {
                this.userDraft.clear();
                this.router.navigate(['/login']);
            },
            error: (err) => {
                console.error('Registration error:', err);
                alert('Registration failed.');
            }
        });
    }

    validateSubmission(draftData: any, passwordData: any, emailData: any): void {
        if (!draftData.first_name || !draftData.last_name) {
            alert('Last name and first name are mandatory.');
            return;
        }

        if (!this.date_of_birth) {
            alert('Date of birth can not be empty.');
            return;
        }

        if (!this.country_id || this.country_id <= 0) {
            alert('Country is required.');
            return;
        }

        if (!this.address.trim()) {
            alert('Address is required.');
            return;
        }

        if (!this.national_id || isNaN(Number(this.national_id))) {
            alert('This field cannot be left empty.');
            return;
        }

        if (!emailData?.email_address) {
            alert('Invalid or missing email.');
            return;
        }

        if (!passwordData?.password || passwordData.password.length < 4) {
            alert('Password is too short.');
            return;
        }
    }
}
