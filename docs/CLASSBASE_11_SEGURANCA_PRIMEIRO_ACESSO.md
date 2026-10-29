# ClassBase 1.1 — Validação de autenticação segura de primeira execução

**Data:** 29/10/2026  
**Estado:** candidato em branch isolada; NÃO publicado e NÃO validado fisicamente no Android.  
**Branch:** `feat/classbase-11-first-run-security`  
**Base:** `fix/classbase-11-mobile-qa-safety` (QA2 0.2.3, 8/8 verificações físicas PASS)

## Problema encontrado

Antes da mudança, a aplicação executava `manager.auth_repository.ensure_default_user()` em cada inicialização. Em um banco vazio, era criada automaticamente a credencial conhecida `admin` / `classbase123`, adequada apenas à demonstração. A alteração não modifica dados existentes nem elimina a base SQLite.

## Novo fluxo de primeiro acesso

1. Se **não existir nenhuma conta** em `usuarios`, o usuário é levado a **Configurar ClassBase**, em vez de receber uma conta e senha pública.
2. O responsável informa nome de usuário, nova senha e confirmação; mínimo de 12 e máximo de 128 caracteres. Não aceitar senha de demonstração, senha igual ao nome de usuário, espaços nas extremidades ou confirmação divergente.
3. A criação inicial acontece em transação SQLite com `BEGIN IMMEDIATE`; depois de concluída, uma nova tentativa de criar a conta inicial falha.
4. Senhas são salvas apenas por `PBKDF2-HMAC-SHA256` com 200 mil iterações, salt aleatório de 16 bytes. A senha não é copiada para log.
5. A conta criada deve fazer **login normalmente**. O fluxo de configuração não concede sessão automática.

## Instalações legadas com senha de demonstração

- O banco de dados anterior é mantido.
- Uma conta `admin` que ainda autentica com `classbase123` é redirecionada obrigatoriamente à tela **Atualizar senha**, antes de abrir a Home.
- A atualização exige a **senha atual**, senha nova, confirmação e preserva os alunos, cursos e histórico.
- O hash e o salt são trocados atomicamente. A tentativa com senha atual incorreta não altera nada.
- Após a mudança, o usuário deve autenticar novamente; a senha de demonstração não poderá mais ser usada.
- Contas legadas com senha própria não são forçadas a trocar de senha neste fluxo.

## Limitações / riscos residuais

- O armazenamento do banco é **local**. Não há restauração de senha perdida implementada; o responsável deve guardar a senha em local seguro. Um plano seguro de backup/recuperação precisa ser preparado separadamente, antes de dados reais.
- A primeira conta tem acesso local aos cadastros, sem permissões por perfil. Ainda não existem expiração de sessão, bloqueio progressivo por tentativas ou autenticação biométrica. Esses requisitos precisam de avaliação conforme o uso pretendido.
- O método interno `create_user` é mantido para compatibilidade de testes e bancos existentes; as telas novas usam exclusivamente `initialize_owner` e `change_password`.
- A contagem de usuários define a tela inicial; caso existam alunos mas nenhuma conta, o fluxo também exige criação de conta inicial. Não há migração destrutiva de dados.
- Nunca colocar uma senha pessoal ou uma chave de assinatura no repositório ou nos logs do CI.

## Evidências de validação

- Testes automatizados de criação de conta, senha inválida/curta, conta única, rotação de senha legada, senha antiga incorreta, preservação de aluno/curso, hash e salt e ligação estática das telas.
- Workflow de testes Python: `.github/workflows/classbase-11-first-run-auth.yml`.
- **Ainda falta**: instalar APK de teste em um pacote isolado (não sobrepor QA2), validar teclado e telas de configuração no POCO C75, fazer teste de migração/atualização da mesma identidade Android, preparar chave de assinatura estável e avaliar segurança/privacidade.

## Gate

**GO** apenas para análise e testes automatizados da branch isolada.  
**NO-GO** para merge em `main`, distribuição final ou substituição da QA2 sem validação Android.
