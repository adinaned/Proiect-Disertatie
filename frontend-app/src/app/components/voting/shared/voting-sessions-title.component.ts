import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
    selector: 'app-voting-session-form-title',
    imports: [],
    templateUrl: './voting-session-form-title.component.html',
    styleUrls: ['./voting-sessions-title.component.css']
})

export class VotingSessionsTitleComponent {
    constructor(private router: Router) {}
}
