import {Component, OnInit} from '@angular/core';
import {catchError, forkJoin, from, of, switchMap} from 'rxjs';
import {ViewProfileService} from '../../../services/user-profile/view-profile.service';
import {NgIf, NgClass} from '@angular/common';
import {AuthService} from "../../../services/auth/auth.service";

@Component({
    selector: 'app-auth-auth',
    standalone: true,
    imports: [NgIf, NgClass],
    templateUrl: './view-profile.component.html',
    styleUrls: ['../../auth/shared/auth-form.component.css', './view-profile.component.css']
})

export class ViewProfileComponent implements OnInit {
    profile: any;
    email: string = '';
    country: string = '';
    organization: string = '';
    role: string = '';
    profileStatus: string = '';
    dateOfBirthFormatted: string = '';

    constructor(
        private profileService: ViewProfileService,
        private authService: AuthService
    ) {
    }

    ngOnInit(): void {
        from(this.authService.getCurrentUserFromCookie())
            .pipe(
                switchMap(user => {
                    const userId = user?.user_id;
                    if (!userId) throw new Error('User not found in cookie');

                    return this.profileService.getEmail(userId).pipe(
                        switchMap(emailRes => {
                            this.email = emailRes?.email_address || '';

                            return this.profileService.getUserDetails(userId).pipe(
                                switchMap(userData => {
                                    this.profile = userData;

                                    if (userData.date_of_birth) {
                                        const date = new Date(userData.date_of_birth);
                                        this.dateOfBirthFormatted = date.toLocaleDateString('en-US', {
                                            year: 'numeric',
                                            month: 'short',
                                            day: 'numeric'
                                        });
                                    }

                                    return forkJoin({
                                        country: this.profileService.getCountryName(userData.country_id),
                                        organization: this.profileService.getOrganizationName(userData.organization_id),
                                        role: this.profileService.getRoleName(userData.role_id),
                                        status: this.profileService.getProfileStatus(userId)
                                    });
                                })
                            );
                        })
                    );
                }),
                catchError(error => {
                    console.error('Error loading profile:', error);
                    return of(null);
                })
            )
            .subscribe(result => {
                if (!result) return;

                this.country = result.country;
                this.organization = result.organization;
                this.role = result.role;
                this.profileStatus = result.status?.name?.toUpperCase() || 'UNKNOWN';

                console.log('Profile loaded');
            });
    }
}