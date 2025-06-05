import {Injectable} from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from '@angular/common/http';

@Injectable({providedIn: 'root'})
export class RegisterAccountService {
    private profileDraftData: any = {};
    private emailData: any = {};
    private passwordData: any = {};
    private baseUrl = 'http://127.0.0.1:5000';

    constructor(private http: HttpClient) {
    }

    getEmail(email: string): Observable<boolean> {
        return this.http.get<boolean>(`${this.baseUrl}/emails/${email}`);
    }

    setAccountData(data: any, passwordData: any, emailData: any) {
        this.profileDraftData = {...this.profileDraftData, ...data};
        this.passwordData = {...this.passwordData, ...passwordData}
        this.emailData = {...this.emailData, ...emailData};
    }

    getProfileDraftData(): any {
        return this.profileDraftData;
    }

    getPasswordData(): any {
        return this.passwordData;
    }

    getEmailData(): any {
        return this.emailData;
    }

    hasValidUserData(): boolean {
        return this.profileDraftData &&
            this.profileDraftData.first_name &&
            this.profileDraftData.last_name &&
            this.emailData &&
            this.passwordData;
    }

    clear() {
        this.profileDraftData = {};
        this.passwordData = {};
        this.emailData = {};
    }
}
