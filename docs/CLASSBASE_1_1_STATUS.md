# ClassBase 1.1 — Release Candidate de desenvolvimento

## Objetivo

A versão 1.1 evolui o ClassBase sem alterar sua proposta escolar principal:

- gerenciamento de alunos;
- Python;
- Kivy;
- SQLite;
- CRUD;
- funcionamento local/offline.

A versão 1.0 fisicamente aprovada continua preservada pela tag `android-qa-pass-0.1.0`.

## Melhorias implementadas

### 1. Cursos como entidade do banco

- tabela `cursos`;
- relacionamento 1:N;
- `alunos.curso_id` como chave estrangeira;
- CRUD de cursos;
- ativar/desativar cursos;
- proteção contra exclusão de curso vinculado;
- migração de alunos antigos sem perda de dados.

### 2. Datas e detalhes do aluno

- `created_at`;
- `updated_at`;
- tela Detalhes do aluno;
- conversão do horário UTC para o horário local na interface.

### 3. Dashboard, filtros e ordenação

- quantidade total de alunos;
- distribuição por curso;
- `COUNT`;
- `GROUP BY`;
- `LEFT JOIN`;
- filtro por curso;
- pesquisa combinada;
- ordenação por nome, RM ou data de cadastro;
- contador de resultados.

### 4. Histórico de alterações

- tabela `historico`;
- criação/edição/exclusão de aluno;
- criação/edição/ativação/desativação/exclusão de curso;
- registro na mesma transação da operação principal;
- histórico preservado após exclusão;
- tela de histórico com filtro por entidade.

## Versão do schema SQLite

```text
PRAGMA user_version = 4
```

A inicialização migra os formatos anteriores aceitos pelo projeto para o schema atual.

## Testes automatizados

Checkpoint anterior ao APK DEV:

```text
68/68 PASS
```

A suíte cobre, entre outros:

- autenticação;
- CRUD de alunos;
- CRUD/regras de cursos;
- migrações;
- timestamps;
- tela de detalhes;
- dashboard;
- filtros e ordenação;
- histórico/auditoria;
- navegação;
- persistência;
- UX mobile já existente.

## Estratégia de QA Android

A 1.1 não será instalada sobre a versão 1.0 neste primeiro teste.

O APK de desenvolvimento utilizará outro package ID:

```text
org.classbase.classbase11dev
```

Título:

```text
ClassBase 1.1 DEV
```

Versão:

```text
0.2.0
```

Isso permite manter lado a lado:

```text
ClassBase 1.0 aprovado
ClassBase 1.1 DEV
```

com bancos separados no Android.

## Gate para promover a 1.1

Antes de substituir a versão principal:

1. build Android isolado;
2. instalar como app DEV;
3. validar telas novas;
4. validar cadastro/edição/exclusão;
5. validar cursos;
6. validar detalhes;
7. validar filtros/dashboard;
8. validar histórico;
9. verificar teclado e layouts;
10. repetir suíte automatizada;
11. somente então decidir merge/promoção.
