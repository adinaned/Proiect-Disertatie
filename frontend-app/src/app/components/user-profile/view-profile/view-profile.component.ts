import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { catchError, of, switchMap } from 'rxjs';
import {NgClass, NgIf} from '@angular/common';

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

    constructor(
        private router: Router,
        private http: HttpClient
    ) {}

    ngOnInit(): void {
        const userDataString = localStorage.getItem('user');

        if (!userDataString) {
            console.log("'user' data not found in localStorage.");
            return;
        }

        try {
            const userData = JSON.parse(userDataString);
            this.email = userData?.email;
            if (!this.email) {
                console.log('Email not found in user data');
                return;
            }
        } catch (e) {
            console.error('Error parsing user JSON:', e);
            return;
        }

        this.http.get<any>(`http://127.0.0.1:5000/emails/${this.email}`)
            .pipe(
                switchMap(emailResponse => {
                    const userId = emailResponse?.user_id;
                    if (!userId) {
                        throw new Error('user_id not found in email response');
                    }

                    return this.http.get<any>(`http://127.0.0.1:5000/users/${userId}`).pipe(
                        switchMap(userData => {
                            this.profile = userData;
                            this.getCountryName(userData.country_id);
                            this.getOrganizationName(userData.organization_id);
                            this.getRoleName(userData.role_id);

                            return this.http.get<any>(`http://127.0.0.1:5000/profile_statuses/${userId}`);
                        })
                    );
                }),
                catchError(error => {
                    console.error('API error:', error);
                    return of(null);
                })
            )
            .subscribe(profileStatusResponse => {
                this.profileStatus = profileStatusResponse?.name?.toUpperCase() || 'UNKNOWN';
                console.log('Profile status:', this.profileStatus);
            });
    }

    getCountryName(id: number) {
        this.http.get<any>(`http://127.0.0.1:5000/countries/${id}`)
            .subscribe(response => {
                this.country = response?.name || '';
            });
    }

    getOrganizationName(id: number) {
        this.http.get<any>(`http://127.0.0.1:5000/organizations/${id}`)
            .subscribe(response => {
                this.organization = response?.name || '';
            });
    }

    getRoleName(id: number) {
        this.http.get<any>(`http://127.0.0.1:5000/roles/${id}`)
            .subscribe(response => {
                this.role = response?.name || '';
            });
    }
}
