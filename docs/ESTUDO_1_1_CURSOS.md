# ClassBase 1.1 — Como explicar a melhoria de Cursos

## O que mudou

Na versão 1.0, o curso era salvo diretamente dentro da tabela de alunos como texto.

Exemplo:

```text
alunos
id | rm | nome | curso
```

Na versão 1.1, criamos uma tabela própria para cursos:

```text
cursos
id | nome | ativo
```

e a tabela de alunos passou a guardar `curso_id`:

```text
alunos
id | rm | nome | curso_id
```

O campo `curso_id` é uma chave estrangeira que aponta para `cursos.id`.

## Como explicar ao professor

> Antes o curso era um texto repetido em cada aluno. Na 1.1 nós normalizamos o banco criando uma tabela própria de cursos e relacionando alunos a cursos por chave estrangeira. Dessa forma, o curso possui um identificador único e pode ser administrado sem duplicar sua informação em cada registro de aluno.

## Conceitos envolvidos

### Chave primária

`cursos.id` identifica cada curso de maneira única.

### Chave estrangeira

`alunos.curso_id` guarda o ID do curso relacionado ao aluno.

### Relacionamento 1:N

Um curso pode possuir vários alunos, enquanto cada aluno possui um curso.

```text
CURSO 1 -------- N ALUNOS
```

### Integridade referencial

O SQLite impede excluir fisicamente um curso que ainda esteja ligado a alunos.

Isso acontece pela chave estrangeira com `ON DELETE RESTRICT`.

## Por que não continuar salvando o nome do curso no aluno?

Porque teríamos repetição.

Exemplo antigo:

```text
Ana    | Desenvolvimento de Sistemas
Bruno  | Desenvolvimento de Sistemas
Carlos | Desenvolvimento de Sistemas
```

Se o nome do curso precisasse ser alterado, vários registros poderiam precisar de atualização.

Na nova estrutura:

```text
cursos
1 | Desenvolvimento de Sistemas

alunos
Ana    | 1
Bruno  | 1
Carlos | 1
```

Todos apontam para o mesmo curso.

## O que faz CourseRepository

A classe `CourseRepository` centraliza operações no banco relacionadas a cursos:

- `create_course`: cadastra curso;
- `get_course`: busca um curso;
- `list_courses`: lista cursos;
- `update_course`: altera o nome;
- `set_course_active`: ativa ou desativa;
- `delete_course`: exclui se não houver aluno vinculado;
- `count_students`: conta alunos ligados ao curso.

A tela não executa SQL diretamente.

```text
Tela de Cursos
      ↓
CourseRepository
      ↓
SQLite
```

## Por que existe ativo/inativo?

Desativar um curso é diferente de excluir.

Um curso inativo permanece no banco e pode continuar ligado a alunos antigos, mas deixa de aparecer como opção para novos cadastros.

Isso preserva o histórico.

## O que acontece no cadastro de aluno

A tela carrega os cursos ativos do banco.

Quando o usuário escolhe um curso:

```text
Nome do curso
     ↓
StudentRepository
     ↓
busca cursos.id
     ↓
salva curso_id em alunos
```

A interface continua mostrando o nome do curso porque as consultas usam `JOIN` entre `alunos` e `cursos`.

## O que é JOIN neste projeto?

A tabela de alunos tem o ID do curso, não o nome.

Por isso usamos:

```sql
SELECT ...
FROM alunos AS a
JOIN cursos AS c ON c.id = a.curso_id
```

O JOIN combina os dados relacionados das duas tabelas.

## Migração da versão 1.0

Não apagamos os dados antigos.

A inicialização detecta se a tabela antiga ainda possui a coluna `curso`.

Se possuir:

1. lê os cursos antigos;
2. cria esses cursos na tabela `cursos`;
3. cria a nova tabela de alunos com `curso_id`;
4. copia os alunos preservando RM e nome;
5. relaciona cada aluno ao curso correto;
6. substitui a tabela antiga.

Existe teste automatizado específico verificando que um aluno da versão 1.0 continua existindo depois da migração.

## Perguntas prováveis

**Por que usar chave estrangeira?**  
Para representar e proteger o relacionamento entre aluno e curso.

**Por que não salvar apenas o ID e nunca fazer JOIN?**  
O ID é adequado para relacionamento interno, mas a interface precisa mostrar o nome. O JOIN recupera os dois dados relacionados.

**Por que não excluir um curso com alunos?**  
Isso deixaria alunos apontando para um curso inexistente. A integridade referencial impede esse estado inválido.

**Por que desativar curso?**  
Para impedir novos vínculos sem apagar o histórico de alunos que já pertenciam ao curso.

**A versão antiga perde dados?**  
Não. A migração automática foi criada e testada especificamente para preservar os registros.
