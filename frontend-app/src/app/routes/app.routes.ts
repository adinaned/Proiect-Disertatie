import { Routes } from '@angular/router';
import { LoginComponent } from '../shared/auth/components/login/login.component';
import { ForgotPasswordComponent } from '../shared/auth/components/forgot-password/forgot-password.component';
import { RegisterAccountComponent } from '../shared/auth/components/register-account/register-account.component';
import { RegisterProfileComponent } from '../shared/auth/components/register-profile/register-profile.component';
import { ProfileComponent } from '../shared/profile/profile.components';
// import { Token } from '../user/components/token/token';
// import { VotingSessionDetailComponent } from '../user/components/voting-sessions/voting-session-detail.component';
import { VotingSessionsComponent } from '../shared/voting/voting-sessions/components/voting-sessions.component';

export const routes: Routes = [
    { path: '', component: LoginComponent },
    { path: 'login', component: LoginComponent },
    { path: 'register-account', component: RegisterAccountComponent },
    { path: 'register-profile', component: RegisterProfileComponent },
    { path: 'forgot-password', component: ForgotPasswordComponent },
    { path: 'register-account-form', component: RegisterProfileComponent },
    { path: 'profile', component: ProfileComponent },
    // { path: 'token', component: Token },
    // { path: 'voting-session-detail', component: VotingSessionDetailComponent },
    { path: 'voting-sessions', component: VotingSessionsComponent },
];



