import { Component } from '@angular/core';
import { SharedService } from '../../services/shared.service';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  imports: [FormsModule, CommonModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  username = '';
  password = '';
  successMessage: string | null = null;
  errorMessage: string | null = null;

  constructor(private sharedService: SharedService, private router: Router) {}

  onSubmit() {
    const loginData = {
      username: this.username,
      password: this.password
    };

    this.sharedService.loginUser(loginData).subscribe({
      next: (response) => {
        this.successMessage = 'Login successful. Redirecting...';
        this.errorMessage = null;

        localStorage.setItem('access_token', response.access_token);

        this.sharedService.setLoggedIn(true);

        setTimeout(() => this.router.navigate(['/dashboard']), 500);
      },
      error: (error) => {
        this.errorMessage = 'Invalid credentials. Please try again.';
        this.successMessage = null;
      }
    });
  }
}
