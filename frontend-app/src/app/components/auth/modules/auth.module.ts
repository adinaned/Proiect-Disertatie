import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RegisterAccountComponent } from '../register-account/register-account.component';

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        RegisterAccountComponent
    ]
})
export class AuthModule { }