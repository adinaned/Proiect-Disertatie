import {Injectable} from '@angular/core';
import {Observable, switchMap} from 'rxjs';
import {HttpClient} from '@angular/common/http';

@Injectable({providedIn: 'root'})
export class RegisterProfileService {
    constructor(private http: HttpClient) {
    }

    private baseUrl = 'http://127.0.0.1:5000';

    postProfile(data: any): Observable<any> {
        console.log('Payload for registerProfile:', data);
        return this.http.post(`${this.baseUrl}/users`, data);
    }

    registerEmail(emailData: any): Observable<any> {
        console.log('Payload for registerEmail:', emailData);
        return this.http.post(`${this.baseUrl}/emails`, emailData);
    }

    registerPassword(passwordData: any): Observable<any> {
        console.log('Payload for registerPassword:', passwordData);
        return this.http.post(`${this.baseUrl}/passwords`, passwordData);
    }

    registerProfile(profileData: any, passwordData: any, emailData: any): Observable<any> {
        return this.postProfile(profileData).pipe(
            switchMap((profileResponse) => {
                const userId = profileResponse.id;

                const updatedEmailData = {
                    ...emailData,
                    user_id: userId
                };

                const updatedPasswordData = {
                    ...passwordData,
                    user_id: userId
                };

                return this.registerEmail(updatedEmailData).pipe(
                    switchMap(() => this.registerPassword(updatedPasswordData))
                );
            })
        );
    }

    // getProfile(userId: string): Observable<any> {
    //     return this.getUserProfile(userId);
    // }
    //
    // updateProfile(userId: string, newData: any): Observable<any> {
    //     return this.api.updateUserProfile(userId, newData);
    // }
}
