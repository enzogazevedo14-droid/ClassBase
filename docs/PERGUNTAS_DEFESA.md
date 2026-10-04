# Perguntas para defesa do projeto

## 1. O que é CRUD?

CRUD é o conjunto de quatro operações básicas de gerenciamento de dados:

- Create: criar;
- Read: consultar;
- Update: atualizar;
- Delete: excluir.

No ClassBase essas operações correspondem a cadastrar, listar/pesquisar, editar e excluir alunos.

## 2. Por que SQLite?

Porque o projeto é local e offline. SQLite não exige servidor, é gratuito e funciona bem para um aplicativo pequeno armazenando dados no próprio aparelho.

## 3. Por que não MySQL?

MySQL seria útil em um sistema cliente-servidor, principalmente com vários dispositivos acessando o mesmo banco. Para o escopo atual, exigiria infraestrutura adicional sem trazer benefício necessário.

## 4. Por que Kivy?

Porque permite desenvolver a interface utilizando Python e gerar uma aplicação Android, mantendo a tecnologia principal do projeto.

## 5. Por que o RM é TEXT?

Porque RM é um identificador. Não fazemos contas matemáticas com ele, então tratá-lo como texto é adequado e evita associar o tipo do campo ao significado de um número calculável.

## 6. Como o RM duplicado é impedido?

Existem duas camadas:
- a aplicação trata o erro e mostra mensagem ao usuário;
- o SQLite possui `UNIQUE` na coluna RM.

## 7. Onde os dados ficam?

Em um arquivo SQLite chamado `classbase.db`, salvo no diretório de dados gravável da aplicação.

## 8. Os dados somem quando fecha o app?

Não. Eles permanecem no arquivo SQLite. Isso foi validado encerrando e reabrindo o processo do aplicativo.

## 9. A senha fica salva em texto?

Não. O banco guarda um salt aleatório e o resultado de PBKDF2-HMAC-SHA256.

## 10. O app precisa de internet?

Não na versão atual. O funcionamento offline foi uma decisão de escopo.

## 11. Como a interface acessa o banco?

As telas chamam classes Repository. O Repository executa as consultas no SQLite. Isso separa a interface da persistência.

## 12. O que são consultas parametrizadas?

São consultas SQL em que os valores são enviados separadamente da instrução, usando placeholders. No projeto usamos `?`.

## 13. O que acontece se der erro durante uma operação no banco?

O gerenciador de conexão executa rollback e depois propaga a exceção. Se tudo der certo, executa commit.

## 14. Como foi gerado o APK?

Com Buildozer no Ubuntu via WSL2. O Buildozer usa o python-for-android para compilar e empacotar o aplicativo.

## 15. O projeto foi testado em celular?

Sim. A QA crítica foi executada em um POCO C75 com Android 16, incluindo CRUD, persistência e comportamento com teclado virtual.

## 16. Qual problema real apareceu somente no celular?

O teclado virtual cobria os botões dos formulários. A correção final utilizou modo resize e formulários roláveis.

## 17. Quantos testes automatizados existem?

29 testes na versão atual.

## 18. Qual é a principal limitação?

O banco é local. Dois celulares não compartilham automaticamente os mesmos alunos.

## 19. Como transformar em um sistema multiusuário?

Criando uma API/backend e utilizando um banco central, por exemplo PostgreSQL ou MySQL, com autenticação e sincronização.

## 20. O projeto está pronto para produção?

Não é esse o objetivo. Está validado como MVP escolar e aplicação de demonstração. Uma versão de produção exigiria backend, gestão de usuários, políticas de segurança, backups e testes em mais dispositivos.
