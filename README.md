# 💉 Uai Odontologia – Sistema MVC + ORM

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)  
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)  
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red.svg)  
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Um sistema completo de agendamento odontológico com chatbot estilo WhatsApp e painel administrativo.**

</div>

---  

## 📄 Índice  

1. [Sobre o Projeto](#-sobre-o-projeto)  
2. [Funcionalidades](#-funcionalidades)  
3. [Tecnologias](#-tecnologias)  
4. [Arquitetura MVC](#-arquitetura-mvc)  
5. [Instalação](#-instalação)  
6. [Como Usar](#-como-usar)  
7. [Estrutura de Pastas](#-estrutura-de-pastas)  
8. [Modelo de Dados](#-modelo-de-dados)  
9. [API REST](#-api-rest)  
10. [Configuração](#-configuração)  
11. [Licença](#-licença)  
12. [Desenvolvedor](#-desenvolvedor)  

---  

## 🎯 Sobre o Projeto  

**Uai Odontologia** simula uma clínica moderna usando a arquitetura **MVC (Model‑View‑Controller)** e **ORM (SQLAlchemy)**.  

O projeto é gerado automaticamente via script Python que cria toda a estrutura de arquivos e diretórios necessária. Ele oferece:

- **Landing page responsiva** – estilizada com *Tailwind CSS* via CDN.  
- **Chatbot “WhatsApp”** – guia o usuário pelo agendamento passo‑a‑passo, interpreta intenções por regras simples e persiste os dados no banco.  
- **Painel administrativo** – lista agendamentos, permite confirmar consultas em tempo real e visualiza estatísticas.  

Tudo isso roda sobre **Flask**, garantindo separação clara entre lógica de negócio, apresentação e persistência.  

---  

## ✨ Funcionalidades  

- **Chatbot Interativo**  
  - Fluxo controlado por estados (`greeting → select_service → select_date → get_name → get_phone → completed`).  
  - Reconhecimento de serviços por palavras‑chave (implantes, ortodontia, harmonização, próteses, endodontia).  
  - Armazenamento automático na sessão do Flask durante o diálogo.  

- **Persistência de Dados**  
  - SQLAlchemy ORM com SQLite (`uai_odonto.db`).  
  - Criação automática das tabelas na primeira execução.  
  - *Seeds* automáticos de profissionais cadastrados no primeiro boot.  

- **Painel Administrativo**  
  - Dashboard com cards de estatísticas (total, pendentes, confirmados, profissionais).  
  - Tabela com todos os agendamentos e ações de aprovação.  
  - Relação entre **Paciente**, **Profissional** e **Agendamento**.  

- **UI Moderna**  
  - Design *mobile‑first* com Tailwind CSS.  
  - Animações de *reveal* nas seções da landing page.  
  - Interface de chat inspirada no WhatsApp Web.  

---  

## 🛠️ Tecnologias  

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.8+ | Linguagem principal |
| **Flask** | 3.0.0 | Framework web |
| **Flask‑SQLAlchemy** | 3.1.1 | ORM para abstração do banco |
| **SQLite** | — (integrado) | Banco relacional leve (auto‑configurado) |
| **Jinja2** | — (integrado) | Templates HTML |
| **Tailwind CSS** | CDN | Estilização *utility‑first* |
| **JavaScript** (vanilla) | — (integrado) | Manipulação do DOM no chatbot |

---  

## 🏗️ Arquitetura MVC  

```
┌─────────────────────────────────────┐
│         Client (Browser)            │
└─────────────────┬───────────────────┘
                  │
        ┌─────────▼─────────┐
        │  Controller       │ ← app.py (rotas, chat logic)
        │  (Flask routes)   │
        └─────────┬─────────┘
                  │          ↕
        ┌─────────▼─────────┐
        │    Model          │ ← models.py (SQLAlchemy ORM)
        │  (DB Entities)    │
        └───────────────────┘
                  │
        ┌─────────▼─────────┐
        │     View          │ ← templates/*.html (Jinja2)
        │  (UI Presentation)│
        └───────────────────┘
```

---  

## 🚀 Instalação  

### Manual  

```bash
# 1. Criar diretórios
mkdir -p uai_odonto/{templates,static/css,static/js,static/images}

# 2. Ambiente virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar a aplicação
python app.py
```

Acesse no navegador:

| Página | URL |
|--------|-----|
| Home | http://127.0.0.1:5000/ |
| Chatbot | http://127.0.0.1:5000/chat |
| Admin | http://127.0.0.1:5000/admin |

---  

## 📱 Como Usar  

1. **Landing Page** – Navegue pelos serviços e conheça a equipe de profissionais cadastrados.  
2. **Chatbot de Agendamento** –  
   - Acesse `/chat`.  
   - Siga as perguntas do assistente virtual.  
   - Informe: serviço → data preferida → nome completo → telefone.  
   - O agendamento será salvo como **pendente**.  
3. **Painel Administrativo** –  
   - Acesse `/admin`.  
   - Visualize estatísticas em tempo real.  
   - Clique em **Confirmar** para mudar o status de *pendente* para *confirmado*.  

---  

## 📂 Estrutura de Pastas  

```
uai_odonto/
├─ instance/
│   └─ uai_odonto.db           # Banco SQLite (criado automaticamente)
├─ templates/
│   ├─ base.html               # Template base com Tailwind
│   ├─ index.html              # Landing page
│   ├─ chat.html               # Interface do chatbot
│   └─ admin/
│       └─ dashboard.html      # Painel administrativo
├─ config.py                   # Configurações da aplicação
├─ models.py                   # Definições ORM (Profissional, Paciente, Agendamento)
├─ app.py                      # Rotas Flask (Controller)
├─ requirements.txt            # Dependências Python
├─ .gitignore                  # Arquivos ignorados pelo Git
├─ setup.bat                   # Script de automação Windows
└─ venv/                       # Ambiente virtual (gerado)
```

---  

## 🗃️ Modelo de Dados  

### Profissional  

| Campo | Tipo | Descrição |
|-------|------|-----------|
| **profissional_id** | Integer (PK) | Chave primária |
| **nome** | String(100) | Nome completo |
| **especialidade** | String(80) | Especialidade clínica |
| **email** | String(100) | Email opcional |
| **telefone** | String(20) | Telefone de contato |
| **criado_em** | DateTime | Data de criação |

### Paciente  

| Campo | Tipo | Descrição |
|-------|------|-----------|
| **paciente_id** | Integer (PK) | Chave primária |
| **nome** | String(100) | Nome completo |
| **email** | String(100) | Email obrigatório |
| **telefone** | String(20) | Telefone obrigatório |
| **criado_em** | DateTime | Data de criação |

### Agendamento  

| Campo | Tipo | Descrição |
|-------|------|-----------|
| **agendamento_id** | Integer (PK) | Chave primária |
| **paciente_id** | Integer (FK) | Relacionamento com Paciente |
| **profissional_id** | Integer (FK) | Relacionamento com Profissional |
| **data_consulta** | Date | Data da consulta |
| **hora_consulta** | Time | Hora da consulta |
| **observacao** | Text | Observações do agendamento |
| **status** | String(20) | `'pendente'` / `'confirmado'` |
| **created_at** | DateTime | Timestamp de criação |

---  

## 🔗 API REST  

### `POST /api/chat/message`  

**Request Body**

```json
{
  "message": "Quero agendar implante para segunda",
  "current_step": "select_service"
}
```

**Response**

```json
{
  "response": "Ótimo! Deseja agendar para **IMPLANTES**?\nQual sua data preferida?",
  "action": { "service": "implantes" },
  "current_step": "select_date"
}
```

### `GET /admin/approve/<id>`  

Confirma agendamento pendente, alterando o **status** para **confirmado**.  

---  

## ⚙️ Configuração  

No arquivo `config.py`:

```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///uai_odonto.db'
SECRET_KEY = 'uai-odonto-secret-key-change-in-production'
SQLALCHEMY_ECHO = False   # True para debug SQL
```

---  

## 📝 Licença  

Distribuído sob a licença **MIT**. Consulte o arquivo `LICENSE` para mais detalhes.  

---  

## 👨‍💻 Desenvolvedor
Desenvolvido por **João Barcelos** – [@j-barcelos](https://github.com/j-barcelos)  

Projeto de estudo e demonstração de arquitetura MVC com Python.
