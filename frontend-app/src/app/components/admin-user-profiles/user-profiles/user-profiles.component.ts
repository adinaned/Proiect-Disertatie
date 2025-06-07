import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { NgClass, NgForOf } from '@angular/common';
import { forkJoin } from 'rxjs';
import { UserService } from '../../../services/users/user.service';
import {routes} from "../../../routes/app.routes";

@Component({
    selector: 'app-user-profiles',
    standalone: true,
    imports: [NgClass, NgForOf],
    templateUrl: './user-profiles.component.html',
    styleUrls: ['./user-profiles.component.css']
})
export class UserProfilesComponent implements OnInit {
    users: any[] = [];

    constructor(
        private router: Router,
        private userService: UserService
    ) {}

    ngOnInit() {
        this.userService.getUsers().subscribe((users) => {

            this.userService.getRoles().subscribe((roles) => {
                const statusRequests = users.map(user =>
                    this.userService.getProfileStatuses(user.id)
                );

                forkJoin(statusRequests).subscribe((statusesArray) => {

                    this.users = users.map((user, index) => {
                        const role = roles.find(r => r.id === user.role_id)?.name ?? 'Unknown';
                        const statusObj = statusesArray[index];
                        const profileStatus = statusObj?.name ?? 'N/A';

                        return {
                            ...user,
                            firstName: user.first_name,
                            lastName: user.last_name,
                            role,
                            profile_status: profileStatus
                        };
                    });
                });
            });
        });
    }

    viewUser(userId: number) {
        console.log('View user clicked. User ID:', userId);
        this.router.navigate([`/view-user-profile/${userId}`]);
    }

    getStatusClass(status: string): string {
        return status?.toLowerCase().replace(/\s+/g, '-') ?? '';
    }
}
