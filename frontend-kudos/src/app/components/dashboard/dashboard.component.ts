import { Component } from '@angular/core';
import { SharedService } from '../../services/shared.service';
import { CommonModule } from '@angular/common';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule, FontAwesomeModule, FormsModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {
  sameOrgUsers: any[] = [];
  availableKudos: number = 0; 
  viewType: string = 'users'; 

  constructor(private sharedService: SharedService) {}

  ngOnInit(): void {
    this.fetchSameOrgUsers();
    this.fetchAvailableKudos();
  }

  fetchSameOrgUsers(): void {
    this.sharedService.getSameOrganizationUsers().subscribe({
      next: (response) => {
        this.sameOrgUsers = response.map((user: any) => ({ ...user, message: '' }));
      },
      error: (error) => {
        console.error('Error fetching users:', error);
      }
    });
  }

   fetchAvailableKudos(): void {
    this.sharedService.getAvailableKudos().subscribe({
      next: (response:any) => {
        this.availableKudos = response['available_kudos']
      },
      error: (error) => {
        console.error('Error fetching available kudos:', error);
      }
    });
  }

  giveKudos(user: any): void {
    const message = user.message.trim();
    if (!message) return;

    const kudoData = {
      to_user_id: user.id,
      message: message
    };

    this.sharedService.giveKudos(kudoData).subscribe({
      next: () => {
        console.log('Kudos sent successfully');
        user.message = '';
        alert(`Kudos sent to ${user.username} successfully!`);
        this.fetchAvailableKudos();
        this.fetchSameOrgUsers();
      },
      error: (error) => {
        console.error('Failed to send kudos', error);
        alert('Failed to send kudos. Please try again.');
      }
    });
  }

  switchView(view: string): void {
    this.viewType = view;
    if (view === 'given') {
      this.fetchGivenKudos();
    } else if (view === 'received') {
      this.fetchReceivedKudos();
    } else {
      this.fetchSameOrgUsers();
    }
  }

  fetchGivenKudos(): void {
    this.sharedService.getGivenKudos().subscribe({
      next: (response: any) => {
        // Mapping the nested structure to a flat one for easier handling
        this.sameOrgUsers = response.map((kudo: any) => ({
          id: kudo.id,
          username: kudo.to_user.username,
          message: kudo.message,
          created_at: kudo.created_at
        }));
      },
      error: (error) => {
        console.error('Error fetching given kudos:', error);
      }
    });
  }

  fetchReceivedKudos(): void {
    this.sharedService.getReceivedKudos().subscribe({
      next: (response: any) => {
        // Mapping the nested structure to a flat one for easier handling
        this.sameOrgUsers = response.map((kudo: any) => ({
          id: kudo.id,
          username: kudo.from_user.username,
          message: kudo.message,
          created_at: kudo.created_at
        }));
      },
      error: (error) => {
        console.error('Error fetching received kudos:', error);
      }
    });
  }
}
