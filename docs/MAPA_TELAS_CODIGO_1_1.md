# ClassBase 1.1 — Mapa das telas e do código

## Regra geral

Cada tela possui duas partes:

```text
screens/nome.py → comportamento
kv/nome.kv      → aparência e organização
```

## 1. Login

```text
screens/login.py
kv/login.kv
```

### O usuário faz

Digita usuário e senha e toca Entrar.

### O código faz

`LoginScreen.login()`:

1. lê os campos via `self.ids`;
2. chama `AuthRepository.authenticate()`;
3. se verdadeiro, muda `manager.current` para `home`;
4. se falso, mostra mensagem.

## 2. Home

```text
screens/home.py
kv/home.kv
```

### O usuário vê

- total de alunos;
- distribuição por curso;
- atalhos para cadastro, consulta, cursos, histórico e sair.

### O código faz

`on_pre_enter()` atualiza os números antes de a tela aparecer.

A Home é rolável para não cortar ações em telas menores.

## 3. Cadastro

```text
screens/cadastro.py
kv/cadastro.kv
```

### O usuário faz

Informa RM, nome e escolhe um curso.

### O código faz

`refresh_courses()` carrega cursos ativos do banco.

`register_student()` chama o Repository e mostra resultado.

## 4. Alunos

```text
screens/alunos.py
kv/alunos.kv
```

### O usuário pode

- pesquisar;
- filtrar por curso;
- ordenar;
- abrir detalhes;
- editar;
- excluir.

### O código faz

`refresh_students()` consulta o Repository e recria os cards da lista.

## 5. Detalhes

```text
screens/detalhes.py
kv/detalhes.kv
```

### Mostra

- nome;
- RM;
- curso;
- criação;
- última atualização.

`load_student(id)` busca o registro correto no banco.

## 6. Editar

```text
screens/editar.py
kv/editar.kv
```

`load_student()` preenche os campos.

`save_student()` chama `update_student()`.

A tela também é rolável para continuar utilizável com teclado virtual.

## 7. Cursos

```text
screens/cursos.py
kv/cursos.kv
```

Permite cadastrar, editar, ativar, desativar e excluir quando permitido.

A tela usa `CourseRepository`.

O popup de edição possui altura fixa adequada para o redimensionamento causado pelo teclado.

## 8. Histórico

```text
screens/historico.py
kv/historico.kv
```

Mostra eventos mais recentes primeiro.

Filtro:

```text
Todos
Alunos
Cursos
```

A tela apenas consulta o histórico; quem grava eventos são os Repositories.

## Navegação principal

```text
Login
  ↓
Home
 ├── Cadastro
 ├── Alunos
 │    ├── Detalhes
 │    │    └── Editar
 │    └── Editar
 ├── Cursos
 └── Histórico
```

## Perguntas rápidas

**Quem troca as telas?**
`ScreenManager`.

**Quem acessa SQLite?**
Os Repositories.

**Quem define os botões/campos?**
Arquivos KV.

**Quem responde aos botões?**
Classes Python das telas.

**Quem cria os cards variáveis?**
Python, porque a quantidade depende dos registros do banco.
