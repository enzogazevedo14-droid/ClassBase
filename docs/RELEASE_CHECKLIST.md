# Checklist de QA física — ClassBase 0.1.0 RC

APK aprovado nesta rodada: `dist/ClassBase-0.1.0-qa-pass-debug.apk`.

Legenda: `[x]` validado no aparelho real; `[A]` coberto por teste automatizado e não repetido manualmente nesta rodada.

## Instalação e abertura

- [x] Instalar/atualizar o APK sem erro.
- [A] Conferir separadamente o ícone no launcher; o ícone foi empacotado e validado no build.
- [x] Abrir o aplicativo em orientação retrato.
- [x] Confirmar o presplash do ClassBase.
- [x] Confirmar que a tela de login aparece sem cortes ou tela preta.
- [x] Confirmar que teclado e campos de texto funcionam.

## Login e sessão

- [x] Login com `admin` / `classbase123`.
- [A] Login inválido mostra mensagem e não entra.
- [x] Botão Sair retorna ao login.
- [x] Após sair, usuário, senha e mensagem ficam vazios.

## CRUD de alunos

- [x] Cadastrar aluno com RM, nome e curso.
- [A] Bloquear cadastro com campos obrigatórios vazios.
- [x] Bloquear RM duplicado.
- [x] Confirmar contador atualizado na Home.
- [x] Pesquisar por RM.
- [x] Pesquisar por nome.
- [x] Pesquisar por curso.
- [x] Editar e salvar cadastro no aparelho.
- [A] Alterar RM, nome e curso juntos em um único cenário.
- [x] Bloquear RM duplicado durante edição.
- [x] Cancelar uma exclusão sem apagar o aluno.
- [x] Confirmar uma exclusão e remover o aluno.

## Persistência e usabilidade

- [x] Fechar completamente o processo e abrir novamente.
- [x] Confirmar que os alunos continuam salvos após reinício.
- [x] Confirmar persistência após atualização do APK.
- [A] Stress de lista longa/rolagem com muitos registros.
- [x] Confirmar que nome, RM e curso cabem nos cartões.
- [x] Confirmar que Editar e Excluir são fáceis de tocar.
- [x] Confirmar formulário de cadastro utilizável com teclado aberto.
- [x] Confirmar formulário de edição utilizável com teclado aberto.
- [x] Confirmar Salvar alterações funcionando com teclado aberto.
- [x] Confirmar feedback de sucesso em verde.
- [x] Remover todos os registros criados apenas para QA.

## Gate

**Gate crítico de demonstração escolar: PASS.**

O commit validado é `ee5216b` e a tag correspondente é `android-qa-pass-0.1.0`.

Os itens `[A]` permanecem cobertos pela suíte automatizada de 29 testes, mas não foram repetidos manualmente no POCO C75 nesta rodada. Para um gate físico exaustivo de produção, esses cenários ainda podem ser repetidos manualmente.
