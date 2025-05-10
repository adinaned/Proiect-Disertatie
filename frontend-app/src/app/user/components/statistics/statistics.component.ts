import {Component} from '@angular/core';

@Component({
    selector: 'app-statistics',
    imports: [],
    templateUrl: './statistics.component.html',
    styleUrls: ['./statistics.component.css']
})
export class StatisticsComponent {
    handleToken() {
        console.log("Switching to 'Statistics' tab");
    }
}
