import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
    selector: 'app-profile',
    imports: [],
    templateUrl: './view-profile.component.html',
    styleUrls: ['../../../auth/components/shared/auth-form.component.css', '../shared/profile.component.css']
})

export class ViewProfileComponent {
    constructor(private router: Router) {}
}
