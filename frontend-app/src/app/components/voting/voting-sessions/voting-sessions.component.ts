import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {NgClass, NgForOf, NgIf} from '@angular/common';

import {VotingSessionsService} from '../../../services/voting/voting-sessions.service';
import {VoteService} from '../../../services/voting/votes/vote.service';

@Component({
    selector: 'app-voting-sessions',
    standalone: true,
    imports: [NgClass, NgForOf, NgIf],
    templateUrl: './voting-sessions.component.html',
    styleUrls: ['./voting-sessions.component.css']
})
export class VotingSessionsComponent implements OnInit {
    sessions: any[] = [];
    isAdmin: boolean = false;

    constructor(
        private router: Router,
        private votingSessionService: VotingSessionsService,
        private voteService: VoteService
    ) {
    }

    ngOnInit() {
        this.checkIfUserIsAdmin();
        this.votingSessionService.getAllVotingSessions().subscribe({
            next: (data) => {
                const now = new Date();
                this.sessions = data.map((session: any) => {
                    const start = new Date(session.start_datetime);
                    const end = new Date(session.end_datetime);
                    let status = 'closed';
                    let time_remaining = '';

                    if (!isNaN(start.getTime()) && !isNaN(end.getTime())) {
                        if (now < start) {
                            status = 'upcoming';
                            time_remaining = 'Opening in ' + this.calculateTimeRemaining(start);
                        } else if (now >= start && now <= end) {
                            status = 'open';
                            time_remaining = 'Voting session closes in ' + this.calculateTimeRemaining(end);
                        } else {
                            status = 'closed';
                        }
                    }

                    return {
                        ...session,
                        status,
                        time_remaining,
                        stats_url: 'https://voting_stats'
                    };
                });
            },
            error: (err) => {
                console.error('Error fetching voting sessions:', err);
            }
        });
    }

    checkIfUserIsAdmin(): void {
        const userData = localStorage.getItem('user');
        const email = userData ? JSON.parse(userData)?.email : null;
        if (!email) return;

        this.votingSessionService.getUserIdByEmail(email).subscribe({
            next: (emailRes) => {
                const userId = emailRes?.user_id;
                if (!userId) return;

                this.votingSessionService.getUserById(userId).subscribe({
                    next: (userRes) => {
                        const roleId = userRes?.role_id;
                        if (!roleId) return;

                        this.votingSessionService.getRoleById(roleId).subscribe({
                            next: (roleRes) => {
                                const roleName = roleRes?.name?.toLowerCase();
                                this.isAdmin = roleName === 'admin';
                            },
                            error: () => console.error('Error fetching role info.')
                        });
                    },
                    error: () => console.error('Error fetching user info.')
                });
            },
            error: () => console.error('Error fetching user ID from email.')
        });
    }

    deleteSession(sessionId: number): void {
        if (confirm('Are you sure you want to delete this voting session?')) {
            this.votingSessionService.deleteVotingSession(sessionId).subscribe({
                next: () => {
                    this.sessions = this.sessions.filter(s => s.id !== sessionId);
                    console.log(`Session ${sessionId} deleted`);
                },
                error: err => {
                    console.error('Failed to delete session:', err);
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


    private pad(n: number): string {
        return n < 10 ? '0' + n : '' + n;
    }

    handleVote(session: any) {
        this.router.navigate(['/voting-session-form', session.id]);
    }

    async handleAction(session: any) {
        const isRegistered = this.isRegistered(session.id);

        if (session.status === 'upcoming' && !isRegistered) {
            const keys = await this.voteService.generateKeypair();
            this.savePrivateKeyToStorage(session.id, keys.privateKey);
            this.savePublicKeyToStorage(session.id, keys.publicKey);

            const userData = JSON.parse(localStorage.getItem('user') || '{}');

            this.voteService.getEmailObj(userData.email).subscribe({
                next: (response) => {
                    const userId = response.user_id;

                    this.voteService.submitPublicKey(session.id, userId, keys.publicKey).subscribe({
                        next: () => console.log('Public key sent to backend.'),
                        error: (err) => console.error('Error sending public key:', err)
                    });
                },
                error: (err) => {
                    console.error('Could not retrieve user ID from email:', err);
                }
            });

            return;
        }

        if (session.status === 'open' && isRegistered) {
            this.handleVote(session);
            return;
        }

        console.warn('No action possible for this session.');
    }

    getButtonClass(session: any): string {
        return this.isButtonDisabled(session) ? 'vote-btn greyed-out' : 'vote-btn';
    }

    getButtonLabel(session: any): string {
        const isRegistered = this.isRegistered(session.id);

        if (session.status === 'closed') {
            return 'Closed';
        }
        if (session.status === 'upcoming') {
            return isRegistered ? 'Vote' : 'Register to Vote';
        }
        if (session.status === 'open') {
            return isRegistered ? 'Vote' : 'Unavailable';
        }
        if (session.status === 'submitted') {
            return 'Voted';
        }

        return 'Unavailable';
    }

    isButtonDisabled(session: any): boolean {
        const isRegistered = this.isRegistered(session.id);

        if (session.status === 'open') {
            return !isRegistered;
        }
        if (session.status === 'upcoming') {
            return isRegistered;
        }

        return true;
    }

    isRegistered(sessionId: number): boolean {
        return !!localStorage.getItem(`privateKey_${sessionId}`);
    }

    async savePrivateKeyToStorage(sessionId: number, privateKey: string) {
        localStorage.setItem(`privateKey_${sessionId}`, privateKey);
        console.log(`Private key saved for session ${sessionId}`);
    }

    async savePublicKeyToStorage(sessionId: number, publicKey: { x: string; y: string }) {
        localStorage.setItem(`publicKey_${sessionId}`, JSON.stringify(publicKey));
        // await this.voteService.sendPublicKey(sessionId, publicKey).toPromise();
        console.log('Public key sent for session ${sessionId}');
    }
}
