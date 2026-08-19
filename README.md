# 🧠 System AI - Web Interface

Um assistente virtual inteligente e local (estilo Jarvis), construído com uma arquitetura full-stack moderna. O sistema utiliza processamento de Linguagem Natural (NLP) 100% offline através do Ollama, garantindo privacidade total dos dados, aliado a uma interface reativa e gerenciamento de memória em banco de dados relacional.

## 🚀 Tecnologias Utilizadas

**Frontend:**
* [Angular](https://angular.dev/) - Framework SPA responsivo e componentizado.
* HTML5 / CSS3 Avançado - Design futurista "glassmorphism", animações CSS e auto-scroll fluido.
* TypeScript - Tipagem forte e integração com APIs em tempo real (Streams nativas/Fetch).

**Backend:**
* [FastAPI](https://fastapi.tiangolo.com/) (Python) - Servidor de alta performance e assíncrono.
* [PostgreSQL](https://www.postgresql.org/) - Banco de dados relacional para persistência de histórico e usuários.
* [SQLAlchemy](https://www.sqlalchemy.org/) - ORM para manipulação eficiente dos dados.
* Pydantic - Validação de schemas e tipagem.

**Inteligência Artificial (Motor IA):**
* [Ollama](https://ollama.com/) (Dockerizado) - Gerenciador de LLMs locais.
* LLM: **Llama 3.2 (3B)** - Modelo de inferência rápida otimizado para hardwares com restrição de RAM (aprox. 2GB consumidos).

## ✨ Principais Funcionalidades

* **Streaming de Texto em Tempo Real:** Respostas processadas e exibidas "palavra por palavra" (Server-Sent Events), eliminando o tempo de espera no carregamento do LLM.
* **Memória de Longo Prazo:** O histórico de conversas é salvo no PostgreSQL. Ao selecionar uma conexão antiga, a IA recupera o contexto inteiro e continua o raciocínio de onde parou.
* **Autenticação Segura:** Sistema de login com geração e validação de tokens JWT (JSON Web Tokens) através de Interceptors no Angular.
* **Interface Dinâmica:** Barra lateral expansível, separação visual de mensagens (User vs System), indicador de digitação (typing animation) e botões de limpeza/exclusão de histórico.

## 🛠️ Como Executar o Projeto

Este projeto é dividido em três serviços principais: Banco de Dados, Backend (Python) e Frontend (Angular).

### 1. Preparando o Ambiente IA (Ollama)
Certifique-se de ter o Docker instalado e inicie o container do Ollama:
```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name system_ollama ollama/ollama
```
Baixe o modelo utilizado no projeto:
```bash
docker exec -it system_ollama ollama pull llama3.2
```
###2. Rodando o Backend (FastAPI)
Navegue até a pasta do backend, ative seu ambiente virtual (VENV) e instale as dependências:
```bash
pip install -r requirements.txt
```
Inicie o servidor (o padrão será executado na porta 8080 ou 8000):
```bash
uvicorn app.main:app --reload --port 8080
```
###3. Rodando o Frontend (Angular)
Navegue até a pasta do frontend e instale os pacotes NPM:
```bash
npm install
```
Inicie o servidor de desenvolvimento:
```bash
ng serve
```
Acesse http://localhost:4200 em seu navegador para iniciar a comunicação com o sistema.
Desenvolvido por Lucca Lima.
