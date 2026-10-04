# Arquitetura do ClassBase

## Visão geral

```mermaid
flowchart TD
    U[Usuário] --> K[Interface Kivy]
    K --> S[Classes de tela]
    S --> M[ClassBaseScreenManager]
    S --> SR[StudentRepository]
    S --> AR[AuthRepository]
    SR --> DB[(SQLite classbase.db)]
    AR --> DB
```

## Estrutura do projeto

```text
ClassBase/
├── main.py
├── buildozer.spec
├── requirements.txt
├── assets/
│   ├── icon.png
│   └── presplash.png
├── database/
│   ├── connection.py
│   ├── auth.py
│   └── repository.py
├── screens/
│   ├── manager.py
│   ├── login.py
│   ├── home.py
│   ├── cadastro.py
│   ├── alunos.py
│   └── editar.py
├── kv/
│   ├── theme.kv
│   ├── login.kv
│   ├── home.kv
│   ├── cadastro.kv
│   ├── alunos.kv
│   └── editar.kv
├── tests/
└── docs/
```

## Responsabilidades

### main.py

- inicia o aplicativo;
- carrega os arquivos KV;
- define o banco no diretório gravável da aplicação;
- cria os repositórios;
- garante o usuário inicial;
- registra as cinco telas;
- configura o comportamento do teclado virtual.

### database/connection.py

- abre e fecha conexões SQLite;
- habilita foreign keys;
- executa commit em sucesso;
- executa rollback em exceção;
- cria as tabelas quando necessário.

### database/repository.py

Responsável pelos alunos:

- `create_student`;
- `get_student`;
- `list_students`;
- `update_student`;
- `delete_student`;
- `count_students`.

As consultas usam placeholders `?`, evitando concatenação direta de entrada do usuário no SQL.

### database/auth.py

Responsável por usuários e autenticação:

- criação de usuário;
- geração de salt;
- PBKDF2-HMAC-SHA256;
- autenticação;
- criação do usuário inicial.

### screens/

Cada classe representa o comportamento de uma tela. O layout visual correspondente fica em `kv/`.

Essa separação facilita explicar o projeto:

```text
arquivo .kv = aparência
arquivo .py da tela = comportamento
repository = acesso ao banco
```

## Fluxo de cadastro

```mermaid
sequenceDiagram
    actor Usuario
    participant Tela as RegisterStudentScreen
    participant Repo as StudentRepository
    participant DB as SQLite

    Usuario->>Tela: informa RM, nome e curso
    Tela->>Repo: create_student(...)
    Repo->>Repo: valida e limpa dados
    Repo->>DB: INSERT parametrizado
    alt RM já existe
        DB-->>Repo: IntegrityError
        Repo-->>Tela: ValueError
        Tela-->>Usuario: mensagem de erro
    else cadastro válido
        DB-->>Repo: id do registro
        Repo-->>Tela: sucesso
        Tela-->>Usuario: mensagem verde
    end
```

## Fluxo de login

```mermaid
sequenceDiagram
    actor Usuario
    participant Tela as LoginScreen
    participant Auth as AuthRepository
    participant DB as SQLite

    Usuario->>Tela: usuário e senha
    Tela->>Auth: authenticate(...)
    Auth->>DB: SELECT salt, senha_hash
    Auth->>Auth: PBKDF2 da senha informada
    Auth->>Auth: hmac.compare_digest
    Auth-->>Tela: True/False
    Tela-->>Usuario: Home ou erro
```

## Decisões importantes

- O RM é `TEXT UNIQUE NOT NULL`.
- O banco fica no `user_data_dir` do aplicativo no Android.
- A UI não conhece detalhes de SQL.
- O ScreenManager compartilha os repositórios com as telas.
- Cadastro e edição utilizam ScrollView para compatibilidade com teclado.
- O app funciona offline por decisão de escopo.
