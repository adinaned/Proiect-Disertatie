import {FormsModule} from '@angular/forms';
import {NgModule} from "@angular/core";
import {provideHttpClient, withFetch} from '@angular/common/http';
import {BrowserModule} from '@angular/platform-browser';
import {RouterModule, provideRouter} from '@angular/router';
import {CookieService} from 'ngx-cookie-service';

import {AppComponent} from './app.component';
import {routes} from './app/routes/app.routes';

@NgModule({
    declarations: [],
    imports: [
        BrowserModule,
        FormsModule,
        RouterModule.forRoot(routes),
        AppComponent
    ],
    providers: [
        provideHttpClient(withFetch()),
        provideRouter(routes),
        CookieService
    ]
})
export class AppModule {
}