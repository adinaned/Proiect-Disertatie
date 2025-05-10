import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root'
})
export class UserService {
    userData: any = {};

    setBasicData(data: any) {
        this.userData = { ...this.userData, ...data };
    }

    setProfileData(data: any) {
        this.userData = { ...this.userData, ...data };
    }

    getUserData() {
        return this.userData;
    }

    clearData() {
        this.userData = {};
    }
}
