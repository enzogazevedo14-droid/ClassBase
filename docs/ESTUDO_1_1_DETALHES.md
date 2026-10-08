# ClassBase 1.1 — Como explicar Datas e Detalhes do Aluno

## O que foi adicionado

A tabela `alunos` agora possui:

```text
created_at
updated_at
```

Esses campos registram:

- quando o aluno foi cadastrado;
- quando o cadastro foi alterado pela última vez.

Também foi criada a tela `detalhes`, que mostra:

- nome;
- RM;
- curso;
- data de cadastro;
- última atualização.

## Por que adicionar essas datas?

Porque um sistema real normalmente precisa saber quando um registro foi criado e quando foi alterado.

Elas também ajudam a demonstrar persistência e evolução do registro no banco de dados.

## Como funciona no cadastro

Antes do `INSERT`, o Python gera o horário atual em UTC.

Depois o Repository executa uma inserção equivalente a:

```sql
INSERT INTO alunos (
    rm,
    nome,
    curso_id,
    created_at,
    updated_at
)
VALUES (?, ?, ?, ?, ?)
```

No primeiro cadastro, `created_at` e `updated_at` recebem o mesmo horário.

## Como funciona na edição

Quando o aluno é atualizado:

```sql
UPDATE alunos
SET
    rm = ?,
    nome = ?,
    curso_id = ?,
    updated_at = ?
WHERE id = ?
```

O `created_at` não é alterado.

Assim:

```text
created_at = quando nasceu o registro
updated_at = última modificação
```

## Por que usamos UTC no banco?

UTC é um horário de referência independente de fuso horário.

O banco armazena o horário de forma consistente e a tela converte para o horário local do dispositivo antes de mostrar ao usuário.

## Como funciona a tela Detalhes

Na lista de alunos existe a ação `Detalhes`.

Ela chama:

```python
open_detail(student_id)
```

Essa função encontra a tela `detalhes` e chama:

```python
detail_screen.load_student(student_id)
```

A tela consulta o aluno pelo ID e preenche os componentes visuais.

Fluxo:

```text
Lista de alunos
      ↓
open_detail(id)
      ↓
StudentDetailScreen
      ↓
get_student(id)
      ↓
StudentRepository
      ↓
SQLite
      ↓
dados voltam para a tela
```

## Por que usamos o ID e não o nome?

Porque nomes podem se repetir.

O `id` é a chave primária interna e identifica exatamente um registro.

## Onde a aparência da tela fica?

```text
screens/detalhes.py
```

controla comportamento e carregamento de dados.

```text
kv/detalhes.kv
```

controla a estrutura visual.

Essa é a mesma separação usada nas outras telas do projeto.

## Migração

A versão 1.1 anterior já possuía `curso_id`, mas não possuía as datas.

A migração detecta esse caso e recria a estrutura mais nova preservando:

- ID;
- RM;
- nome;
- curso relacionado.

Depois preenche as datas dos registros antigos.

O banco agora utiliza `PRAGMA user_version = 3` para indicar a versão atual do schema.

## Perguntas prováveis

**Qual a diferença entre created_at e updated_at?**

`created_at` representa a criação do registro. `updated_at` representa a última alteração.

**Por que created_at não muda quando editamos?**

Porque ele representa um fato histórico: quando o registro foi criado.

**Por que guardar isso no banco e não somente mostrar a hora atual?**

Porque a informação precisa permanecer salva mesmo depois que o aplicativo fecha.

**Por que a tela usa o ID para carregar o aluno?**

Porque o ID é único e identifica exatamente o registro que foi selecionado.

**O que acontece com alunos antigos ao atualizar o banco?**

A migração preserva os registros e acrescenta os campos necessários. Isso é coberto por testes automatizados.
