import { AuthGuard } from '../../auth-guard/auth.guard';

import { Routes } from '@angular/router';
import { LoginComponent } from '../components/auth/login/login.component';
import { ForgotPasswordComponent } from '../components/auth/forgot-password/forgot-password.component';
import { RegisterAccountComponent } from '../components/auth/register-account/register-account.component';
import { RegisterProfileComponent } from '../components/auth/register-profile/register-profile.component';
import { ViewProfileComponent } from '../components/user-profile/view-profile/view-profile.component';
import { ChangePasswordComponent } from '../components/user-profile/change-password/change-password.component';
import { StatisticsComponent } from '../components/voting/statistics/statistics.component';
import { VotingSessionFormComponent } from '../components/voting/voting-session-form/voting-session-form.component';
import { VotingSessionsComponent } from '../components/voting/voting-sessions/voting-sessions.component';
import { CreateVotingSessionComponent } from '../components/voting/create-voting-session/create-voting-session.component';

export const routes: Routes = [
    { path: '', component: LoginComponent },
    { path: 'login', component: LoginComponent },
    { path: 'register-account', component: RegisterAccountComponent },
    { path: 'register-profile', component: RegisterProfileComponent},
    { path: 'forgot-password', component: ForgotPasswordComponent },
    { path: 'profile', component: ViewProfileComponent, canActivate: [AuthGuard]},
    { path: 'change-password', component: ChangePasswordComponent, canActivate: [AuthGuard]},
    { path: 'statistics', component: StatisticsComponent},
    { path: 'voting-session-form/:id', component: VotingSessionFormComponent, canActivate: [AuthGuard]},
    { path: 'voting-sessions', component: VotingSessionsComponent, canActivate: [AuthGuard]},
    { path: 'create-voting-sessions', component: CreateVotingSessionComponent },
];



