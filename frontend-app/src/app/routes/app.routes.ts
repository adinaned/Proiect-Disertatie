import {AdminGuard} from '../../guards/admin.guard';
import {AuthGuard} from '../../guards/auth.guard';
import {GuestGuard} from '../../guards/guest.guard';

// import {AdminGuard} from '../../admin-guard/admin.guard';

import {Routes} from '@angular/router';
import {LoginComponent} from '../components/auth/login/login.component';
import {ForgotPasswordComponent} from '../components/auth/forgot-password/forgot-password.component';
import {RegisterAccountComponent} from '../components/auth/register-account/register-account.component';
import {RegisterProfileComponent} from '../components/auth/register-profile/register-profile.component';
import {ViewProfileComponent} from '../components/user-profile/view-profile/view-profile.component';
import {ChangePasswordComponent} from '../components/user-profile/change-password/change-password.component';
import {StatisticsComponent} from '../components/voting/statistics/statistics.component';
import {VotingSessionFormComponent} from '../components/voting/voting-session-form/voting-session-form.component';
import {VotingSessionsComponent} from '../components/voting/voting-sessions/voting-sessions.component';
import {CreateVotingSessionComponent} from '../components/voting/create-voting-session/create-voting-session.component';
import {UserProfilesComponent} from '../components/admin-user-profiles/user-profiles/user-profiles.component';
import {
    ViewUserProfileComponent
} from '../components/admin-user-profiles/view-user-profile/view-user-profile.component';


export const routes: Routes = [
    {path: '', component: LoginComponent, canActivate: [GuestGuard]},
    {path: 'login', component: LoginComponent, canActivate: [GuestGuard]},
    {path: 'register-account', component: RegisterAccountComponent, canActivate: [GuestGuard]},
    {path: 'register-profile', component: RegisterProfileComponent, canActivate: [GuestGuard]},
    {path: 'forgot-password', component: ForgotPasswordComponent, canActivate: [GuestGuard]},

    {path: 'profile', component: ViewProfileComponent, canActivate: [AuthGuard]},
    {path: 'change-password', component: ChangePasswordComponent, canActivate: [AuthGuard]},
    {path: 'statistics', component: StatisticsComponent, canActivate: [AuthGuard]},
    {path: 'voting-session-form/:id', component: VotingSessionFormComponent, canActivate: [AuthGuard]},
    {path: 'voting-sessions', component: VotingSessionsComponent, canActivate: [AuthGuard]},

    {path: 'create-voting-session', component: CreateVotingSessionComponent, canActivate: [AdminGuard]},
    {path: 'user-profiles', component: UserProfilesComponent, canActivate: [AdminGuard]},
    {path: 'view-user-profile/:id', component: ViewUserProfileComponent, canActivate: [AdminGuard]},
];



