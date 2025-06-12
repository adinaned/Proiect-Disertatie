import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {NgClass, NgForOf, NgIf} from '@angular/common';

import {VotingSessionsService} from '../../../services/voting/voting-sessions.service';
import {VoteService} from '../../../services/voting/votes/vote.service';
import {AuthService} from "../../../services/auth/auth.service";
import {UserService} from "../../../services/users/user.service";
import {LsagService} from "../../../services/voting/votes/lsag.service";

@Component({
    selector: 'app-voting-sessions',
    standalone: true,
    imports: [NgClass, NgForOf, NgIf],
    templateUrl: './voting-sessions.component.html',
    styleUrls: ['./voting-sessions.component.css']
})
export class VotingSessionsComponent implements OnInit {
    votingSessions: any[] = [];
    isAdmin: boolean = false;
    profileStatus: string = '';
    profileActivatedAt: Date | null = null;

    constructor(
        private router: Router,
        private votingSessionsService: VotingSessionsService,
        private voteService: VoteService,
        private authService: AuthService,
        private userService: UserService,
        private lsagService: LsagService
    ) {
    }

    ngOnInit() {
        this.authService.getCurrentUserFromCookie().then(user => {
            console.log('Current user:', user.user_id);
            this.checkIfUserIsAdmin(user.user_id);
            this.loadUserProfileStatus(user.user_id);
        });
    }

    loadUserProfileStatus(userId: number) {
        this.votingSessionsService.getProfileStatus(userId).subscribe({
            next: (profileRes) => {
                this.profileStatus = profileRes?.name?.toUpperCase();
                this.profileActivatedAt = new Date(profileRes.updated_at);
                this.loadVotingSessions();
            },
            error: () => console.error('Error fetching profile status.')
        });
    }

    loadVotingSessions() {
        if (this.profileStatus !== 'ACTIVE') {
            console.warn('User profile is not ACTIVE, voting sessions will not be shown.');
            this.votingSessions = [];
            return;
        }

        this.authService.getCurrentUserFromCookie().then(currentUser => {
            const userId = currentUser?.user_id;
            if (!userId) {
                console.error('User ID not found in cookie.');
                return;
            }

            this.userService.getUserById(userId).subscribe(userDetails => {
                const organizationId = userDetails?.organization_id;
                const roleId = userDetails?.role_id;

                if (!organizationId) {
                    console.error('Organization ID not found for user.');
                    return;
                }

                const now = new Date();

                let sessions$;
                if (this.isAdmin) {
                    sessions$ = this.votingSessionsService.getVotingSessionsByOrganization(organizationId);
                } else {
                    if (!roleId) {
                        console.error('Role ID not found for non-admin user.');
                        return;
                    }
                    sessions$ = this.votingSessionsService.getVotingSessionsByOrganizationAndRole(organizationId, roleId);
                }

                sessions$.subscribe({
                    next: async (data) => {
                        let filteredVotingSessions = data;

                        if (this.profileStatus === 'OPEN') {
                            filteredVotingSessions = [];
                        } else if (this.profileStatus === 'ACTIVE' && this.profileActivatedAt && !this.isAdmin) {
                            filteredVotingSessions = data.filter((session: any) => {
                                const start = new Date(session.start_datetime);
                                return start > this.profileActivatedAt!;
                            });
                        }

                        this.votingSessions = await Promise.all(
                            filteredVotingSessions.map(async (session: any) => {
                                const start = new Date(session.start_datetime);
                                const end = new Date(session.end_datetime);

                                let status = 'closed';
                                let time_remaining = '';
                                let ringSize = 0;

                                try {
                                    const ringResponse = await this.voteService.getRing(session.id).toPromise();
                                    ringSize = ringResponse?.length || 0;

                                    if (!isNaN(start.getTime()) && !isNaN(end.getTime())) {
                                        if (now < start) {
                                            status = 'upcoming';
                                            time_remaining = 'Opening in ' + this.calculateTimeRemaining(start);
                                        } else if (now >= start && now <= end) {
                                            if (ringSize < 3) {
                                                status = 'closed';
                                                time_remaining = 'Not enough participants to start the session.';
                                            } else {
                                                status = 'open';
                                                time_remaining = 'Voting session closes in ' + this.calculateTimeRemaining(end);
                                            }
                                        }
                                    }
                                } catch (e) {
                                    console.warn(`Failed to fetch ring for session ${session.id}:`, e);
                                    status = 'closed';
                                    time_remaining = 'Could not retrieve key ring.';
                                }

                                const isVoterRegistered = await this.isRegistered(session.id, userId);

                                return {
                                    ...session,
                                    status,
                                    time_remaining,
                                    start_date: start,
                                    end_date: end,
                                    isVoterRegistered,
                                    stats_url: 'https://voting_stats'
                                };
                            })
                        );
                        this.sortVotingSessions();
                    },
                    error: (err) => {
                        console.error('Error fetching voting sessions:', err);
                    }
                });
            });

        }).catch(err => {
            console.error('Error retrieving user from cookie:', err);
        });
    }

