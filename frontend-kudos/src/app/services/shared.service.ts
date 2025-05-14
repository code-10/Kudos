import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharedService {

  private loggedInStatus = new BehaviorSubject<boolean>(!!localStorage.getItem('access_token'));
  private usersApi = 'http://localhost:8000/api/users/';
  private kudosApi = 'http://localhost:8000/api/kudos/';

  constructor(private http: HttpClient) {}

  registerUser(userData: any): Observable<any> {
    return this.http.post(`${this.usersApi}register/`, userData);
  }

  loginUser(loginData: any): Observable<any> {
    return this.http.post(`${this.usersApi}login/`, loginData);
  }

  getSameOrganizationUsers(): Observable<any> {
    const token = localStorage.getItem('access_token');
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });

    return this.http.get(`${this.usersApi}same-organization-users/`, { headers });
  }

  giveKudos(kudoData: any): Observable<any> {
    const token = localStorage.getItem('access_token');
    return this.http.post(`${this.kudosApi}give/`, kudoData, {
      headers: { Authorization: `Bearer ${token}` }
    });
  }

  getCurrentUser(): Observable<any> {
    const token = localStorage.getItem('access_token');
    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });
    return this.http.get(`${this.usersApi}current_user/`, { headers });
  }

  getAvailableKudos() {
    const token = localStorage.getItem('access_token');
    const headers = {
      Authorization: `Bearer ${token}`
    };
    return this.http.get(`${this.kudosApi}available-kudos/`, { headers });
  }

   getGivenKudos(): Observable<any> {
    const token = localStorage.getItem('access_token');
    const headers = {
      Authorization: `Bearer ${token}`
    };
    return this.http.get(`${this.kudosApi}given/`, { headers });
  }

  getReceivedKudos(): Observable<any> {
    const token = localStorage.getItem('access_token');
    const headers = {
      Authorization: `Bearer ${token}`
    };
    return this.http.get(`${this.kudosApi}received/`, { headers });
  }

  getOrganizations(): Observable<any> {
    return this.http.get(`${this.usersApi}organizations/`);
  }

  setLoggedIn(status: boolean) {
    this.loggedInStatus.next(status);
  }

  get isLoggedIn() {
    return this.loggedInStatus.asObservable();
  }
}
