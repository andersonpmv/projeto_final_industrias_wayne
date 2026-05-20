# Wayne Security System

Sistema Full Stack de gerenciamento de segurança corporativa inspirado no universo Wayne Enterprises.

O projeto foi desenvolvido utilizando arquitetura modular no backend com Flask + JWT Authentication e frontend responsivo em HTML, CSS e JavaScript puro.

A proposta do sistema é simular uma central de segurança interna com:
- controle de usuários
- autenticação
- autorização por níveis
- gerenciamento de recursos
- logs de acesso
- dashboard administrativo
- interface futurista inspirada em Gotham City


---

# Demonstração do Sistema
## Login
- autenticação JWT
- bloqueio de acesso sem token
- validação de credenciais
- persistência de sessão

# Usuários de Teste

O sistema possui três níveis de acesso para validação completa das permissões e fluxos de autenticação.

---

## Administrador

Permissão total do sistema:
- gerenciamento de usuários
- gerenciamento de recursos
- dashboard completo
- logs
- credenciais
- controle geral

Email: admin@wayne.com
Senha: 123456


## Gerente

Permissão intermediária:
- acesso operacional
- visualização administrativa parcial
- gerenciamento limitado

Email: gerente@wayne.com
Senha: 123456


## Funcionário

Permissão restrita:
-acesso básico
-funcionalidades limitadas
-sem acesso administrativo
Email: funcionario@wayne.com
Senha: 123456


## Dashboard
- total de usuários
- total de logs
- acessos permitidos
- acessos negados
- áreas monitoradas
- gráfico de acessos

## Painel Administrativo
- CRUD de usuários
- CRUD de recursos
- gerenciamento de credenciais
- controle de permissões

## Segurança
- proteção de rotas
- decorators de autenticação
- controle por roles:
  - admin
  - gerente
  - funcionário

## Logs
- armazenamento de acessos
- rastreamento de eventos
- histórico de ações

---

# Tecnologias Utilizadas

## Backend
- Python
- Flask
- Flask SQLAlchemy
- Flask CORS
- JWT Authentication
- SQLite

## Frontend
- HTML5
- CSS3
- JavaScript Vanilla
- Chart.js

## Ferramentas
- VS Code
- Git
- GitHub
- Postman
- Insomnia

---
```text
# Estrutura do Projeto

wayne-security-system/
│
├── backend/
│   ├── app/
│   │
│   ├── models/
│   │   ├── access_log.py
│   │   ├── area.py
│   │   ├── resource.py
│   │   └── user.py
│   │
│   ├── routes/
│   │   ├── access_routes.py
│   │   ├── area_routes.py
│   │   ├── auth_routes.py
│   │   ├── dashboard_routes.py
│   │   ├── resource_routes.py
│   │   ├── test_routes.py
│   │   └── user_routes.py
│   │
│   ├── utils/
│   │   ├── auth.py
│   │   ├── auth_decorators.py
│   │   ├── decorators.py
│   │   └── role_decorator.py
│   │
│   ├── config.py
│   ├── extensions.py
│   ├── run.py
│   ├── seed.py
│   ├── requirements.txt
│   └── wayne_security.db
│
├── frontend/
│   ├── assets/
│   │   └── img/
│   │
│   ├── css/
│   │   ├── admin.css
│   │   ├── dashboard.css
│   │   └── login.css
│   │
│   ├── js/
│   │   ├── admin.js
│   │   ├── dashboard.js
│   │   └── login.js
│   │
│   ├── login.html
│   ├── dashboard.html
│   └── admin.html
│
├── docs/
│
└── .gitignore
