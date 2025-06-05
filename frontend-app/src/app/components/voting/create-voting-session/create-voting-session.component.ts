import {Component, OnInit} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';
import {NgFor} from '@angular/common';
import {firstValueFrom} from "rxjs";

@Component({
    selector: 'app-create-voting-session',
    standalone: true,
    imports: [FormsModule, NgFor],
    templateUrl: './create-voting-session.component.html',
    styleUrls: ['./create-voting-session.component.css']
})
export class CreateVotingSessionComponent implements OnInit {
    title = '';
    question = '';
    startDate = '';
    endDate = '';
    organizationId: number | null = null;
    roleId: number | null = null;

    organizations: any[] = [];
    roles: any[] = [];
    options: { value: string }[] = [{value: ''}];

    constructor(private http: HttpClient, private router: Router) {
    }

    ngOnInit(): void {
        this.http.get<any[]>('http://127.0.0.1:5000/organizations')
            .subscribe(data => {
                this.organizations = data;
                console.log('Organizations:', this.organizations);
            });

        this.http.get<any[]>('http://127.0.0.1:5000/roles')
            .subscribe(data => {
                this.roles = data;
                console.log('Roles:', this.roles);
            });
    }

    addOption() {
        this.options.push({value: ''});
    }

    removeOption(index: number) {
        this.options.splice(index, 1);
    }

    onCancel() {
        this.router.navigate(['/login']);
    }

    onSubmit() {
        if (!this.title || !this.question || !this.startDate || !this.endDate || !this.organizationId || !this.roleId) {
            alert('Please fill in all required fields.');
            return;
        }

        const normalizedStart = this.startDate.includes(':') && this.startDate.split(':').length === 2
            ? this.startDate + ':00'
            : this.startDate;

        const normalizedEnd = this.endDate.includes(':') && this.endDate.split(':').length === 2
            ? this.endDate + ':00'
            : this.endDate;

        const payload = {
            title: this.title,
            question: this.question,
            start_datetime: new Date(normalizedStart).toISOString(),
            end_datetime: new Date(normalizedEnd).toISOString(),
            organization_id: this.organizationId,
            role_id: this.roleId
        };

        console.log('Payload to send for session:', payload);

        this.http.post<any>('http://127.0.0.1:5000/voting_sessions', payload)
            .subscribe({
                next: (sessionResponse) => {
                    const sessionId = sessionResponse.id;
                    console.log('Session created with ID:', sessionId);

                    const optionPayloads = this.options
                        .filter(opt => opt.value.trim() !== '')
                        .map(opt => ({
                            name: opt.value,
                            session_id: sessionId,
                        }));

                    console.log('Option payloads to save:', optionPayloads);

                    const requests = optionPayloads.map(option =>
                        firstValueFrom(this.http.post<any>(`http://127.0.0.1:5000/options/${sessionId}`, option))
                    );

                    Promise.all(requests)
                        .then(() => {
                            alert('Voting session and options created successfully!');
                            this.router.navigate(['/voting-sessions']);
                        })
                        .catch((err) => {
                            console.error('Failed to save options:', err);
                            alert('Voting session created, but failed to save one or more options.');
                        });
                },
                error: err => {
                    console.error('Failed to create voting session:', err);
                    alert('Failed to create voting session.');
                }
            });
    }
}
