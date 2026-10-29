# ClassBase 1.1 DEV 0.2.2 — QA física (POCO C75)

Estado: APROVAÇÃO FINAL BLOQUEADA — testes manuais em andamento.
APK QA anterior: `classbase-0.2.2-arm64-v8a-debug.apk` compilado na execução GitHub Actions #2.
Branch do APK observado: `ci/classbase-1.1-android-qa`, commit `af7eff9`.
Branch desta correção: `fix/classbase-11-mobile-qa-safety`.

## Resultados comunicados pelo testador

| ID | Caso | Estado |
|---|---|---|
| 1 | Login e Home | PASS |
| 2 | Cadastro e listagem de aluno fictício | PASS |
| 3 | RM duplicado rejeitado | PASS |
| 4 | Editar aluno sem alterar demais dados | PASS |
| 5 | Persistência após forçar parada | PASS |
| 6 | Criar curso de teste | PASS |
| 7 | Editar curso / teclado Android | RESSALVA: salvar funcionou **após fechar o teclado**, botão inacessível ou sem efeito com teclado aberto |
| 8 | Desativar e reativar curso | PASS |
| 9 | Histórico de operações legível | PASS |
| 10 | Busca por nome/RM, filtro de curso e mudança de ordenação | PASS — ordenação efetiva não validada com múltiplos alunos |
| 11 | Cancelar exclusão de curso | FAIL REPORTADO: ao tocar em Excluir, curso teria sido apagado sem confirmação |

## Observações e diagnósticos pendentes

- O código do APK 0.2.2 já continha um `Popup` com `Cancelar` e `Excluir`, e apenas o botão interno chamava `delete_course`.
- A discrepância entre o código e o comportamento físico relatado exige investigação; NÃO afirmar causa como confirmada.
- Confirmar pelo histórico local (somente leitura) se houve o evento de exclusão do curso; não efetuar novas exclusões até reteste controlado.
- Não descartar ou limpar o banco SQLite de teste enquanto a investigação estiver aberta.
- A v1.0 aprovada permanece intacta; não mesclar a v1.1 na `main`.

## Hardening proposto nesta branch

- Curso e aluno: confirmação em duas ações distintas: marcar caixa de ciência e tocar em Excluir; botão inicia desabilitado.
- Proteção no próprio callback contra exclusão sem a caixa marcada.
- O patch **não está validado fisicamente**. Requer novo APK e teste Android antes de qualquer promoção.
- APKs debug assinados em runners efêmeros podem ter chaves diferentes; não presumir atualização in-place mantendo dados. Planejar chave de assinatura estável e backup de teste antes de instalar outra build.
