import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink], // Importamos os módulos necessários
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
})
export class LoginComponent {
  loginForm: FormGroup;
  isLoading = false;
  errorMessage = '';

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private router: Router,
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
    });
  }

  onSubmit() {
    if (this.loginForm.invalid) return;

    this.isLoading = true;
    this.errorMessage = '';

    // Monta o corpo da requisição exatamente como o OAuth2 espera
    const body = new HttpParams()
      .set('username', this.loginForm.value.email)
      .set('password', this.loginForm.value.password);

    this.http
      .post('http://localhost:8080/api/v1/login', body.toString(), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      })
      .subscribe({
        next: (response: any) => {
          // Guarda o "crachá" JWT no navegador
          localStorage.setItem('access_token', response.access_token);
          // Redireciona para o Cérebro do Sistema
          this.router.navigate(['/chat']);
        },
        error: (err) => {
          this.isLoading = false;
          this.errorMessage = 'Acesso negado. Credenciais inválidas.';
          console.error(err);
        },
      });
  }
}
