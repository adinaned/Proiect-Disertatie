import {FormsModule} from '@angular/forms';
import {NgModule} from "@angular/core";
import {BrowserModule} from '@angular/platform-browser';
import {RouterModule} from '@angular/router';
import { routes } from './app/routes/app.routes';

import {AppComponent} from './app.component';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { provideRouter } from '@angular/router';

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
        provideRouter(routes)
    ]
})
export class AppModule {
}