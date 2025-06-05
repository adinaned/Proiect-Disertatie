import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {HttpClient} from '@angular/common/http';
import {catchError, of, switchMap} from "rxjs";
import {NgIf} from "@angular/common";

@Component({
    selector: 'app-auth-auth',
    imports: [
        NgIf
    ],
    templateUrl: './view-profile.component.html',
    styleUrls: ['../../auth/shared/auth-form.component.css', './view-profile.component.css']
})

export class ViewProfileComponent {
    profile: any;
    email: string = '';
    country: string = '';
    organization: string = '';
    role: string = '';

    constructor(private router: Router,
                private http: HttpClient) {
    }

    ngOnInit(): void {
        const userDataString = localStorage.getItem('user');

        if (!userDataString) {
            console.log("'user' data not found in localStorage.");
            return;
        }

        try {
            const userData = JSON.parse(userDataString);
            console.log(userData);
            this.email = userData?.email;
            console.log(this.email);

        } catch (e) {
            console.log('Error at parsing JSON:', e);
            return;
        }

        this.http.get<any>(`http://127.0.0.1:5000/emails/${this.email}`)
            .pipe(
                switchMap(emailResponse => {
                    const userId = emailResponse?.user_id;
                    if (!userId) {
                        throw new Error('user_id not found in email response');
                    }
                    return this.http.get<any>(`http://127.0.0.1:5000/users/${userId}`);
                }),
                catchError(error => {
                    console.error('API error:', error);
                    return of(null);
                })
            )

            .subscribe(userData => {
                this.profile = userData;
                this.getCountryName(this.profile.country_id);
                this.getOrganizationName(this.profile.organization_id);
                this.getRoleName(this.profile.role_id);
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
