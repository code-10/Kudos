import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { SharedService } from '../../services/shared.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-register',
  imports: [FormsModule, CommonModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  username = '';
  email = '';
  password = '';
  organization_id = '';
  successMessage: string | null = null;
  errorMessage: string | null = null;
  organizations: any[] = [];
  selectedOrganization: string = '';

  constructor(private sharedService: SharedService, private router: Router) {}

  ngOnInit(): void {
    this.fetchOrganizations();
  }

  onSubmit() {
    const userData = {
      username: this.username,
      email: this.email,
      password: this.password,
      organization_id: this.selectedOrganization,
    };

    this.sharedService.registerUser(userData).subscribe({
      next: (response) => {
        this.successMessage = 'Registration successful. Please login.';
        this.errorMessage = null;

        setTimeout(() => this.router.navigate(['/login']), 500);
      },
      error: (error) => {
        this.errorMessage = 'Registration failed. Please try again.';
        this.successMessage = null;
      }
    });
  }

  fetchOrganizations(): void {
    this.sharedService.getOrganizations().subscribe({
      next: (response: any) => {
        this.organizations = response.reverse();
      },
      error: (error) => {
        console.error('Error fetching organizations:', error);
      },
    });
  }
}
