import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable, from, switchMap, throwError} from 'rxjs';
import {AuthService} from '../auth/auth.service';

@Injectable({
    providedIn: 'root'
})
export class ChangePasswordService {
    private baseUrl = 'http://127.0.0.1:5000';

    constructor(private http: HttpClient, private authService: AuthService) {
    }

    changePassword(oldPassword: string, newPassword: string): Observable<any> {
        return from(this.authService.getCurrentUserFromCookie()).pipe(
            switchMap(user => {
                if (!user?.user_id) {
                    throw new Error('User ID not found in cookie');
                }

                return this.http.patch(`${this.baseUrl}/passwords/${user.user_id}`, {
                    old_password: oldPassword,
                    new_password: newPassword
                });
            })
        );
    }
}