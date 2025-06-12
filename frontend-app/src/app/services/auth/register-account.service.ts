import {Injectable} from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from '@angular/common/http';

@Injectable({providedIn: 'root'})
export class RegisterAccountService {
    private profileDraftData: any = {};
    private baseUrl = 'http://127.0.0.1:5000';

    constructor(private http: HttpClient) {
    }

    getEmail(email: string): Observable<boolean> {
        return this.http.get<boolean>(`${this.baseUrl}/emails/${email}`);
    }

    setAccountData(data: any) {
        this.profileDraftData = {...this.profileDraftData, ...data};
    }

    getProfileDraftData(): any {
        return this.profileDraftData;
    }

    hasValidUserData(): boolean {
        return this.profileDraftData &&
            this.profileDraftData.first_name &&
            this.profileDraftData.last_name &&
            this.profileDraftData.email_address &&
            this.profileDraftData.password;
    }

    clear() {
        this.profileDraftData = {};
    }
}