    sortVotingSessions(): void {
        this.votingSessions = [
            ...this.votingSessions
                .filter(s => s.status === 'upcoming' && !s.isVoterRegistered)
                .sort((a, b) => a.start_date.getTime() - b.start_date.getTime()),

            ...this.votingSessions
                .filter(s => s.status === 'open' && s.isVoterRegistered)
                .sort((a, b) => a.end_date.getTime() - b.end_date.getTime()),

            ...this.votingSessions
                .filter(s => s.status === 'upcoming' && s.isVoterRegistered)
                .sort((a, b) => a.start_date.getTime() - b.start_date.getTime()),

            ...this.votingSessions
                .filter(s => s.status === 'open' && !s.isVoterRegistered)
                .sort((a, b) => a.end_date.getTime() - b.end_date.getTime()),

            ...this.votingSessions
                .filter(s => s.status === 'closed')
                .sort((a, b) => b.end_date.getTime() - a.end_date.getTime())
        ];
    }


    checkIfUserIsAdmin(user_id: any): void {
        this.userService.getUserById(user_id).subscribe({
            next: (userRes) => {
                const roleId = userRes?.role_id;
                if (!roleId) return;

                this.userService.getRoleById(roleId).subscribe({
                    next: (roleRes) => {
                        const roleName = roleRes?.name?.toLowerCase();
                        this.isAdmin = roleName === 'admin';
                        console.log("User is admin?", this.isAdmin);
                    },
                    error: () => console.error('Error fetching role info.')
                });
            },
            error: () => console.error('Error fetching user details.')
        });
    }


    deleteVotingSession(votingSessionId: number): void {
        if (confirm('Are you sure you want to delete this voting votingSession?')) {
            this.votingSessionsService.deleteVotingSession(votingSessionId).subscribe({
                next: () => {
                    this.votingSessions = this.votingSessions.filter(s => s.id !== votingSessionId);
                    console.log(`votingSession ${votingSessionId} deleted`);
                },
                error: err => {
                    console.error('Failed to delete voting session:', err);
                }
            });
        }
    }

    getStatusClass(status: string): string {
        return status;
    }

    private calculateTimeRemaining(target: Date): string {
        const now = new Date();
        const diffMs = target.getTime() - now.getTime();

        if (diffMs <= 0) return 'Expired';

        const seconds = Math.floor((diffMs / 1000) % 60);
        const minutes = Math.floor((diffMs / 1000 / 60) % 60);
        const hours = Math.floor((diffMs / 1000 / 60 / 60) % 24);
        const days = Math.floor(diffMs / 1000 / 60 / 60 / 24);

        const parts: string[] = [];

        if (days > 0) parts.push(`${days} day${days !== 1 ? 's' : ''}`);
        if (hours > 0) parts.push(`${hours} hour${hours !== 1 ? 's' : ''}`);
        if (minutes > 0) parts.push(`${minutes} minute${minutes !== 1 ? 's' : ''}`);
        if (days === 0 && hours === 0 && minutes === 0 && seconds > 0)
            parts.push(`${seconds} second${seconds !== 1 ? 's' : ''}`);

        return parts.join(', ');
    }

