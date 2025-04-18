import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
    selector: 'app-profile',
    imports: [],
    templateUrl: './profile.component.html',
    styleUrls: ['../auth/components/shared/auth-form.component.css', './profile.component.css']
})

export class ProfileComponent {
    constructor(private router: Router) {}
}
