import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
    selector: 'app-edit-profile',
    imports: [],
    templateUrl: './edit-profile.component.html',
    styleUrls: ['../../../auth/components/shared/auth-form.component.css', '../shared/profile.component.css', 'edit-profile.component.css']
})

export class EditProfileComponent {
    constructor(private router: Router) {}
}
