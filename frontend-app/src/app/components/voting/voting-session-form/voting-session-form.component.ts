import {Component} from '@angular/core';
import {NgForOf, NgIf} from "@angular/common";
import {ActivatedRoute} from '@angular/router';
import {Router} from '@angular/router';

import {VotingSessionFormService} from '../../../services/voting/voting-session-form.service';
import {LsagService} from '../../../services/voting/votes/lsag.service';
import {VoteService} from '../../../services/voting/votes/vote.service';
import {AuthService} from '../../../services/auth/auth.service';
import {UserService} from '../../../services/users/user.service';
import {encryptPrivateKey} from '../../../services/voting/votes/private-key-encryption';
import {firstValueFrom} from "rxjs";

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
    popupType: 'confirm' | 'uploadKey' | 'result' | null = null;
    uploadedKey: any = null;

    constructor(
        private route: ActivatedRoute,
        private votingService: VotingSessionFormService,
        private router: Router,
        private LSAGService: LsagService,
        private voteService: VoteService,
        private authService: AuthService,
        private userService: UserService
    ) {
    }

    ngOnInit(): void {
        const votingSessionId = String(this.route.snapshot.paramMap.get('id'));
        if (!votingSessionId) return;

        this.votingService.getSessionById(votingSessionId).subscribe({
            next: (sessionData: any) => {
                this.session = sessionData;

                this.votingService.getOptionsByVotingSessionId(votingSessionId).subscribe({
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
            error: (err: any) => {
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

    confirmVote() {
        this.popupType = 'uploadKey';
    }

    closePopup() {
        this.popupType = null;
    }

    async onKeyFileUpload(event: any) {
        const file = event.target.files[0];
        if (!file) return;

        try {
            const fileContent = await file.text();
            this.uploadedKey = JSON.parse(fileContent);
            this.submitVote();
        } catch (e) {
            console.error("Error at reading the json file:", e);
            alert("Invalid file.");
        }
    }

    async submitVote() {
        this.popupType = 'result';

        if (!this.selectedOption || !this.uploadedKey) {
            alert("Select an option and upload the file containing the keys!");
            return;
        }

        const optionId = this.selectedOption.id;
        const votingSessionId = String(this.route.snapshot.paramMap.get('id'));

        try {
            const ring = await firstValueFrom(this.voteService.getRing(votingSessionId));
            if (!Array.isArray(ring) || ring.length === 0) {
                console.error("Ring is empty or not valid");
                return;
            }

            const x = this.uploadedKey.public_key.x;
            const y = this.uploadedKey.public_key.y;

            console.log(ring)
            const index = ring.findIndex(p => p.x === x && p.y === y);
            const userKey = {
                x: BigInt(x),
                y: BigInt(y)
            };

            if (index === -1) {
                console.error('Public key not found in ring.');
                return;
            } else {
                console.log('Public key found in ring at index: ' + index);
            }

            const privateKey = BigInt(this.uploadedKey.private_key);

            const message = `${optionId}`;
            console.log("message", message);
            const signature = await this.LSAGService.generateLSAGSignature(
                message, ring, index, privateKey
            );

            const keyImage = this.LSAGService.generateKeyImage(userKey, privateKey);

            await firstValueFrom(this.voteService.submitVote({
                voting_session_id: votingSessionId,
                option_id: optionId,
                signature,
                key_image: keyImage
            }));

            console.log("Vote submitted successfully");

        } catch (err) {
            console.error("Error in vote submission flow:", err);
        }
    }

    backToHomepage() {
        this.router.navigate(['/voting-sessions']);
    }
}
