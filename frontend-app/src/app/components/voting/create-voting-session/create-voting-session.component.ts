import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {FormsModule} from '@angular/forms';
import {NgFor} from '@angular/common';
import {firstValueFrom} from 'rxjs';
import {VotingSessionService} from '../../../services/voting/create-voting-session.service';
import {AuthService} from '../../../services/auth/auth.service';
import {UserService} from '../../../services/users/user.service';
import {ViewProfileService} from "../../../services/user-profile/view-profile.service";

@Component({
    selector: 'app-create-voting-session',
    standalone: true,
    imports: [FormsModule, NgFor],
    templateUrl: './create-voting-session.component.html',
    styleUrls: ['./create-voting-session.component.css']
})
export class CreateVotingSessionComponent implements OnInit {
    title = '';
    question = '';
    startDate = '';
    endDate = '';
    organizationId: string = '';
    organizationName: string = '';
    roleId: string = '';

    roles: any[] = [];
    options: { value: string }[] = [{value: ''}];

    constructor(
        private router: Router,
        private votingService: VotingSessionService,
        private authService: AuthService,
        private userService: UserService,
        private viewProfileService: ViewProfileService
    ) {
    }

    ngOnInit(): void {
        this.authService.getCurrentUserFromCookie().then(currentUser => {
            const userId = currentUser?.user_id;
            if (!userId) {
                console.error('User ID not found in cookie.');
                return;
            }

            this.userService.getUserById(userId).subscribe(userData => {
                this.organizationId = userData.organization_id;

                this.viewProfileService.getOrganizationName(this.organizationId).subscribe(orgName => {
                    this.organizationName = orgName;
                });

                this.userService.getRolesByOrganizationId(this.organizationId).subscribe(data => {
                    this.roles = data;
                });
            });
        }).catch(err => {
            console.error('Error loading user from cookie:', err);
        });
    }


    addOption() {
        this.options.push({value: ''});
    }

    removeOption(index: number) {
        this.options.splice(index, 1);
    }

    onCancel() {
        this.router.navigate(['/voting-sessions']);
    }

    async onSubmit() {
        if (!this.title || !this.question || !this.startDate || !this.endDate || !this.organizationId || !this.roleId) {
            alert('Please fill in all required fields.');
            return;
        }

        const start = this.normalizeDatetime(this.startDate);
        const end = this.normalizeDatetime(this.endDate);

        const payload = {
            title: this.title,
            question: this.question,
            start_datetime: new Date(start).toISOString(),
            end_datetime: new Date(end).toISOString(),
            organization_id: this.organizationId,
            role_id: this.roleId
        };

        try {
            const sessionResponse = await firstValueFrom(this.votingService.createVotingSession(payload));
            const votingSessionId = sessionResponse.id;

            const optionsPayload = this.options
                .filter(opt => opt.value.trim() !== '')
                .map(opt => ({name: opt.value, session_id: votingSessionId}));

            const requests = optionsPayload.map(opt =>
                firstValueFrom(this.votingService.createOption(votingSessionId, opt))
            );

            await Promise.all(requests);

            alert('Voting session and options created successfully!');
            this.router.navigate(['/voting-sessions']);
        } catch (err) {
            console.error('Error:', err);
            alert('Failed to create voting session or options.');
        }
    }

    private normalizeDatetime(dateStr: string): string {
        return dateStr.includes(':') && dateStr.split(':').length === 2 ? `${dateStr}:00` : dateStr;
    }
}
