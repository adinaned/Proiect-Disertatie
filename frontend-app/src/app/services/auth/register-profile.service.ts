import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';

@Injectable({providedIn: 'root'})
export class RegisterProfileService {
    constructor(private http: HttpClient) {
    }

    private baseUrl = 'http://127.0.0.1:5000';

    registerProfile(data: any): Observable<any> {
        console.log('Payload for registerProfile:', data);
        return this.http.post(`${this.baseUrl}/users`, data);
    }

    getOrganizationByName(name: string): Observable<any> {
        return this.http.get(`${this.baseUrl}/organizations/${name}`);
    }

    getCountryByName(name: string): Observable<any> {
        return this.http.get(`${this.baseUrl}/countries/${name}`);
    }

    getAllCountries(): Observable<any> {
        return this.http.get(`${this.baseUrl}/countries`);
    }
}
