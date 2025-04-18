import { Component } from '@angular/core';

@Component({
    selector: 'app-forgot-password',
    imports: [
    ],
    templateUrl: './user-profile.component.html',
    styleUrl: './user-profile.component.css'
})

export class UserProfileComponent {
  isDropdownVisible = false;

  toggleDropdown(): void {
    this.isDropdownVisible = !this.isDropdownVisible;
  }

  logout(): void {
    console.log('User logged out');
  }
}
