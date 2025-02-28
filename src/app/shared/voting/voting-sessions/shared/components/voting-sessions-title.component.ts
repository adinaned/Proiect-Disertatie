import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
    selector: 'app-voting-sessions-title',
    imports: [],
    templateUrl: './voting-sessions-title.component.html',
    styleUrls: ['./voting-sessions-title.component.css']
})

export class VotingSessionsTitleComponent {
    constructor(private router: Router) {}
}
