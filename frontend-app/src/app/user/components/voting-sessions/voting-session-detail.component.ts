import { Component } from '@angular/core';
import {NgIf} from "@angular/common";

@Component({
    selector: 'app-display-voting-session',
    imports: [
        NgIf
    ],
    templateUrl: './voting-session-detail.component.html',
    styleUrls: ['./voting-session-detail.component.css']
})
export class VotingSessionDetailComponent {
    popupType: 'confirm' | 'result' | null = null;

    openPopup() {
        this.popupType = 'confirm';
    }

    closePopup() {
        this.popupType = null;
    }

    submitVote() {
        this.popupType = 'result';
    }
}
