# ClassBase 1.1 RC2 — Pré-QA física

## Checkpoint de código

```text
8040577
fix: harden ClassBase 1.1 pre-physical RC
```

Branch:

```text
release/classbase-1.1-rc
```

A `main` e a tag da 1.0 aprovada não foram alteradas.

## Testes automatizados

```text
83/83 PASS
```

Compilação Python com `compileall`: PASS.

## Riscos encontrados e corrigidos nesta rodada

### Curso padrão reaparecia

Antes, os cursos padrão eram inseridos com `INSERT OR IGNORE` em toda inicialização.

Isso permitia que um curso padrão excluído reaparecesse após reabrir o app.

Correção:

- cursos padrão só são semeados quando a tabela `cursos` é criada pela primeira vez;
- teste de regressão confirma que curso excluído continua excluído.

### Salvar sem mudanças poluía auditoria

Antes, salvar um aluno sem modificar os campos alterava `updated_at` e criava histórico.

Correção:

- dados idênticos não alteram timestamp;
- não é criado evento sem mudança real;
- mesma regra para curso com nome idêntico.

### Layout de telas menores

Home e Detalhes cresceram com a 1.1 e poderiam ficar apertadas em viewports menores.

Correção:

- ambas agora utilizam `ScrollView`;
- cadastro e edição já eram roláveis;
- testes garantem que essas telas continuem roláveis.

### Popup de curso e histórico longo

- popup de edição de curso agora usa altura fixa mobile-safe;
- cards do histórico ganharam mais espaço vertical para descrições longas.

## Testes adicionais

A suíte agora inclui:

- rollback se a gravação de histórico falhar;
- `PRAGMA integrity_check`;
- `PRAGMA foreign_key_check`;
- pesquisa com string semelhante a SQL injection;
- ORDER BY inválido/malicioso;
- migração de banco 1.0 com 120 alunos;
- CRUD normal após a migração;
- ausência de eventos falsos;
- responsividade estrutural.

## APK RC2

```text
ClassBase-1.1-DEV-RC2-0.2.1-debug.apk
```

Package:

```text
org.classbase.dev.classbase
```

Versão:

```text
0.2.1
```

ABI:

```text
arm64-v8a
```

Tamanho:

```text
23.328.354 bytes
```

SHA-256:

```text
6FF40D62189CBD1140E7F1AD3B97E7E67D1E7213F8E13D84875C643988C44809
```

APK Signature Scheme v2: PASS.

Arquivos:

```text
C:\Users\User\Downloads\ClassBase-1.1-DEV-RC2-0.2.1-debug.apk
C:\Users\User\Documents\ClassBase\dist\ClassBase-1.1-DEV-RC2-0.2.1-debug.apk
```

## O que ainda não pode receber PASS sem aparelho

- renderização real das novas telas no Android;
- rolagem touch real;
- teclado nos novos fluxos;
- popup de edição de curso no teclado Android;
- densidade/fonte no aparelho;
- navegação manual completa;
- persistência após encerramento do processo Android;
- comportamento após atualização do APK DEV.

## Gate atual

```text
CÓDIGO: PASS
BANCO: PASS
MIGRAÇÃO: PASS
TESTES: PASS
APK BUILD: PASS
ASSINATURA: PASS
QA FÍSICA 1.1: PENDENTE
PROMOÇÃO PARA MAIN: BLOQUEADA ATÉ QA FÍSICA
```
