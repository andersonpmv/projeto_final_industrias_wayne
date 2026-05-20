# Wayne Security System

Sistema Full Stack de gerenciamento de segurança corporativa inspirado no universo Wayne Enterprises.

O projeto foi desenvolvido utilizando arquitetura modular no backend com Flask + JWT Authentication e frontend responsivo em HTML, CSS e JavaScript puro.

A proposta do sistema é simular uma central de segurança corporativa interna com autenticação, controle de acesso, gerenciamento administrativo e monitoramento operacional.

---

# Links do Projeto Online

## Frontend
https://wayne-security-frontend.vercel.app/login.html

## Backend API
https://wayne-security-backend.onrender.com

---

# Funcionalidades do Sistema

## Login e Autenticação

- autenticação JWT
- persistência de sessão
- logout seguro
- proteção de rotas
- bloqueio de acesso sem token
- controle de permissões
- autenticação por níveis de acesso

---

# Usuários de Teste

O sistema possui três níveis diferentes de acesso para validação completa das permissões e fluxos de autenticação.

---

## Administrador

Permissão total do sistema:

- gerenciamento de usuários
- gerenciamento de recursos
- gerenciamento de credenciais
- visualização completa do dashboard
- acesso aos logs
- controle administrativo total

### Credenciais
```text
Email: admin@wayne.com
Senha: 123456
```

---

## Gerente

Permissão intermediária:

- acesso operacional
- visualização parcial do sistema
- gerenciamento limitado
- acesso ao dashboard

### Credenciais
```text
Email: gerente@wayne.com
Senha: 123456
```

---

## Funcionário

Permissão restrita:

- acesso básico
- funcionalidades limitadas
- sem acesso administrativo

### Credenciais
```text
Email: funcionario@wayne.com
Senha: 123456
```

---

# Dashboard

O dashboard principal apresenta:

- total de usuários
- total de logs
- acessos permitidos
- acessos negados
- áreas monitoradas
- total de recursos
- usuários ativos
- gráfico de acessos por área

---

# Painel Administrativo

O painel administrativo permite:

- CRUD de usuários
- CRUD de recursos
- gerenciamento de credenciais
- controle de permissões
- gerenciamento operacional interno

---

# Segurança

O sistema possui:

- autenticação JWT
- decorators de autenticação
- controle de acesso por roles
- proteção de rotas privadas
- verificação de permissões
- bloqueio de acesso sem token
- controle de usuários bloqueados

---

# Logs e Monitoramento

O sistema registra:

- armazenamento de acessos
- rastreamento de eventos
- histórico de ações
- monitoramento operacional
- controle de acessos internos

---

# Tecnologias Utilizadas

## Backend

- Python
- Flask
- Flask SQLAlchemy
- Flask CORS
- Flask Bcrypt
- JWT Authentication
- SQLite
- Gunicorn

---

## Frontend

- HTML5
- CSS3
- JavaScript Vanilla
- Chart.js

---

## Ferramentas

- VS Code
- Git
- GitHub
- Postman
- Insomnia
- Render
- Vercel

---

# Arquitetura do Projeto

O projeto foi estruturado utilizando arquitetura modular para facilitar:

- escalabilidade
- organização
- manutenção
- separação de responsabilidades
- reutilização de código

---

# Estrutura do Projeto

```text
wayne-security-system/
│
├── backend/
│   │
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
│   ├── Procfile
│   ├── requirements.txt
│   └── wayne_security.db
│
├── frontend/
│   │
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
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   └── admin.html
│
├── docs/
│
├── .gitignore
└── README.md
```

---

# Deploy

## Frontend hospedado na Vercel

https://wayne-security-frontend.vercel.app/login.html

---

## Backend hospedado no Render

https://wayne-security-backend.onrender.com

---

# Testes Realizados

O sistema foi validado com:

- testes completos de autenticação
- validação de permissões
- CRUD completo
- proteção de rotas
- testes de token JWT
- testes de dashboard
- testes administrativos
- testes responsivos
- integração frontend/backend
- deploy em produção
- testes via Postman
- testes via Insomnia

---

# Responsividade

O frontend foi desenvolvido com layout responsivo para:

- desktop
- notebook
- tablet
- mobile

---

# Objetivo do Projeto

O objetivo do projeto é demonstrar conhecimentos em:

- desenvolvimento full stack
- arquitetura backend
- autenticação JWT
- APIs REST
- organização modular
- segurança de aplicações
- integração frontend/backend
- deploy em produção
- controle de permissões
- gerenciamento administrativo

---

# Autor

Anderson Alves

Projeto desenvolvido para fins de estudo, prática e consolidação de conhecimentos em desenvolvimento Full Stack.