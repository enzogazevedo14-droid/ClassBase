# ClassBase 1.1 — Estado do Release Candidate

## Objetivo

A versão 1.1 evolui o ClassBase sem alterar sua proposta escolar principal:

- gerenciamento de alunos;
- Python;
- Kivy;
- SQLite;
- CRUD;
- funcionamento local/offline.

A versão 1.0 fisicamente aprovada continua preservada pela tag `android-qa-pass-0.1.0`.

## Checkpoint atual

Branch:

```text
release/classbase-1.1-rc
```

Commit de código do RC2:

```text
8040577
fix: harden ClassBase 1.1 pre-physical RC
```

A `main` ainda permanece na versão 1.0/documentação aprovada. A 1.1 não será promovida antes da QA física.

## Melhorias implementadas

### Cursos como entidade do banco

- tabela `cursos`;
- relacionamento 1:N;
- `alunos.curso_id` como chave estrangeira;
- CRUD de cursos;
- ativar/desativar cursos;
- proteção contra exclusão de curso vinculado;
- migração de alunos antigos sem perda de dados;
- cursos padrão inseridos somente na criação inicial da tabela.

### Datas e detalhes do aluno

- `created_at`;
- `updated_at`;
- tela Detalhes do aluno;
- conversão UTC → horário local para exibição;
- salvar sem mudanças não altera `updated_at`.

### Dashboard, filtros e ordenação

- total de alunos;
- distribuição por curso;
- `COUNT`;
- `GROUP BY`;
- `LEFT JOIN`;
- filtro por curso;
- pesquisa combinada;
- ordenação por nome, RM ou mais recentes;
- contador de resultados.

### Histórico de alterações

- tabela `historico`;
- criação/edição/exclusão de aluno;
- criação/edição/ativação/desativação/exclusão de curso;
- histórico na mesma transação da operação principal;
- histórico preservado após exclusão;
- filtro por entidade;
- operações sem mudança real não geram eventos artificiais.

### Responsividade preventiva

- Home rolável;
- Cadastro rolável;
- Edição rolável;
- Detalhes rolável;
- popup de edição de curso com altura fixa;
- cards do histórico com mais espaço para descrições longas;
- teclado configurado em modo `resize`.

## Schema SQLite

```text
PRAGMA user_version = 4
```

Migrações cobertas:

- formato 1.0 com curso como texto;
- formato relacional anterior sem timestamps;
- reabertura repetida/idempotência;
- banco legado com 120 alunos;
- continuidade de CRUD após migração.

## Testes automatizados

Estado atual:

```text
83/83 PASS
```

Também passou:

- `python -m compileall`;
- `git diff --check`;
- auditoria UTF-8 sem caracteres de substituição;
- `PRAGMA integrity_check = ok`;
- `PRAGMA foreign_key_check` sem erros.

A suíte inclui testes de:

- autenticação;
- senha sem texto puro;
- CRUD de alunos;
- cursos e integridade referencial;
- migrações;
- timestamps;
- detalhes;
- dashboard;
- filtros;
- ordenação;
- histórico;
- rollback transacional;
- tentativa de entrada semelhante a SQL injection;
- responsividade estrutural;
- navegação;
- persistência.

## APK DEV RC2

O RC2 foi gerado a partir do código do commit `8040577`.

- Título: `ClassBase 1.1 DEV`
- Versão: `0.2.1`
- Package: `org.classbase.dev.classbase`
- ABI: `arm64-v8a`
- minSdk: 24
- targetSdk: 33
- Tamanho: 23.328.354 bytes
- APK Signature Scheme v2: PASS
- Buildozer/Gradle: PASS
- SHA-256: `6FF40D62189CBD1140E7F1AD3B97E7E67D1E7213F8E13D84875C643988C44809`

Arquivos:

```text
C:\Users\User\Downloads\ClassBase-1.1-DEV-RC2-0.2.1-debug.apk
C:\Users\User\Documents\ClassBase\dist\ClassBase-1.1-DEV-RC2-0.2.1-debug.apk
```

O APK anterior 0.2.0 deve ser considerado **superado pelo RC2 0.2.1**.

## Isolamento da versão 1.0

A 1.1 usa package diferente da 1.0:

```text
1.0: org.classbase.classbase
1.1 DEV: org.classbase.dev.classbase
```

Portanto os dois podem coexistir no Android com bancos separados.

A alteração de package/título/versão foi feita apenas na cópia de build do WSL. O `buildozer.spec` versionado foi restaurado e o repositório WSL voltou a ficar limpo.

## QA física

Ainda pendente.

O que precisa ser validado no aparelho:

1. instalação lado a lado com a 1.0;
2. abertura/presplash/login;
3. Home e rolagem;
4. cadastro;
5. cursos;
6. detalhes;
7. edição;
8. busca/filtro/ordenação;
9. dashboard;
10. histórico;
11. teclado nos novos fluxos;
12. persistência ao encerrar/reabrir;
13. atualização do APK DEV preservando o banco;
14. ausência de crash/logcat fatal.

## Gate atual

```text
CÓDIGO                     PASS
BANCO                      PASS
MIGRAÇÕES                  PASS
TESTES AUTOMATIZADOS       83/83 PASS
COMPILAÇÃO PYTHON          PASS
APK ANDROID RC2            PASS
ASSINATURA V2              PASS
QA FÍSICA 1.1              PENDENTE
MERGE EM MAIN              BLOQUEADO ATÉ QA FÍSICA
```

## Materiais de defesa

- `GUIA_DEFESA_CODIGO_1_1.md`;
- `COMPARACAO_FERRAMENTAS.md`;
- `MAPA_TELAS_CODIGO_1_1.md`;
- `ESTUDO_1_1_CURSOS.md`;
- `ESTUDO_1_1_DETALHES.md`;
- `ESTUDO_1_1_DASHBOARD_FILTROS.md`;
- `ESTUDO_1_1_HISTORICO.md`;
- `PRE_QA_FISICA_RC2.md`.
