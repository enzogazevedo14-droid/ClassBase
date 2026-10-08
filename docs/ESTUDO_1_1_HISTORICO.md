# ClassBase 1.1 — Como explicar o Histórico de Alterações

## O que foi adicionado

Foi criada a tabela `historico` para registrar ações importantes executadas no ClassBase.

Ela armazena:

```text
id
entidade
registro_id
acao
descricao
created_at
```

Exemplos de eventos:

```text
Aluno · Criado
Ana Souza (RM 100) cadastrada no curso Administração.

Aluno · Atualizado
Ana Souza (RM 101): RM 100 → 101; Curso DS → Administração.

Curso · Desativado
Curso Administração desativado.
```

## Por que criar um histórico?

Em sistemas reais é útil saber o que aconteceu com os dados.

O histórico ajuda a responder perguntas como:

- quando um aluno foi cadastrado;
- quando seus dados foram alterados;
- quando um registro foi excluído;
- quando um curso foi ativado ou desativado.

Esse conceito também é chamado de auditoria ou trilha de auditoria.

## Por que o histórico é uma tabela separada?

O histórico representa acontecimentos, não o estado atual do aluno ou curso.

Por isso ele não deve ser misturado com a tabela `alunos` ou `cursos`.

```text
alunos     -> estado atual dos alunos
cursos     -> estado atual dos cursos
historico  -> ações que já aconteceram
```

## Por que historico.registro_id não é uma chave estrangeira?

Essa decisão é proposital.

Quando um aluno é excluído, queremos manter no histórico a informação de que aquele aluno existiu e foi excluído.

Se `registro_id` tivesse uma chave estrangeira obrigatória apontando para `alunos`, excluir o aluno poderia:

- bloquear a exclusão; ou
- obrigar a apagar o histórico.

Para auditoria, queremos que o evento permaneça.

## O que faz record_history?

É uma função usada pelos repositórios para inserir um evento na tabela `historico`.

Ela recebe:

```text
entidade
registro_id
ação
descrição
data/hora
```

A interface não grava histórico diretamente.

Fluxo:

```text
Tela
  ↓
StudentRepository / CourseRepository
  ↓
operação principal no SQLite
  ↓
record_history()
  ↓
tabela historico
```

## Por que registrar dentro da mesma transação?

Esta é uma das decisões mais importantes.

Exemplo de cadastro:

```text
BEGIN
  inserir aluno
  inserir histórico
COMMIT
```

Se algo der errado:

```text
ROLLBACK
```

Assim não fica uma situação em que:

- o aluno foi criado mas o histórico não foi; ou
- o histórico diz que foi criado, mas o cadastro falhou.

Os dois registros são confirmados juntos.

## O que registramos nos alunos?

### Criação

Registra nome, RM e curso.

### Atualização

Compara o valor antigo com o novo.

Somente as diferenças aparecem na descrição.

Exemplo:

```text
RM: 100 → 101
Nome: Ana → Ana Souza
Curso: Administração → Desenvolvimento de Sistemas
```

### Exclusão

Antes de apagar, o Repository busca os dados necessários.

Depois executa o `DELETE` e registra no histórico quem foi excluído.

O evento permanece mesmo depois que o aluno não existe mais.

## O que registramos nos cursos?

- criação;
- alteração de nome;
- ativação;
- desativação;
- exclusão.

Os cursos criados automaticamente na primeira execução não geram histórico, pois não foram uma ação do usuário.

## HistoryRepository

O `HistoryRepository` é responsável por consultar a tabela de histórico.

O método principal é:

```python
list_events(entity="", limit=100)
```

Ele permite:

- mostrar todos os eventos;
- mostrar apenas eventos de alunos;
- mostrar apenas eventos de cursos;
- limitar a quantidade retornada;
- ordenar do mais recente para o mais antigo.

## Tela Histórico de ações

A tela possui:

- filtro Todos;
- filtro Alunos;
- filtro Cursos;
- quantidade de ações;
- lista dos eventos em ordem decrescente.

Arquivos:

```text
screens/historico.py
kv/historico.kv
```

O Python controla os dados e o KV controla a apresentação.

## Versão do banco

Com a tabela de histórico, o schema passa a usar:

```text
PRAGMA user_version = 4
```

A migração continua aceitando bancos das versões anteriores.

## Perguntas prováveis

**O que é uma trilha de auditoria?**

É um registro das ações que aconteceram no sistema ao longo do tempo.

**Por que o histórico não é apagado quando o aluno é excluído?**

Porque justamente queremos preservar a informação de que a exclusão aconteceu.

**Por que registrar na mesma transação?**

Para garantir consistência. A alteração principal e seu histórico são confirmados ou desfeitos juntos.

**O que é rollback nesse caso?**

É o cancelamento da transação quando ocorre um erro, evitando salvar apenas uma parte da operação.

**Por que não registrar os cursos padrão criados automaticamente?**

Porque o histórico deve representar ações relevantes do usuário, e não a preparação interna inicial do banco.

**Onde a tela salva o histórico?**

Ela não salva diretamente. Quem registra são os Repositories durante as operações.
