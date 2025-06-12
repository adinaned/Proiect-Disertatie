import {Component} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';
import {Router} from '@angular/router';
import {forkJoin} from 'rxjs';

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
    country = '';
    city = '';
    address = '';
    national_id = '';
    organization = '';
    countries: any[] = [];


    constructor(
        private router: Router,
        private registerAccountService: RegisterAccountService,
        private registerProfileService: RegisterProfileService,
        private userDraft: RegisterAccountService
    ) {
    }

    ngOnInit(): void {
        if (!this.registerAccountService.hasValidUserData()) {
            console.warn("Please complete the first step before continuing.");
            this.router.navigate(['/register-account']);
        }

        this.registerProfileService.getAllCountries().subscribe({
            next: (response) => {
                this.countries = response.data || [];
            },
            error: (err) => {
                console.error('Failed to load countries:', err);
            }
        });
    }

    handleSubmit(): void {
        const draftData = this.userDraft.getProfileDraftData();

        try {
            this.validateSubmission(draftData);
        } catch (e) {
            console.error('Validation failed:', e);
            alert('Invalid submission data.');
            return;
        }

        forkJoin({
            country: this.registerProfileService.getCountryByName(this.country),
            organization: this.registerProfileService.getOrganizationByName(this.organization)
        }).subscribe({
            next: ({ country, organization }) => {
                const profileData = {
                    first_name: draftData.first_name,
                    last_name: draftData.last_name,
                    date_of_birth: new Date(this.date_of_birth).toISOString(),
                    country_id: country?.data?.id,
                    city: this.city,
                    address: this.address,
                    national_id: Number(this.national_id),
                    organization_id: organization?.data?.id,
                    email_address: draftData.email_address,
                    password: draftData.password
                };

                console.log('Profile data ready for submission:', profileData);

                this.registerProfileService.registerProfile(profileData).subscribe({
                    next: () => {
                        this.userDraft.clear();
                        this.router.navigate(['/login']);
                    },
                    error: (err) => {
                        console.error('Registration error:', err);
                        alert('Registration failed. Please try again later.');
                    }
                });
            },
            error: (err) => {
                console.error('Error retrieving country or organization:', err);
                alert('Failed to retrieve organization or country. Please check your input.');
            }
        });
    }

    validateSubmission(draftData: any): void {
        if (!draftData.first_name || !draftData.last_name) {
            alert('Last name and first name are mandatory.');
            return;
        }

        if (!this.date_of_birth) {
            alert('Date of birth can not be empty.');
            return;
        }

        if (!this.country) {
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

        if (!draftData.email_address) {
            alert('Invalid or missing email.');
            return;
        }

        if (!draftData.password || draftData.password.length < 4) {
            alert('Password is too short.');
            return;
        }
    }
}
