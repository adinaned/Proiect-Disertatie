import {Component} from '@angular/core';
import {Router} from '@angular/router';
import {NgIf} from "@angular/common";
import {FormsModule} from '@angular/forms';
import {ChangePasswordService} from '../../../services/user-profile/change-password.service';

@Component({
    selector: 'app-edit-auth-auth',
    standalone: true,
    imports: [FormsModule, NgIf],
    templateUrl: './change-password.component.html',
    styleUrls: ['../../auth/shared/auth-form.component.css', 'change-password.component.css']
})

export class ChangePasswordComponent {
    oldPassword = '';
    newPassword = '';
    confirmPassword = '';
    showWarning = false;
    warningMessage = '';
    hasUnsavedChanges = false;
    successMessage = '';

    constructor(
        private router: Router,
        private changePasswordService: ChangePasswordService
    ) {
    }

    onSubmit(): void {
        this.showWarning = false;
        this.successMessage = '';

        if (this.newPassword !== this.confirmPassword) {
            this.warningMessage = 'New passwords do not match.';
            this.showWarning = true;
            return;
        }

        if (this.oldPassword === this.newPassword) {
            this.warningMessage = 'New password must be different from the old password.';
            this.showWarning = true;
            return;
        }

        console.log(this.oldPassword);
        console.log(this.newPassword);
        console.log(this.confirmPassword);


        this.changePasswordService.changePassword(this.oldPassword, this.newPassword).subscribe({
            next: () => {
                this.successMessage = 'Changes saved successfully!';
                this.hasUnsavedChanges = false;
                this.oldPassword = '';
                this.newPassword = '';
                this.confirmPassword = '';
            },
            error: (error) => {
                this.warningMessage = error.error?.message || 'Password update failed.';
                this.showWarning = true;
            }
        });
    }

    markDirty() {
        this.hasUnsavedChanges = true;
        this.successMessage = '';
    }

    onCancel(): void {
        this.hasUnsavedChanges = false;
        this.oldPassword = '';
        this.newPassword = '';
        this.confirmPassword = '';
        this.successMessage = '';
        this.warningMessage = '';
        this.router.navigate(['/change-password']);
    }
}
