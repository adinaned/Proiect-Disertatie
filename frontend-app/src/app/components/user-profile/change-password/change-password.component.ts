import {Component} from '@angular/core';
import {Router} from '@angular/router';
import {HttpClient} from '@angular/common/http';
import {FormsModule} from '@angular/forms';
import {NgIf} from "@angular/common";

@Component({
    selector: 'app-edit-auth-auth',
    standalone: true,
    imports: [FormsModule, NgIf],
    templateUrl: './change-password.component.html',
    styleUrls: ['../../auth/shared/auth-form.component.css', 'change-password.component.css']
})
export class ChangePasswordComponent {
    oldPassword: string = '';
    newPassword: string = '';
    confirmPassword: string = '';
    showWarning: boolean = false;
    warningMessage: string = '';
    hasUnsavedChanges: boolean = false;
    showOldPassword = false;
    showNewPassword = false;
    showConfirmPassword = false;
    successMessage: string = '';

    constructor(private http: HttpClient, private router: Router) {
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

        const emailData = localStorage.getItem('user');
        const email = emailData ? JSON.parse(emailData)?.email : null;
        console.log('email', email);

        if (!email) {
            this.warningMessage = 'User email not found.';
            this.showWarning = true;
            return;
        }

        this.http.get<any>(`http://127.0.0.1:5000/emails/${email}`).subscribe({
            next: (emailResponse) => {
                const userId = emailResponse?.user_id;

                if (!userId) {
                    this.warningMessage = 'User ID not found for given email.';
                    this.showWarning = true;
                    return;
                }

                this.http.put<any>(`http://127.0.0.1:5000/passwords/${userId}`, {
                    new_password: this.newPassword
                }).subscribe({
                    next: () => {
                        this.successMessage = 'Changes saved successfully!';
                        this.hasUnsavedChanges = false;
                        this.oldPassword = '';
                        this.newPassword = '';
                        this.confirmPassword = '';
                    },
                    error: err => {
                        this.warningMessage = err.error?.message || 'Password update failed.';
                        this.showWarning = true;
                    }
                });
            },
            error: err => {
                this.warningMessage = err.error?.message || 'Failed to retrieve user ID.';
                this.showWarning = true;
            }
        });
    }

    markDirty() {
        this.hasUnsavedChanges = true;
        this.successMessage = '';
    }

    // toggleOldPassword() {
    //     this.showOldPassword = !this.showOldPassword;
    // }
    // toggleNewPassword() {
    //     this.showNewPassword = !this.showNewPassword;
    // }
    // toggleConfirmPassword() {
    //     this.showConfirmPassword = !this.showConfirmPassword;
    // }

    onCancel(): void {
        this.hasUnsavedChanges = false;
        this.oldPassword = '';
        this.newPassword = '';
        this.confirmPassword = '';
        this.successMessage = '';
        this.warningMessage = ''
        this.router.navigate(['/change-password']);
    }
}
