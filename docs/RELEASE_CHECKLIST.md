# Checklist de QA física — ClassBase 0.1.0 RC

Execute este checklist no APK `dist/ClassBase-0.1.0-rc-debug.apk`.

## Instalação e abertura

- [ ] Instalar o APK sem erro.
- [ ] Abrir o aplicativo em orientação retrato.
- [ ] Confirmar que a tela de login aparece sem cortes ou tela preta.
- [ ] Confirmar que teclado e campos de texto funcionam.

## Login e sessão

- [ ] Login com `admin` / `classbase123`.
- [ ] Login inválido mostra mensagem e não entra.
- [ ] Botão Sair retorna ao login.
- [ ] Após sair, usuário, senha e mensagem ficam vazios.

## CRUD de alunos

- [ ] Cadastrar aluno com RM, nome e curso.
- [ ] Bloquear cadastro com campos obrigatórios vazios.
- [ ] Bloquear RM duplicado.
- [ ] Confirmar contador atualizado na Home.
- [ ] Pesquisar por RM.
- [ ] Pesquisar por nome.
- [ ] Pesquisar por curso.
- [ ] Editar RM, nome e curso.
- [ ] Bloquear RM duplicado durante edição.
- [ ] Cancelar uma exclusão sem apagar o aluno.
- [ ] Confirmar uma exclusão e remover o aluno.

## Persistência e usabilidade

- [ ] Fechar o aplicativo completamente.
- [ ] Abrir novamente e confirmar que os alunos continuam salvos.
- [ ] Confirmar que listas longas rolam normalmente.
- [ ] Confirmar que nome, RM e curso cabem nos cartões.
- [ ] Confirmar que Editar e Excluir são fáceis de tocar.
- [ ] Confirmar que nenhuma tela estoura ou fica escondida pelo teclado.

## Gate

O RC só vira entrega aprovada quando todos os itens acima estiverem concluídos sem crash ou perda de dados.

Se houver falha, registrar a ação exata, a tela e, quando possível, coletar o log via ADB antes de alterar o código.
