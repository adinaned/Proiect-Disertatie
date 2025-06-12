import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {NgClass, NgForOf, NgIf} from '@angular/common';
import {forkJoin, map} from 'rxjs';
import {UserService} from '../../../services/users/user.service';
import {AuthService} from '../../../services/auth/auth.service';

@Component({
    selector: 'app-user-profiles',
    standalone: true,
    imports: [NgClass, NgForOf, NgIf],
    templateUrl: './user-profiles.component.html',
    styleUrls: ['./user-profiles.component.css']
})
export class UserProfilesComponent implements OnInit {
    users: any[] = [];

    constructor(
        private router: Router,
        private userService: UserService,
        private authService: AuthService
    ) {
    }

    ngOnInit() {
        this.authService.getCurrentUserFromCookie().then(currentUser => {
            if (!currentUser?.user_id) {
                console.error('User ID not found in cookie.');
                return;
            }

            this.userService.getUserById(currentUser.user_id).subscribe(userData => {
                const organizationId: string = userData?.organization_id;
                if (!organizationId) {
                    console.error('Organization ID not found in user data.');
                    return;
                }

                this.userService.getUsersByOrganizationId(organizationId).subscribe((users: any[]) => {
                    const filteredUsers = users.filter(u => u.id !== currentUser.user_id);

                    const combinedRequests = filteredUsers.map((user: any) => {
                        if (!user.role_id) {
                            return forkJoin({
                                status: this.userService.getProfileStatuses(user.id)
                            }).pipe(
                                map(({ status }) => ({
                                    ...user,
                                    firstName: user.first_name,
                                    lastName: user.last_name,
                                    role: 'None',
                                    profile_status: status?.data?.name || 'N/A'
                                }))
                            );
                        }

                        return forkJoin({
                            role: this.userService.getRoleById(user.role_id),
                            status: this.userService.getProfileStatuses(user.id)
                        }).pipe(
                            map(({ role, status }) => ({
                                ...user,
                                firstName: user.first_name,
                                lastName: user.last_name,
                                role: role?.name || 'Unknown',
                                profile_status: status?.data?.name || 'N/A'
                            }))
                        );
                    });

                    forkJoin(combinedRequests).subscribe((enrichedUsers: any[]) => {
                        this.users = enrichedUsers;
                    });
                });
            });
        }).catch(err => {
            console.error('Failed to load current user from cookie:', err);
        });
    }

    viewUser(userId: number) {
        this.router.navigate([`/view-user-profile/${userId}`]);
    }

    getStatusClass(status: string): string {
        return status?.toLowerCase().replace(/\s+/g, '-') ?? '';
    }
}
