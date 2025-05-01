import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
    selector: 'app-voting-sessions',
    imports: [],
    templateUrl: './voting-sessions.component.html',
    styleUrls: ['./voting-sessions.component.css']
})

export class VotingSessionsComponent {
    constructor(private router: Router) {}
}