    handleVote(votingSession: any) {
        this.router.navigate(['/voting-session-form', votingSession.id]);
    }

    async handleAction(votingSession: any) {
        const user = await this.authService.getCurrentUserFromCookie();
        if (!user || !user.user_id) {
            console.error('User not authenticated');
            return;
        }

        const userId = user.user_id;
        const isRegistered = await this.isRegistered(votingSession.id, userId);

        if (votingSession.status === 'upcoming' && !isRegistered) {
            const keys = await this.lsagService.generateKeypair();

            this.authService.getCurrentUserFromCookie().then(user => {
                const userId = user.user_id;
                this.voteService.submitPublicKey(votingSession.id, userId, keys.publicKey).subscribe({
                    next: () => {
                        console.log('Public key sent to backend.');
                        votingSession.isVoterRegistered = true;
                        this.sortVotingSessions();

                        alert("Your voting key has been generated. Save the file and don't lose it!");

                        const keyFile = {
                            voting_session_id: votingSession.id,
                            public_key: {
                                x: keys.publicKey.x.toString(),
                                y: keys.publicKey.y.toString(),
                            },
                            private_key: keys.privateKey.toString()
                        };

                        const jsonBlob = new Blob([JSON.stringify(keyFile, null, 2)], {type: 'application/json'});
                        const url = window.URL.createObjectURL(jsonBlob);

                        const link = document.createElement('a');
                        link.href = url;
                        link.download = `voting_key_${votingSession.id}.json`;
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                    },
                    error: (err) => console.error('Error sending public key:', err)
                });
            }).catch(err => {
                console.error('Error getting user from cookie:', err);
            });

            return;
        }

        if (votingSession.status === 'open' && isRegistered) {
            this.handleVote(votingSession);
            return;
        }

        console.warn('No action possible for this votingSession.');
    }

    getButtonClass(votingSession: any): string {
        if (!this.isAdmin) {
            return this.isButtonDisabled(votingSession) ? 'vote-btn greyed-out' : 'vote-btn';
        } else {
            return votingSession.status !== 'upcoming' ? 'delete-btn greyed-out' : 'delete-btn';
        }
    }

    getButtonLabel(votingSession: any): string {
        const isRegistered = votingSession.isVoterRegistered;

        if (votingSession.status === 'closed') {
            return 'Closed';
        }
        if (votingSession.status === 'upcoming') {
            return isRegistered ? 'Vote' : 'Register to Vote';
        }
        if (votingSession.status === 'open') {
            return isRegistered ? 'Vote' : 'Not Registered';
        }
        if (votingSession.status === 'submitted') {
            return 'Voted';
        }

        return 'Unavailable';
    }

    isButtonDisabled(votingSession: any): boolean {
        const isRegistered = votingSession.isVoterRegistered;

        if (votingSession.status === 'open') {
            return !isRegistered;
        }
        if (votingSession.status === 'upcoming') {
            return isRegistered;
        }

        return true;
    }

    isRegistered(sessionId: string, userId: string): Promise<boolean> {
        return new Promise((resolve) => {
            this.voteService.checkIfRegistered(sessionId, userId).subscribe({
                next: (res) => {
                    resolve(res.status === 200);
                },
                error: (err) => {
                    if (err.status === 404) {
                        resolve(false);
                    } else {
                        console.error('Error checking registration:', err);
                        resolve(false);
                    }
                }
            });
        });
    }
}
