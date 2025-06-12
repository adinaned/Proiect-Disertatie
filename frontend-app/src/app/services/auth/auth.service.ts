import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {BehaviorSubject, catchError, firstValueFrom, of, switchMap} from 'rxjs';

@Injectable({providedIn: 'root'})
export class AuthService {
    private baseUrl = 'http://127.0.0.1:5000';
    private userSubject = new BehaviorSubject<any | null>(null);
    user$ = this.userSubject.asObservable();


    constructor(private http: HttpClient) {
    }

    setUser(user: any) {
        this.userSubject.next(user);
    }

    clearUser() {
        this.userSubject.next(null);
    }

    isAuthenticatedByCookie(): Promise<boolean> {
        return firstValueFrom(
            this.http.get<any>(`${this.baseUrl}/me`, { withCredentials: true }).pipe(
                switchMap((res) => {
                    this.setUser(res.data);
                    return of(true);
                }),
                catchError(() => {
                    this.clearUser();
                    return of(false);
                })
            )
        );
    }

    getCurrentUserFromCookie(): Promise<any | null> {
        return firstValueFrom(
            this.http.get<any>(`${this.baseUrl}/me`, { withCredentials: true }).pipe(
                switchMap(res => {
                    this.setUser(res.data);
                    return of(res.data);
                }),
                catchError(() => {
                    this.clearUser();
                    return of(null);
                })
            )
        );
    }

    getUser() {
        return this.userSubject.getValue();
    }

    isLoggedIn(): boolean {
        return !!this.getUser();
    }
}