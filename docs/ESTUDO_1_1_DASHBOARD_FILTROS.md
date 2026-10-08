# ClassBase 1.1 — Como explicar Dashboard, Filtros e Ordenação

## O que foi adicionado

A Home agora mostra:

- total de alunos;
- quantidade de alunos por curso.

A tela de alunos agora permite:

- pesquisar;
- filtrar por curso;
- ordenar por nome;
- ordenar por RM;
- ordenar pelos cadastros mais recentes;
- visualizar quantos resultados foram encontrados.

## Consulta agregada do dashboard

Para descobrir quantos alunos existem em cada curso, usamos uma consulta com `COUNT` e `GROUP BY`.

Conceitualmente:

```sql
SELECT
    c.nome,
    COUNT(a.id) AS total
FROM cursos AS c
LEFT JOIN alunos AS a
    ON a.curso_id = c.id
GROUP BY c.id, c.nome
```

## O que é COUNT?

`COUNT` conta registros.

Exemplo:

```text
Administração: 2
Desenvolvimento de Sistemas: 5
```

Esses números são calculados a partir do banco e não ficam escritos manualmente na interface.

## O que é GROUP BY?

`GROUP BY` agrupa linhas que possuem uma informação em comum.

No ClassBase agrupamos os alunos pelo curso para contar quantos existem em cada grupo.

## Por que LEFT JOIN no dashboard?

Queremos que um curso possa aparecer na consulta mesmo quando possui zero alunos.

Com `LEFT JOIN`, os cursos continuam presentes e o `COUNT(a.id)` pode retornar zero.

## Como funciona o filtro

O método:

```python
list_students(search="", course="", order_by="nome")
```

pode receber busca, curso e ordenação ao mesmo tempo.

Quando existe um curso selecionado, a consulta adiciona uma condição equivalente a:

```sql
c.nome = ?
```

Quando também existe pesquisa, as condições são combinadas com `AND`.

Exemplo:

```text
Pesquisa: Ana
Curso: Administração
```

O banco retorna apenas alunos que atendem às duas condições.

## Como funciona a ordenação

Existem três opções permitidas:

```text
Nome A-Z      -> ORDER BY nome
RM            -> ORDER BY rm
Mais recentes -> ORDER BY created_at DESC
```

## Por que não enviamos o nome da coluna diretamente do usuário para o SQL?

Nomes de colunas e trechos de `ORDER BY` não são tratados como valores pelos placeholders `?`.

Por isso o programa usa uma lista interna de opções permitidas:

```python
ORDER_BY = {
    "nome": ...,
    "rm": ...,
    "recentes": ...,
}
```

A interface escolhe uma dessas opções conhecidas.

Isso evita montar o SQL com um trecho arbitrário informado pelo usuário.

## Fluxo da tela de alunos

```text
usuário digita/faz filtro
        ↓
StudentListScreen
        ↓
refresh_students()
        ↓
StudentRepository.list_students()
        ↓
SQLite
        ↓
lista filtrada/ordenada
        ↓
cards atualizados
```

## Perguntas prováveis

**Por que usar GROUP BY?**

Porque queremos separar os registros por curso para calcular uma quantidade para cada grupo.

**Qual a diferença entre WHERE e ORDER BY?**

`WHERE` decide quais registros entram no resultado. `ORDER BY` decide em qual ordem os registros aparecem.

**A pesquisa acontece no Python ou no banco?**

A condição de pesquisa é enviada ao SQLite. O banco executa o filtro e devolve os registros encontrados.

**É possível pesquisar e filtrar ao mesmo tempo?**

Sim. O Repository monta as condições necessárias e combina pesquisa e curso.

**Por que o dashboard não tem números fixos?**

Porque ele executa consultas ao banco toda vez que a Home é aberta.
