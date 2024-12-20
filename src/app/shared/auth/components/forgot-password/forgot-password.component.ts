import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
    selector: 'app-forgot-password',
    imports: [],
    templateUrl: './forgot-password.component.html',
    styleUrls: ['../shared/auth-form.component.css', './forgot-password.component.css']
})

export class ForgotPasswordComponent {
    constructor(private router: Router) {}

    handleLogin() {
        console.log("Switching to 'Log In' tab");
        this.router.navigate(['/login']);
    }
}
