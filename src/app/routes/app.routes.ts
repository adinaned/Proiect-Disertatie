import { Routes } from '@angular/router';
import { LoginComponent } from '../shared/auth/components/login/login.component';
import { ForgotPasswordComponent } from '../shared/auth/components/forgot-password/forgot-password.component';
import { RegisterAccountComponent } from '../shared/auth/components/register-account/register-account.component';
import { RegisterProfileComponent } from '../shared/auth/components/register-profile/register-profile.component';
import { UserProfileComponent } from '../user/components/user-profile/user-profile.component';
import { Token } from '../user/components/token/token';
import { VotingSessionDetailComponent } from '../user/components/voting-sessions/voting-session-detail.component';
import { VotingSessionsListComponent } from '../user/components/voting-sessions/voting-sessions-list.component';

export const routes: Routes = [
    { path: '', component: LoginComponent },
    { path: 'login', component: LoginComponent },
    { path: 'register-account', component: RegisterAccountComponent },
    { path: 'register-profile', component: RegisterProfileComponent },
    { path: 'forgot-password', component: ForgotPasswordComponent },
    { path: 'register-account-form', component: RegisterProfileComponent },
    { path: 'user-profile', component: UserProfileComponent },
    { path: 'token', component: Token },
    { path: 'voting-session-detail', component: VotingSessionDetailComponent },
    { path: 'voting-sessions-list', component: VotingSessionsListComponent },
];



