import { Component, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
// Importamos os dois componentes "filhos"
import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { ChatAreaComponent } from '../../components/chat-area/chat-area.component';

@Component({
  selector: 'app-chat-layout',
  standalone: true,
  imports: [CommonModule, SidebarComponent, ChatAreaComponent],
  templateUrl: './chat-layout.component.html',
  styleUrl: './chat-layout.component.scss',
})
export class ChatLayoutComponent {
  isSidebarOpen = true;

  // O Angular captura a tag #chatArea do HTML e coloca nessa variável
  @ViewChild('chatArea') chatAreaComponent!: ChatAreaComponent;

  toggleSidebar() {
    this.isSidebarOpen = !this.isSidebarOpen;
  }

  // Função chamada quando clicamos no botão + NOVA CONEXÃO
  onNewChat() {
    if (this.chatAreaComponent) {
      this.chatAreaComponent.resetChat(); // Executa a limpeza da tela
    }
  }

  onLoadChat(id: string) {
    if (this.chatAreaComponent) {
      this.chatAreaComponent.loadConversation(id); // Aciona a função que criamos no Passo 3
    }
  }

  onChatDeleted(deletedId: string) {
    if (this.chatAreaComponent && this.chatAreaComponent.currentConversationId === deletedId) {
      this.chatAreaComponent.resetChat(); // Limpa a tela se a conversa atual for apagada
    }
  }
}
