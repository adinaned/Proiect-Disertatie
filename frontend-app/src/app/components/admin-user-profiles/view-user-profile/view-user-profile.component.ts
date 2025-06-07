import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {FormsModule} from '@angular/forms';
import {CommonModule} from '@angular/common';
import {catchError, of, switchMap} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {NgIf} from '@angular/common';

@Component({
    selector: 'app-view-user-profile',
    templateUrl: './view-user-profile.component.html',
    imports: [FormsModule, CommonModule, NgIf],
    styleUrls: ['./view-user-profile.component.css']
})
export class ViewUserProfileComponent implements OnInit {
    profile: any;
    email: string = '';
    country: string = '';
    organization: string = '';
    role: { id: number; name: string } | null = null;
    originalRole: { id: number; name: string } | null = null;
    roles: { id: number; name: string }[] = [];
    roleId: number | null = null;
    profileStatus: string = '';
    statusOptions: string[] = ['active', 'closed', 'suspended'];
    userId: number | null = null;
    currentProfileStatus: string = '';
    selectedProfileStatus: string = '';
    hasUnsavedChanges = false;
    originalProfileStatus: string = '';

    constructor(
        private router: Router,
        private route: ActivatedRoute,
        private http: HttpClient
    ) {
    }

    ngOnInit(): void {
        const userId = this.route.snapshot.paramMap.get('id') || '';
        if (!userId) {
            console.error('User ID not found in route.');
            return;
        }

        this.http.get<any>(`http://127.0.0.1:5000/emails/user/${userId}`)
            .pipe(
                switchMap(emailResponse => {
                    const email_address = emailResponse?.email_address;
                    if (!email_address) throw new Error('Email Address not found');
                    this.email = email_address;

                    return this.http.get<any>(`http://127.0.0.1:5000/users/${userId}`);
                }),
                catchError(error => {
                    console.error('API error:', error);
                    return of(null);
                })
            )
            .subscribe(userData => {
                if (!userData) return;

                this.profile = userData;
                this.userId = userData.id;
                this.roleId = userData.role_id;

                this.getCountryName(userData.country_id);
                this.getOrganizationName(userData.organization_id);
                this.getRoleName(userData.role_id);

                this.http.get<any>(`http://127.0.0.1:5000/profile_statuses/${userData.id}`)
                    .subscribe(status => {
                        this.profile.profile_status = status?.name || '';
                        this.profileStatus = this.profile.profile_status;
                        this.currentProfileStatus = this.profile.profile_status;
                        this.originalProfileStatus = this.profile.profile_status;
                        this.selectedProfileStatus = '';
                    });
            });
    }

    getCountryName(id: number) {
        this.http.get<any>(`http://127.0.0.1:5000/countries/${id}`)
            .subscribe(res => this.country = res?.name || '');
    }

    getOrganizationName(id: number) {
        this.http.get<any>(`http://127.0.0.1:5000/organizations/${id}`)
            .subscribe(res => this.organization = res?.name || '');
    }

    getRoleName(currentRoleId: number) {
        this.http.get<any[]>(`http://127.0.0.1:5000/roles`)
            .subscribe(allRoles => {
                this.roles = allRoles;

                const matched = allRoles.find(r => r.id === currentRoleId);
                if (matched) {
                    this.role = matched;
                    this.originalRole = { ...matched };
                }
            });
    }

    onRoleChange(newRole: any) {
        this.role = newRole;
        this.roleId = newRole.id;
        this.checkForUnsavedChanges();
    }

    saveChanges() {
        if (!this.userId) return;

        const statusChanged = this.selectedProfileStatus && this.selectedProfileStatus !== this.currentProfileStatus;
        const roleChanged = this.role?.id !== this.originalRole?.id;

        if (statusChanged) {
            const payload_profile_status = {
                user_id: this.userId,
                name: this.selectedProfileStatus
            };

            this.http.put(`http://127.0.0.1:5000/profile_statuses/${this.userId}`, payload_profile_status)
                .subscribe({
                    next: () => {
                        this.currentProfileStatus = this.selectedProfileStatus!;
                        this.originalProfileStatus = this.selectedProfileStatus!;
                        this.selectedProfileStatus = '';
                        this.checkForUnsavedChanges();
                        alert('Profile status updated!');
                    },
                    error: (err) => {
                        console.error('Failed to update profile status:', err);
                        alert('Failed to update profile status.');
                    }
                });
        }

        if (roleChanged) {
            const payload_role = {
                role_id: this.role?.id
            };

            this.http.put(`http://127.0.0.1:5000/users/${this.userId}`, payload_role)
                .subscribe({
                    next: () => {
                        this.originalRole = {
                            id: this.role!.id,
                            name: this.role!.name
                        };
                        this.checkForUnsavedChanges();
                        alert('User role updated!');
                    },
                    error: (err) => {
                        console.error('Failed to update user role:', err);
                        alert('Failed to update user role.');
                    }
                });
        }

        this.checkForUnsavedChanges();
    }

    checkForUnsavedChanges() {
        const statusChanged = this.selectedProfileStatus && this.selectedProfileStatus !== this.originalProfileStatus;
        const roleChanged = this.role !== this.originalRole;

        this.hasUnsavedChanges = statusChanged || roleChanged;
    }
}
