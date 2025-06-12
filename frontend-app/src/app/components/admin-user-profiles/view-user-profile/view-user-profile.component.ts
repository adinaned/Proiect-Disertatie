import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { catchError, of, switchMap, map } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { NgIf } from '@angular/common';
import { UserService } from '../../../services/users/user.service';

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
    role: { id: string; name: string } | null = null;
    originalRole: { id: string; name: string } | null = null;
    roles: { id: string; name: string }[] = [];
    roleId: string | null = null;
    profileStatus: string = '';
    statusOptions: string[] = ['active', 'closed', 'suspended'];
    userId: string | null = null;
    currentProfileStatus: string = '';
    selectedProfileStatus: string = '';
    hasUnsavedChanges = false;
    originalProfileStatus: string = '';
    dateOfBirth: string = '';

    constructor(
        private route: ActivatedRoute,
        private http: HttpClient,
        private userService: UserService,
    ) { }

    ngOnInit(): void {
        const userId = this.route.snapshot.paramMap.get('id') || '';
        if (!userId) {
            console.error('User ID not found in route.');
            return;
        }

        this.http.get<any>(`http://127.0.0.1:5000/emails/user/${userId}`)
            .pipe(
                map(res => res?.data),
                switchMap((emailData: any) => {
                    const email_address = emailData?.email_address;
                    if (!email_address) throw new Error('Email Address not found');
                    this.email = email_address;

                    return this.http.get<any>(`http://127.0.0.1:5000/users/${userId}`).pipe(map(res => res?.data));
                }),
                catchError(error => {
                    console.error('API error:', error);
                    return of(null);
                })
            )
            .subscribe((user: any) => {
                if (!user) return;

                this.profile = user;
                if (user.date_of_birth) {
                    const date = new Date(user.date_of_birth);
                    this.dateOfBirth = date.toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'short',
                        day: 'numeric'
                    });
                }
                this.userId = user.id;
                this.roleId = user.role_id;

                this.getCountryName(user.country_id);
                this.getOrganizationName(user.organization_id);
                this.getRoleName(user.role_id, user.organization_id);

                this.http.get<any>(`http://127.0.0.1:5000/profile_statuses/${user.id}`)
                    .pipe(map(res => res?.data))
                    .subscribe((status: any) => {
                        const statusName = status?.name || '';
                        this.profile.profile_status = statusName;
                        this.profileStatus = statusName;
                        this.currentProfileStatus = statusName;
                        this.originalProfileStatus = statusName;
                        this.selectedProfileStatus = '';
                    });
            });
    }

    private getCountryName(id: string) {
        this.http.get<any>(`http://127.0.0.1:5000/countries/${id}`)
            .pipe(map(res => res?.data))
            .subscribe(res => this.country = res?.name || '');
    }

    private getOrganizationName(id: string) {
        this.http.get<any>(`http://127.0.0.1:5000/organizations/${id}`)
            .pipe(map(res => res?.data))
            .subscribe(res => this.organization = res?.name || '');
    }

    private getRoleName(currentRoleId: string, organizationId: string) {
        this.userService.getRolesByOrganizationId(organizationId)
            .subscribe((allRoles: { id: string; name: string }[]) => {
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

            this.http.patch(`http://127.0.0.1:5000/profile_statuses/${this.userId}`, payload_profile_status)
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

            this.http.patch(`http://127.0.0.1:5000/users/${this.userId}`, payload_role)
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

    public checkForUnsavedChanges() {
        const statusChanged = !!this.selectedProfileStatus && this.selectedProfileStatus !== this.originalProfileStatus;
        const roleChanged = this.role !== this.originalRole;

        this.hasUnsavedChanges = statusChanged || roleChanged;
    }
}