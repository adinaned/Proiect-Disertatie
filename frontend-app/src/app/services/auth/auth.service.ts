import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {catchError, firstValueFrom, of, switchMap} from 'rxjs';

@Injectable({providedIn: 'root'})
export class AuthService {
    constructor(private http: HttpClient) {
    }

    isLoggedIn(): boolean {
        return typeof window !== 'undefined' && !!localStorage.getItem('token');
    }

    async isAdmin(): Promise<boolean> {
        if (typeof window === 'undefined') return false;

        const userDataString = localStorage.getItem('user');
        if (!userDataString) return false;

        try {
            const userData = JSON.parse(userDataString);
            const email = userData?.email;
            if (!email) return false;

            return await firstValueFrom(
                this.http.get<any>(`http://127.0.0.1:5000/emails/${email}`).pipe(
                    switchMap(emailRes => {
                        const userId = emailRes?.user_id;
                        if (!userId) return of(false);

                        return this.http.get<any>(`http://127.0.0.1:5000/users/${userId}`).pipe(
                            switchMap(userRes => {
                                const roleId = userRes?.role_id;
                                if (!roleId) return of(false);

                                return this.http.get<any>(`http://127.0.0.1:5000/roles/${roleId}`).pipe(
                                    switchMap(roleRes => {
                                        const roleName = roleRes?.name?.toLowerCase();
                                        return of(roleName === 'admin');
                                    }),
                                    catchError(() => of(false))
                                );
                            }),
                            catchError(() => of(false))
                        );
                    }),
                    catchError(() => of(false))
                )
            );
        } catch {
            return false;
        }
    }
}