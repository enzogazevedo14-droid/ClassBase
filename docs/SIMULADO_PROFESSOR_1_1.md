# ClassBase 1.1 — Simulado de perguntas do professor

Use este arquivo para treinar sem decorar frases exatamente iguais.

## Nível 1 — ferramentas

### 1. Por que Python?

Porque é a linguagem principal do projeto e concentra lógica, validações, acesso ao SQLite e integração com Kivy.

### 2. Por que Kivy?

Porque permite construir a interface utilizando Python e possui um caminho de empacotamento para Android.

### 3. Por que não Tkinter?

Tkinter seria adequado principalmente para desktop. Como o objetivo incluía APK Android, Kivy se encaixou melhor.

### 4. Por que SQLite?

Porque o app é local, offline e não precisa de servidor central.

### 5. Por que não MySQL?

MySQL faria mais sentido se vários dispositivos precisassem compartilhar um banco central através de backend/API.

### 6. Por que não Firebase?

Firebase adicionaria nuvem, internet e serviço externo sem necessidade para o escopo atual. SQLite também permite demonstrar SQL relacional diretamente.

### 7. Para que serve Buildozer?

Automatiza o empacotamento da aplicação Python/Kivy para Android utilizando python-for-android e o toolchain Android.

### 8. Para que servem Git e GitHub?

Git controla versões e histórico local. GitHub mantém o repositório remoto e facilita branches, commits, tags e compartilhamento.

## Nível 2 — telas

### 9. O que acontece quando aperto Entrar?

A tela lê usuário/senha, chama `AuthRepository.authenticate()` e, se o retorno for verdadeiro, o ScreenManager muda para a Home.

### 10. Por que a Home atualiza em on_pre_enter?

Porque precisamos recalcular os dados toda vez antes de mostrar a tela, evitando contador desatualizado.

### 11. Como o cadastro sabe quais cursos existem?

`RegisterStudentScreen.refresh_courses()` consulta `CourseRepository.list_courses()` e coloca os nomes no Spinner.

### 12. Como a lista cria um card para cada aluno?

`refresh_students()` recebe uma lista de dicionários do Repository e cria widgets Kivy dinamicamente em um loop.

### 13. Por que existe uma tela de detalhes?

Para separar consulta completa de edição e mostrar também timestamps sem sobrecarregar o card da lista.

### 14. O que acontece ao editar?

A tela carrega o aluno pelo ID, preenche os campos e envia as alterações para `StudentRepository.update_student()`.

### 15. Por que existe confirmação antes de excluir?

Porque exclusão é destrutiva e a confirmação reduz exclusões acidentais.

## Nível 3 — banco

### 16. O que é chave primária?

É um campo que identifica unicamente um registro. No projeto usamos `id` como chave primária.

### 17. O que é chave estrangeira?

É um campo que referencia a chave primária de outra tabela. `alunos.curso_id` aponta para `cursos.id`.

### 18. Qual é o relacionamento entre curso e aluno?

1:N. Um curso pode possuir vários alunos; cada aluno referencia um curso.

### 19. O que é JOIN?

É uma operação que combina dados relacionados de tabelas diferentes. Usamos JOIN para obter o nome do curso a partir de `curso_id`.

### 20. Por que RM também é UNIQUE se já existe id?

Porque `id` identifica internamente o registro, enquanto RM é uma regra de negócio: dois alunos não devem ter o mesmo RM.

### 21. O que é COUNT?

Uma função SQL que conta registros.

### 22. O que é GROUP BY?

Agrupa registros por um valor em comum. No dashboard agrupamos por curso para contar alunos.

### 23. Por que LEFT JOIN no dashboard?

Para permitir que um curso exista no resultado mesmo quando ainda não possui alunos.

### 24. O que é ORDER BY?

Define a ordem dos registros retornados.

## Nível 4 — segurança e consistência

### 25. Por que usamos ? nas consultas?

São placeholders de consultas parametrizadas. Os valores são enviados separadamente do SQL, evitando concatenação direta.

### 26. Como a senha é armazenada?

Com salt aleatório e PBKDF2-HMAC-SHA256. Não armazenamos a senha em texto puro.

### 27. O que é commit?

Confirma as alterações de uma transação no banco.

### 28. O que é rollback?

Desfaz a transação quando ocorre erro.

### 29. Por que histórico e alteração principal estão na mesma transação?

Para garantir que os dois sejam confirmados juntos ou desfeitos juntos.

### 30. O que acontece se a gravação do histórico falhar?

A transação sofre rollback. Os testes confirmam que cadastro/edição/exclusão também são desfeitos.

## Nível 5 — decisões da 1.1

### 31. Por que curso virou tabela?

Para evitar texto repetido, permitir CRUD próprio e criar relacionamento relacional entre curso e aluno.

### 32. Por que desativar curso em vez de sempre excluir?

Porque alunos antigos podem continuar vinculados ao curso, preservando histórico, enquanto novos alunos deixam de poder escolhê-lo.

### 33. Por que não podemos excluir curso com aluno?

A chave estrangeira usa `ON DELETE RESTRICT`, protegendo a integridade referencial.

### 34. Por que created_at e updated_at?

Para registrar quando o aluno foi criado e quando sofreu a última alteração real.

### 35. O que acontece se apertar Salvar sem mudar nada?

A operação retorna sucesso, mas não muda `updated_at` e não cria evento artificial no histórico.

### 36. Por que o histórico continua depois de excluir o aluno?

Porque ele registra fatos passados. `registro_id` não é uma foreign key obrigatória justamente para permitir preservar o evento de exclusão.

### 37. Para que serve PRAGMA user_version?

É usado para identificar a versão do schema do SQLite e organizar evolução/migrações.

### 38. Como vocês sabem que a migração não perde dados?

Existem testes que constroem bancos antigos, inclusive com 120 alunos, executam a migração e comparam os dados e a integridade final.

## Nível 6 — perguntas de pressão

### 39. Flutter não seria melhor que Kivy?

Flutter pode ser melhor em alguns projetos mobile e possui ecossistema forte, mas utiliza Dart. Para este trabalho, manter Python como linguagem principal era um requisito importante.

### 40. PostgreSQL não é melhor que SQLite?

Não existe “melhor” sem contexto. PostgreSQL é mais adequado a sistemas cliente-servidor; SQLite atende melhor um aplicativo local/offline sem servidor.

### 41. Por que não colocar tudo em main.py?

Porque separar telas e acesso ao banco reduz acoplamento, facilita teste, manutenção e explicação de responsabilidades.

### 42. Por que a tela não executa INSERT diretamente?

Porque usamos uma camada Repository para separar interface de persistência e centralizar regras do banco.

### 43. E se alguém digitar SQL no campo de pesquisa?

O valor é tratado como parâmetro, não como código SQL. Existe teste automatizado com entrada semelhante a SQL injection e a tabela permanece intacta.

### 44. Como sabem que as chaves estrangeiras não ficaram quebradas?

Os testes executam `PRAGMA foreign_key_check` e esperam resultado vazio.

### 45. Como sabem que o arquivo SQLite não ficou corrompido?

A suíte também executa `PRAGMA integrity_check` e o resultado atual é `ok`.

## Treino recomendado

Primeiro responda cada pergunta em 20–40 segundos sem olhar a resposta.

Depois peça para outro integrante apontar um arquivo ou método aleatório.

A resposta deve explicar:

```text
entrada → método → Repository → banco → resultado
```

Se conseguir explicar esse caminho, você não depende de decorar linhas isoladas.
