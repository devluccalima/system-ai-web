import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http'; // <-- Importamos o HttpClient

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.scss',
})
export class SidebarComponent implements OnInit {
  // Variável que vai guardar a lista de conversas vindas do banco
  conversations: any[] = [];

  // Avisa o componente pai quando o usuário clicar em "Nova Conexão"
  @Output() newChat = new EventEmitter<void>();

  @Output() selectChat = new EventEmitter<string>();

  @Output() chatDeleted = new EventEmitter<string>();

  constructor(
    private router: Router,
    private http: HttpClient,
  ) {}

  // O ngOnInit roda automaticamente assim que a barra lateral nasce na tela
  ngOnInit() {
    this.loadConversations();
  }

  onSelectChat(id: string) {
    this.selectChat.emit(id);
  }

  loadConversations() {
    this.http.get<any[]>('http://localhost:8080/api/v1/chat/conversations').subscribe({
      next: (data) => {
        this.conversations = data;
      },
      error: (err) => {
        console.error('Erro ao carregar histórico:', err);
      },
    });
  }

  startNewChat() {
    this.newChat.emit();
  }

  onDeleteChat(id: string, event: Event) {
    // Isso impede que o clique no botão [X] dispare o clique da conversa (que a abriria)
    event.stopPropagation();

    // Uma confirmação simples por segurança
    if (!confirm('Tem certeza que deseja apagar esta memória?')) return;

    // Dispara a deleção no backend
    this.http.delete(`http://localhost:8080/api/v1/chat/${id}`).subscribe({
      next: () => {
        // Remove a conversa da lista visual instantaneamente
        this.conversations = this.conversations.filter((c) => c.id !== id);

        // Avisa o componente pai (Layout) que essa conversa morreu
        this.chatDeleted.emit(id);
      },
      error: (err) => {
        console.error('Erro ao deletar a conversa:', err);
        alert('Falha ao apagar a memória do banco de dados.');
      },
    });
  }

  logout() {
    localStorage.removeItem('access_token');
    this.router.navigate(['/login']);
  }
}
