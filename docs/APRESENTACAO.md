# Roteiro da apresentação — ClassBase

Sugestão: apresentação de 8 a 12 minutos + demonstração.

## Slide 1 — ClassBase

**Título:** ClassBase  
**Subtítulo:** Aplicativo mobile para gerenciamento de alunos

Falar:
- desenvolvido em Python;
- interface Kivy;
- banco SQLite;
- APK Android.

## Slide 2 — Problema e objetivo

Problema:
- necessidade de organizar dados básicos de alunos;
- aplicar banco de dados em um aplicativo real.

Objetivo:
- criar um app mobile com login e CRUD de alunos;
- manter funcionamento offline e simples.

## Slide 3 — Requisitos

Mostrar:
- login;
- RM, nome e curso;
- RM único;
- cadastrar;
- listar/pesquisar;
- editar;
- excluir com confirmação;
- persistir dados.

Frase importante:

> O objetivo não era criar um sistema escolar completo, e sim implementar corretamente um fluxo de gerenciamento de alunos com banco de dados.

## Slide 4 — Tecnologias

| Tecnologia | Uso |
|---|---|
| Python | regras da aplicação |
| Kivy | interface mobile |
| SQLite | banco local |
| Buildozer | geração do APK |
| Git/GitHub | versionamento |

Explicar por que SQLite e Kivy foram escolhidos.

## Slide 5 — Arquitetura

Mostrar:

```text
Interface Kivy
      ↓
Lógica Python
      ↓
Repositories
      ↓
SQLite
```

Explicar que a interface não acessa o banco diretamente.

## Slide 6 — Banco de dados

Tabela `alunos`:
- id;
- rm;
- nome;
- curso.

Tabela `usuarios`:
- id;
- usuario;
- salt;
- senha_hash.

Destacar:
- RM com UNIQUE;
- senha não fica em texto puro.

## Slide 7 — CRUD

Mostrar a associação:

- Create → cadastrar → INSERT;
- Read → listar/pesquisar → SELECT;
- Update → editar → UPDATE;
- Delete → excluir → DELETE.

Esse slide é importante porque demonstra domínio do conteúdo de banco de dados.

## Slide 8 — Interface e experiência mobile

Mostrar telas:
- Login;
- Home;
- Cadastro;
- Lista;
- Edição.

Explicar que o teste em celular revelou um problema real com o teclado cobrindo ações e que isso foi corrigido com formulários roláveis.

## Slide 9 — Segurança e validações

- PBKDF2-HMAC-SHA256 + salt;
- consultas parametrizadas;
- RM único no banco;
- campos obrigatórios;
- confirmação de exclusão;
- commit/rollback;
- backup Android desativado.

Evitar dizer que o app é “100% seguro”. Dizer que possui medidas compatíveis com o escopo.

## Slide 10 — Testes

Números:
- 29 testes automatizados PASS;
- build Android PASS;
- assinatura APK v2 PASS;
- QA física crítica PASS em POCO C75 / Android 16.

Mostrar exemplos:
- RM duplicado;
- persistência;
- busca;
- edição;
- logout;
- teclado.

## Slide 11 — Problemas encontrados

1. incompatibilidade no primeiro build Android;
2. bloqueio inicial de instalação pelo verificador;
3. teclado cobrindo botões;
4. mensagem de sucesso com cor inadequada.

Explicar que cada problema gerou uma correção e nova validação.

## Slide 12 — Limitações e futuro

Limitações:
- offline;
- banco local;
- sem sincronização;
- usuário simples;
- APK debug.

Futuro:
- API;
- banco central;
- perfis;
- cursos configuráveis;
- exportação;
- release assinada.

## Slide 13 — Demonstração

Fluxo recomendado:
1. login;
2. cadastrar aluno;
3. mostrar contador;
4. consultar;
5. pesquisar;
6. editar;
7. excluir;
8. explicar persistência.

Não improvisar dados. Usar um RM e nome definidos antes da apresentação.

## Slide 14 — Conclusão

Mensagem:

> O ClassBase implementa um ciclo completo de gerenciamento de dados em um aplicativo Android, integrando Python, Kivy e SQLite com validação prática em dispositivo real.

## Divisão sugerida para 4 integrantes

### Integrante 1
- introdução;
- problema;
- objetivo;
- requisitos.

### Integrante 2
- tecnologias;
- arquitetura;
- banco de dados.

### Integrante 3
- CRUD;
- interface;
- segurança e validações.

### Integrante 4
- testes;
- problemas encontrados;
- demonstração;
- conclusão.

Todos devem saber responder perguntas sobre CRUD, SQLite, Kivy e RM único.
