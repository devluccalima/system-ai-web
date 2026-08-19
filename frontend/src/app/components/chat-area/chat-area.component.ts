import { Component, EventEmitter, Input, Output, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

interface ChatMessage {
  role: 'user' | 'system';
  content: string;
}

@Component({
  selector: 'app-chat-area',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat-area.component.html',
  styleUrl: './chat-area.component.scss',
})
export class ChatAreaComponent {
  @Input() isSidebarOpen = true;
  @Output() toggleSidebar = new EventEmitter<void>();

  currentConversationId: string | null = null;

  // 1. Pegamos a referência da nossa tag <main> do HTML
  @ViewChild('scrollFrame') private scrollContainer!: ElementRef;

  userMessage = '';
  isLoading = false;

  messages: ChatMessage[] = [
    { role: 'system', content: 'SISTEMA INICIADO. Aguardando comandos...' },
  ];

  constructor(private http: HttpClient) {}

  // 2. Criamos a função que rola a tela para o final
  private scrollToBottom(): void {
    // Usamos um pequeno atraso (setTimeout) para dar tempo do Angular
    // desenhar o novo balão na tela antes de calcular a altura total
    setTimeout(() => {
      try {
        this.scrollContainer.nativeElement.scrollTop =
          this.scrollContainer.nativeElement.scrollHeight;
      } catch (err) {}
    }, 50);
  }

  async sendMessage() {
    if (!this.userMessage.trim() || this.isLoading) return;

    const text = this.userMessage;
    this.userMessage = '';

    // 1. Adiciona a mensagem do usuário
    this.messages.push({ role: 'user', content: text });
    this.isLoading = true;
    this.scrollToBottom();

    // 2. Cria um balão vazio para a IA, que vamos preencher letra por letra
    const systemMsgIndex = this.messages.push({ role: 'system', content: '' }) - 1;

    // Precisamos pegar o token manualmente já que vamos usar o 'fetch' nativo
    const token = localStorage.getItem('access_token');

    try {
      // 3. Fazemos a requisição nativa esperando um fluxo de dados
      const response = await fetch('http://localhost:8080/api/v1/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`, // O nosso crachá
        },
        body: JSON.stringify({ message: text, conversation_id: this.currentConversationId }), // Envia a mensagem e o ID da conversa
      });

      const convId = response.headers.get('X-Conversation-ID');
      if (convId) {
        this.currentConversationId = convId;
      }

      if (!response.body) throw new Error('Falha ao iniciar o fluxo de dados');

      // 4. Lemos a resposta em pedaços (Chunks)
      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      this.isLoading = false; // Desliga a animação "PROCESSANDO..."

      while (true) {
        const { done, value } = await reader.read();
        if (done) break; // Acabou a resposta

        // Converte os bytes recebidos em texto e adiciona ao balão da IA
        const chunk = decoder.decode(value, { stream: true });
        this.messages[systemMsgIndex].content += chunk;

        // Rola a tela para acompanhar a digitação
        this.scrollToBottom();
      }
    } catch (error) {
      console.error('Erro no fluxo do chat:', error);
      this.messages[systemMsgIndex].content =
        '[ ERRO CRÍTICO: Falha de comunicação com o Núcleo IA. ]';
      this.isLoading = false;
    }
  }

  resetChat() {
    // 1. Zera o ID para que o backend crie uma nova conversa no banco
    this.currentConversationId = null;

    // 2. Limpa a tela e volta a mensagem inicial
    this.messages = [
      { role: 'system', content: 'NOVA CONEXÃO ESTABELECIDA. Aguardando comandos...' },
    ];
  }

  loadConversation(id: string) {
    this.currentConversationId = id;

    // Limpa a tela e coloca a animação de carregamento, se quiser
    this.messages = [];

    // Usa o HttpClient para buscar as mensagens daquela rota nova que fizemos no backend
    this.http.get<ChatMessage[]>(`http://localhost:8080/api/v1/chat/${id}/messages`).subscribe({
      next: (history) => {
        // Substitui as mensagens da tela pelo histórico do banco!
        this.messages = history;
        this.scrollToBottom();
      },
      error: (err) => {
        console.error('Erro ao carregar mensagens antigas:', err);
        this.messages = [
          {
            role: 'system',
            content: '[ ERRO: Não foi possível recuperar a memória desta conexão. ]',
          },
        ];
      },
    });
  }
}
