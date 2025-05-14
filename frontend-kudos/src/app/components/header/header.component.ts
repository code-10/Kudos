import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { SharedService } from '../../services/shared.service';

@Component({
  selector: 'app-header',
  imports: [CommonModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {
  isLoggedIn = false;
  username: string | null = '';

  constructor(private sharedService: SharedService, private router: Router) {}

  ngOnInit() {
    this.sharedService.isLoggedIn.subscribe((status) => {
      this.isLoggedIn = status;
      if (status) {
        this.getCurrentUser();
      }
    });
  }

  getCurrentUser() {
    this.sharedService.getCurrentUser().subscribe({
      next: (user) => {
        this.username = user.username.charAt(0).toUpperCase() + user.username.slice(1);
      },
      error: (error) => {
        console.error('Error fetching current user:', error);
        this.logout();
      }
    });
  }

  logout() {
    localStorage.removeItem('access_token');
    this.sharedService.setLoggedIn(false);
    this.isLoggedIn = false;
    this.username = '';
    this.router.navigate(['/login']);
  }
}
