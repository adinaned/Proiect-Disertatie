import {Component} from '@angular/core';
import {NgForOf, NgIf} from "@angular/common";
import {ActivatedRoute} from '@angular/router';
import {Router} from '@angular/router';

import {VotingSessionFormService} from '../../../services/voting/voting-session-form.service';
import {LsagService} from '../../../services/voting/votes/lsag.service';
import {VoteService} from '../../../services/voting/votes/vote.service';
import {encryptPrivateKey} from '../../../services/voting/votes/private-key-encryption';

@Component({
    selector: 'app-display-voting-session',
    imports: [
        NgIf,
        NgForOf
    ],
    templateUrl: './voting-session-form.component.html',
    styleUrls: ['./voting-session-form.component.css']
})
export class VotingSessionFormComponent {
    session: any;
    selectedOption: any = null;
    popupType: 'confirm' | 'result' | null = null;

    constructor(
        private route: ActivatedRoute,
        private votingService: VotingSessionFormService,
        private router: Router,
        private LSAGService: LsagService,
        private voteService: VoteService
    ) {
    }

    ngOnInit(): void {
        const sessionId = Number(this.route.snapshot.paramMap.get('id'));
        if (!sessionId) return;

        this.votingService.getSessionById(sessionId).subscribe({
            next: (sessionData) => {
                this.session = sessionData;

                this.votingService.getOptionsBySessionId(sessionId).subscribe({
                    next: (optionsData) => {
                        console.log('Options received:', optionsData);
                        this.session.options = optionsData.map((opt: any) => ({
                            id: opt.id,
                            name: opt.name || opt.text || 'Unnamed Option'
                        }));
                    },
                    error: (err) => {
                        console.error('Failed to load options', err);
                        this.session.options = [];
                    }
                });
            },
            error: (err) => {
                console.error('Failed to load voting session', err);
            }
        });
    }

    selectOption(option: any) {
        this.selectedOption = option;
    }

    openPopup() {
        this.popupType = 'confirm';
    }

    closePopup() {
        this.popupType = null;
    }

    async submitVote() {
        this.popupType = 'result';
        const password = "1234";

        if (!this.selectedOption) {
            alert("Please select an option before submitting your vote.");
            return;
        }

        const optionId = this.selectedOption.id;

        const keys = await this.voteService.generateKeypair();
        await this.savePrivateKeyToStorage(keys.privateKey, password);
        await this.savePublicKeyToStorage(keys.publicKey, password);

        const sessionId = Number(this.route.snapshot.paramMap.get('id'));

        const userData = JSON.parse(localStorage.getItem('user') || '{}');

        if (!userData.email) {
            console.error("No email in localStorage user object");
            return;
        }

        this.voteService.getRing(sessionId).subscribe({
            next: async (res) => {
                const ring = res.ring;
                console.log("Ring:" + ring);

                this.voteService.getEmailObj(userData.email).subscribe({
                    next: (response) => {
                        const userId = response.user_id;

                        this.voteService.submitPublicKey(sessionId, userId, keys.publicKey).subscribe({
                            next: () => {
                                console.log('Public key sent to backend.');

                                this.voteService.getPublicKey(sessionId, userId).subscribe({
                                    next: async (publicKey) => {
                                        const userKey = {
                                            x: publicKey.public_key_x,
                                            y: publicKey.public_key_y
                                        };
                                        console.log("User public key from backend:", userKey);

                                        const index = ring.findIndex(p =>
                                            p.x.toLowerCase() === userKey.x.toLowerCase() &&
                                            p.y.toLowerCase() === userKey.y.toLowerCase()
                                        );

                                        if (index === -1) {
                                            console.error('Public key not found in ring.');
                                            return;
                                        }

                                        const message = `${sessionId}|${optionId}`;
                                        const signature = await this.LSAGService.generateLSAGSignature(
                                            message,
                                            ring,
                                            index,
                                            keys.privateKey
                                        );
                                        console.log("Signature:", signature);

                                        const keyImage = this.LSAGService.generateKeyImage(userKey, keys.privateKey);
                                        console.log("Key image:", keyImage);

                                        this.voteService.submitVote({
                                            session_id: sessionId,
                                            option_id: optionId,
                                            signature,
                                            key_image: keyImage
                                        }).subscribe({
                                            next: () => console.log('Vote submitted successfully'),
                                            error: err => console.error('Failed to submit vote:', err)
                                        });
                                    },
                                    error: err => console.error('Failed to fetch public key:', err)
                                });
                            },
                            error: err => console.error('Error sending public key:', err)
                        });
                    },
                    error: err => console.error('Could not retrieve user ID from email:', err)
                });
            },
            error: err => console.error('Failed to fetch ring:', err)
        });
    }

    async savePrivateKeyToStorage(privateKey: string, password: string) {
        // const encrypted = await encryptPrivateKey(privateKey, password);
        // localStorage.setItem('privateKey', encrypted);
        localStorage.setItem('privateKey', privateKey);
    }

    async savePublicKeyToStorage(publicKey: { x: string; y: string }, password?: string): Promise<void> {
        localStorage.setItem('publicKey', JSON.stringify(publicKey));
    }

    backToHomepage() {
        this.router.navigate(['/voting-sessions']);
    }
}
