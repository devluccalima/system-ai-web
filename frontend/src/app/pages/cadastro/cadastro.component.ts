import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-cadastro',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './cadastro.component.html',
  styleUrl: './cadastro.component.scss',
})
export class CadastroComponent {
  cadastroForm: FormGroup;
  isLoading = false;
  errorMessage = '';
  successMessage = '';

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private router: Router,
  ) {
    // Montando a estrutura exata que o backend espera
    this.cadastroForm = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      ai_context: this.fb.group({
        profession: [''],
        tech_stack: [''], // Ex: "Python, Angular, Docker"
        hobbies: [''], // Ex: "RPG, Jogos, Carros"
        current_projects: [''], // Ex: "Sistema de Controle"
        custom_instructions: [''],
      }),
    });
  }

  onSubmit() {
    if (this.cadastroForm.invalid) return;

    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';

    const rawValue = this.cadastroForm.value;

    // Função auxiliar para transformar string "A, B, C" em array ["A", "B", "C"]
    const formatArray = (str: string) => {
      return str
        ? str
            .split(',')
            .map((s) => s.trim())
            .filter((s) => s !== '')
        : [];
    };

    // Monta o JSON (payload) final que será enviado ao FastAPI
    const payload = {
      name: rawValue.name,
      email: rawValue.email,
      password: rawValue.password,
      ai_context: {
        profession: rawValue.ai_context.profession || '', // Se for nulo, manda string vazia
        tech_stack: formatArray(rawValue.ai_context.tech_stack),
        hobbies: formatArray(rawValue.ai_context.hobbies),
        current_projects: formatArray(rawValue.ai_context.current_projects),
        custom_instructions:
          rawValue.ai_context.custom_instructions || 'Seja útil, claro e objetivo.',
      },
    };

    // Faz a requisição POST para a rota de criação de usuários
    this.http.post('http://localhost:8080/api/v1/users', payload).subscribe({
      next: () => {
        this.successMessage = 'REGISTRO CONCLUÍDO. Redirecionando...';
        // Aguarda 2 segundos para o usuário ver a mensagem e manda pro login
        setTimeout(() => this.router.navigate(['/login']), 2000);
      },
      error: (err) => {
        this.isLoading = false;

        // Se for erro 422, o FastAPI manda um array de detalhes. Pegamos o primeiro.
        if (err.status === 422) {
          const problemField = err.error.detail[0]?.loc[err.error.detail[0].loc.length - 1];
          this.errorMessage = `Formato inválido no campo: ${problemField}`;
        } else {
          this.errorMessage = err.error?.detail || 'Erro ao criar registro.';
        }
        console.error('ERRO COMPLETO:', err);
      },
    });
  }
}
