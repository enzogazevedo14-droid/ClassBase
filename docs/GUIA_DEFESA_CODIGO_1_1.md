# ClassBase 1.1 — Guia de defesa do código

Este documento foi preparado a partir do código atual da branch `release/classbase-1.1-rc`.

## 1. O mapa mental que deve ser lembrado

```text
main.py
  ↓
cria os Repositories
  ↓
cria o ScreenManager
  ↓
adiciona as telas
  ↓
usuário interage com arquivos KV
  ↓
classes em screens/*.py tratam a ação
  ↓
Repositories em database/*.py acessam SQLite
  ↓
resultado volta para a tela
```

A ideia mais importante é:

> A interface não executa SQL diretamente. As telas chamam os Repositories, que aplicam regras e acessam o banco.

## 2. main.py

### Para que serve

É o ponto de entrada da aplicação.

A classe `ClassBaseApp` herda de `App`, do Kivy.

No método `build()`:

1. define o título;
2. configura o comportamento do teclado com `Window.softinput_mode = "resize"`;
3. carrega os arquivos KV;
4. escolhe o caminho do SQLite;
5. cria `StudentRepository`, `CourseRepository`, `HistoryRepository` e `AuthRepository`;
6. garante o usuário inicial;
7. cria o `ClassBaseScreenManager`;
8. adiciona as telas;
9. devolve o manager como raiz do app.

### Se o professor perguntar “onde o app começa?”

Resposta:

> O ponto de entrada é o `main.py`. O Kivy executa `ClassBaseApp().run()`, e o método `build()` monta os repositórios e as telas.

## 3. ClassBaseScreenManager

Arquivo:

```text
screens/manager.py
```

Ele herda de `ScreenManager`.

Guarda referências compartilhadas para:

- repositório de alunos;
- autenticação;
- cursos;
- histórico.

Isso permite que as telas usem:

```python
self.manager.repository
self.manager.course_repository
self.manager.history_repository
self.manager.auth_repository
```

### Por que usar ScreenManager?

> Porque o aplicativo possui várias telas e o ScreenManager centraliza qual tela está ativa e a navegação entre elas.

## 4. Login

Arquivos:

```text
screens/login.py
kv/login.kv
```

Método principal:

```python
login()
```

Fluxo:

```text
usuário e senha digitados
        ↓
self.ids
        ↓
AuthRepository.authenticate()
        ↓
consulta usuário no SQLite
        ↓
PBKDF2 da senha informada
        ↓
hmac.compare_digest
        ↓
Home ou mensagem de erro
```

### self.ids

Quando aparece algo como:

```python
self.ids.username_input.text
```

significa:

> Pegar o componente da interface cujo `id` é `username_input` e ler seu texto.

## 5. Home

Arquivos:

```text
screens/home.py
kv/home.kv
```

Método importante:

```python
on_pre_enter()
```

O Kivy chama esse método antes de a tela aparecer.

Ele atualiza:

- total de alunos;
- distribuição por curso.

O total vem de:

```python
repository.count_students()
```

A distribuição vem de:

```python
course_repository.list_student_counts()
```

Essa segunda consulta utiliza `COUNT`, `GROUP BY` e `LEFT JOIN`.

A Home foi colocada dentro de `ScrollView` para continuar utilizável em telas menores.

## 6. Cadastro de aluno

Arquivos:

```text
screens/cadastro.py
kv/cadastro.kv
```

Métodos:

- `on_pre_enter()`;
- `refresh_courses()`;
- `register_student()`.

### refresh_courses()

Busca no banco os cursos ativos e atualiza o `Spinner`.

Isso significa que os cursos não ficam mais presos a uma lista escrita na tela.

### register_student()

1. lê RM, nome e curso;
2. transforma “Selecione o curso” em valor vazio para validação;
3. chama `StudentRepository.create_student()`;
4. trata `ValueError`;
5. mostra sucesso em verde ou erro;
6. limpa os campos se o cadastro funcionou.

## 7. Lista de alunos

Arquivos:

```text
screens/alunos.py
kv/alunos.kv
```

Métodos principais:

- `refresh_filters()`;
- `refresh_students()`;
- `open_detail()`;
- `open_edit()`;
- `request_delete()`;
- `delete_student()`.

### refresh_students()

Lê:

- texto da busca;
- curso selecionado;
- ordenação.

Depois chama:

```python
repository.list_students(
    search=...,
    course=...,
    order_by=...
)
```

Os cards são criados dinamicamente em Python para cada resultado retornado pelo SQLite.

### Por que os cards não estão todos escritos no KV?

> Porque a quantidade de alunos varia. O Python recebe os registros e cria um card para cada aluno encontrado.

## 8. Tela de detalhes

Arquivos:

```text
screens/detalhes.py
kv/detalhes.kv
```

Métodos:

- `_format_timestamp()`;
- `load_student()`;
- `on_pre_enter()`;
- `edit_student()`.

`load_student(student_id)` chama:

```python
repository.get_student(student_id)
```

e preenche:

- nome;
- RM;
- curso;
- data de cadastro;
- última atualização.

A tela usa o ID do aluno porque nomes e outros campos podem se repetir, enquanto a chave primária identifica exatamente um registro.

## 9. Edição

Arquivos:

```text
screens/editar.py
kv/editar.kv
```

### load_student()

Carrega o registro e preenche os campos antes de mostrar a tela.

### save_student()

Envia os valores ao:

```python
StudentRepository.update_student()
```

Se os dados forem idênticos aos já armazenados, a operação retorna sucesso sem alterar `updated_at` e sem criar evento de histórico.

Se alguma informação mudar, `updated_at` recebe um novo horário e o histórico registra apenas as diferenças.

