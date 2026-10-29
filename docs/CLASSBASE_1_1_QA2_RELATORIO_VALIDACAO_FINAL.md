# ClassBase 1.1 — Relatório de validação física QA2

**Data:** 29/10/2026  
**Aparelho:** POCO C75 4G, Android 16  
**Aplicativo validado:** ClassBase 1.1 QA2 / versão Android 0.2.3  
**Pacote isolado:** `org.classbase.qa2.classbase`  
**Branch-fonte:** `fix/classbase-11-mobile-qa-safety`  
**Commit que gerou a build:** `a270e5b0ecafe04103d4a4e5d819f5a73077eaeb`  
**GitHub Actions:** https://github.com/enzogazevedo14-droid/ClassBase/actions/runs/40968316340 (success)  
**Resultado desta rodada:** **8/8 PASS** (validações físicas informadas pelo testador)

## Escopo e método

A verificação foi realizada manualmente no aparelho físico, com dados fictícios. Todos os resultados de QA2 abaixo foram relatados como PASS pelo testador; não se trata de uma execução automatizada do aplicativo pelo assistente.

A versão 0.2.3 QA2 foi instalada como aplicativo separado da versão 0.2.2 DEV, para preservar o banco SQLite e evitar dependência da assinatura debug gerada no CI. Não há evidência de teste de atualização in-place entre os pacotes.

## Resultados da rodada QA2 (0.2.3)

| Teste | Caso | Resultado |
| --- | --- | --- |
| QA2-01 | Instalação, abertura e login | PASS |
| QA2-02 | Editar nome de curso e salvar com teclado Android aberto | PASS |
| QA2-03 | Caixa de confirmação em curso; botão inicialmente desabilitado; marcar caixa habilita; cancelar mantém o curso | PASS |
| QA2-04 | Excluir curso fictício sem alunos após confirmação; outros cursos preservados; histórico registra | PASS |
| QA2-05 | Caixa de confirmação em aluno; botão inicialmente desabilitado; cancelar mantém o aluno | PASS |
| QA2-06 | Excluir aluno fictício após confirmação; curso preservado; histórico registra | PASS |
| QA2-07 | Bloquear exclusão de curso vinculado a aluno; preservar ambos os registros | PASS |
| QA2-08 | Forçar parada pelo Android, reiniciar, fazer login e confirmar persistência de curso, aluno e histórico | PASS |

**Dados fictícios principais:** `Aluno Teste QA2` (RM `990101`, excluído no QA2-06); `Curso Vinculo QA2` e `Aluno Vinculo QA2` (RM `990102`, preservados após o QA2-07/08).

## Histórico da versão anterior 0.2.2 DEV

Foram relatados **22 PASS em 23 testes numerados**, com a seguinte ressalva:

- Teste 7: salvar edição do curso com teclado virtual aberto não funcionava ou não ficava acessível; após fechar teclado, salvamento funcionava. **Corrigido e validado fisicamente em QA2-02**.
- Teste 11: primeira tentativa de excluir curso foi relatada como exclusão sem confirmação. Numa repetição com outro curso, a confirmação e o cancelamento funcionaram, sem reproduzir a falha. O código da 0.2.2 já incluía `Popup` de confirmação; causa original **não determinada**. Proteção reforçada e fisicamente validada no QA2-03/04.
- Teste 10: seleção de opções de ordenação foi verificada, mas a correção da ordem de múltiplos alunos não foi comprovada em um conjunto suficientemente grande.

A verificação QA2 inclui uma caixa obrigatória para confirmar exclusão, além do botão de exclusão inicialmente desabilitado. O fluxo foi testado para cursos e alunos.

## Evidências de compilação e testes automatizados

- GitHub Actions, Android QA2 (testes sem Kivy, sintaxe, buildozer/Android, arquivo APK): **success**.
- Execução: https://github.com/enzogazevedo14-droid/ClassBase/actions/runs/40968316340
- Artefato: `ClassBase-1.1-QA2-0.2.3-APK` (ID 12940077099); APK **debug**, não um APK de distribuição final.
- Correções de UI: `screens/cursos.py` (ação Salvar acima do campo; tecla Concluir/Enter salva) e `screens/cursos.py` / `screens/alunos.py` (confirmação explícita em duas etapas).
- Testes estáticos de regressão: `tests/test_course_edit_layout_contract.py` e `tests/test_delete_confirmation_contract.py`.

## Decisão de qualidade

**GO para encerramento desta rodada de QA física da versão isolada 0.2.3 QA2.**  
**NO-GO para distribuição definitiva ou promoção direta da 1.1 para a `main`.**

Os oito testes aprovados não cobrem segurança de produção, atualização/migração de bases existentes, assinatura de distribuição estável ou um plano de recuperação de dados. O checkpoint da versão 1.0 e seus dados não foram modificados por esta validação.

### Pendências antes da liberação

1. Remover ou substituir a credencial demonstrativa `admin` / `classbase123` por um fluxo adequado à distribuição, com documentação e teste.
2. Definir package id final, versão de distribuição e chave de assinatura Android estável, com proteção adequada da chave.
3. Testar atualização preservando o banco SQLite **no mesmo package id**, incluindo migração/rollback/backup, antes de distribuir a versão 1.1 a usuários existentes. QA2 e DEV são pacotes distintos.
4. Executar verificação de segurança e privacidade (dados pessoais de alunos, persistência local, controle de acesso e política de recuperação).
5. Fazer checklist de release, revisão independente e prova final da APK/AAB de distribuição, incluindo regressões após qualquer mudança de código.
6. Se a ordenação exata de vários alunos for requisito de aceite, validar com mais registros e diferentes critérios.

**Status final registrado:** QA2-08 PASS, **8/8 QA2 PASS**; distribuição final pendente de etapas próprias.