## 10. Gerenciamento de cursos

Arquivos:

```text
screens/cursos.py
kv/cursos.kv
database/courses.py
```

A tela permite:

- cadastrar;
- editar;
- ativar;
- desativar;
- excluir cursos sem alunos vinculados.

### Ativar/desativar é diferente de excluir

Curso inativo:

- continua no banco;
- continua ligado a alunos antigos;
- não aparece para novos cadastros.

Curso excluído:

- deixa de existir;
- só pode ser excluído se nenhum aluno estiver vinculado.

## 11. Histórico

Arquivos:

```text
screens/historico.py
kv/historico.kv
database/history.py
```

Registra operações de alunos e cursos.

Exemplo:

```text
Aluno · Atualizado
RM: 100 → 101; Curso: Administração → Desenvolvimento de Sistemas
```

A gravação do histórico acontece dentro da mesma transação da operação principal.

### Por que isso importa?

Se a auditoria falhar, a operação principal também sofre rollback.

Assim não existe:

- aluno alterado sem histórico correspondente;
- histórico dizendo que houve alteração quando ela falhou.

## 12. database/connection.py

Responsabilidades:

- criar conexão SQLite;
- ativar foreign keys;
- executar commit;
- executar rollback;
- fechar a conexão;
- criar tabelas;
- executar migrações;
- controlar `PRAGMA user_version`.

### connect()

É um context manager.

Fluxo:

```text
abre conexão
    ↓
yield
    ↓
deu certo?
sim → commit
não → rollback
    ↓
fecha conexão
```

## 13. StudentRepository

Arquivo:

```text
database/repository.py
```

Métodos:

- `create_student()`;
- `get_student()`;
- `list_students()`;
- `update_student()`;
- `delete_student()`;
- `count_students()`.

Representa o CRUD principal do trabalho.

```text
Create → create_student
Read   → get_student / list_students
Update → update_student
Delete → delete_student
```

## 14. CourseRepository

Arquivo:

```text
database/courses.py
```

Métodos importantes:

- `create_course()`;
- `list_courses()`;
- `update_course()`;
- `set_course_active()`;
- `delete_course()`;
- `list_student_counts()`.

`list_student_counts()` é a parte usada pelo dashboard.

## 15. AuthRepository

Arquivo:

```text
database/auth.py
```

A senha não é gravada em texto puro.

Fluxo:

```text
senha
 + salt aleatório
      ↓
PBKDF2-HMAC-SHA256
      ↓
hash salvo
```

No login, o hash da senha digitada é calculado novamente e comparado usando `hmac.compare_digest`.

## 16. SQL parametrizado

Exemplo:

```python
connection.execute(
    "SELECT ... WHERE id = ?",
    (student_id,),
)
```

O `?` representa um valor enviado separadamente do texto SQL.

Resposta para o professor:

> Isso evita concatenar diretamente entradas do usuário na consulta e reduz problemas como SQL injection.

A pesquisa foi testada inclusive com uma string parecida com tentativa de SQL injection sem alterar o banco.

## 17. Chave primária e chave estrangeira

### cursos.id

É a chave primária do curso.

### alunos.curso_id

É uma chave estrangeira que aponta para `cursos.id`.

Relacionamento:

```text
CURSO 1 -------- N ALUNOS
```

Um curso pode possuir vários alunos, e cada aluno aponta para um curso.

## 18. JOIN

Como `alunos` guarda `curso_id`, usamos JOIN para recuperar o nome:

```sql
FROM alunos AS a
JOIN cursos AS c ON c.id = a.curso_id
```

Resposta:

> O JOIN combina os dados relacionados das duas tabelas.

## 19. COUNT, GROUP BY e LEFT JOIN

O dashboard precisa saber quantos alunos existem em cada curso.

`COUNT` conta.

`GROUP BY` separa os registros por curso.

`LEFT JOIN` permite que um curso exista no resultado mesmo com zero alunos.

## 20. created_at e updated_at

`created_at` registra quando o aluno foi criado.

`updated_at` registra a última alteração real.

Os horários são gravados em UTC e convertidos para o horário local quando exibidos.

## 21. Migração do banco

O schema atual utiliza:

```text
PRAGMA user_version = 4
```

A inicialização detecta bancos antigos.

O projeto possui testes que simulam um banco da versão 1.0 com 120 alunos e verificam que todos continuam existentes depois da migração.

## 22. Como responder quando o professor apontar uma linha

Use esta estrutura:

1. diga **onde está**;
2. diga **qual informação entra**;
3. diga **qual função é chamada**;
4. diga **o que acontece no banco ou na interface**;
5. diga **por que foi feito assim**.

Exemplo:

```python
self.manager.repository.create_student(rm, nome, curso)
```

Resposta:

> Essa linha está na tela de cadastro. Ela envia os três valores para o StudentRepository. O Repository valida os dados, encontra o ID do curso e executa o INSERT parametrizado no SQLite. Fizemos assim para separar a interface do acesso ao banco.

## 23. Conceitos que não podem confundir

```text
Python      = linguagem
Kivy        = framework de interface
KV          = definição visual do Kivy
SQLite      = banco de dados
Repository  = camada que acessa o banco
Screen      = uma tela do aplicativo
ScreenManager = navegação
Buildozer   = empacotamento Android
Git         = versionamento local
GitHub      = repositório remoto
WSL/Ubuntu  = ambiente Linux usado no build
```

## 24. Estado dos testes antes da QA física

O RC2 possui:

```text
83/83 testes automatizados PASS
```

Isso não substitui a QA física. O APK ainda precisa ser validado no aparelho real antes de promover a 1.1.
