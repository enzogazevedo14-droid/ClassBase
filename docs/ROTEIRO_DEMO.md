# Roteiro de demonstração — ClassBase

## Preparação antes da apresentação

1. Confirmar bateria suficiente no celular.
2. Deixar o APK instalado.
3. Abrir o app uma vez antes da apresentação.
4. Garantir que não existam dados pessoais reais.
5. Criar somente dados fictícios durante a demo.
6. Ter o notebook com a versão desktop como plano B.

## Dados sugeridos para a demo

- RM: `2026001`
- Nome: `Ana Souza`
- Curso: `Desenvolvimento de Sistemas`

Segundo registro opcional:

- RM: `2026002`
- Nome: `Bruno Lima`
- Curso: `Administração`

## Sequência ideal

### 1. Login

Entrar com a conta de demonstração.

Explicar:

> A autenticação é local. A senha não é armazenada diretamente no banco; armazenamos salt e hash.

### 2. Home

Mostrar contador de alunos.

Explicar:

> O contador vem do SQLite, não é um número fixo na interface.

### 3. Cadastro

Cadastrar `Ana Souza`.

Apontar:
- RM obrigatório;
- nome obrigatório;
- curso selecionável;
- mensagem de sucesso verde.

### 4. RM duplicado

Opcionalmente tentar cadastrar o mesmo RM.

Explicar:

> A aplicação valida e o próprio banco também possui a restrição UNIQUE.

Não gastar muito tempo nessa etapa se a apresentação for curta.

### 5. Consulta

Abrir a lista.

Mostrar:
- nome;
- RM;
- curso;
- Editar;
- Excluir.

### 6. Pesquisa

Pesquisar `Ana` ou `2026001`.

Explicar:

> A mesma pesquisa procura nos campos RM, nome e curso.

### 7. Edição

Alterar o nome para `Ana Souza Silva` e salvar.

### 8. Exclusão

Abrir a confirmação, primeiro mencionar que existe a opção Cancelar, depois excluir o registro.

### 9. Persistência

Explicar:

> O banco é um arquivo SQLite salvo no diretório da aplicação. Nos testes, os registros permaneceram após encerrar o processo e abrir novamente, além de permanecerem após atualização do APK.

Se houver tempo, fechar e abrir o app para demonstrar.

## Plano B

Se o celular tiver qualquer problema:
- executar o ClassBase no Windows;
- mostrar capturas/telas;
- continuar a explicação normalmente.

O grupo não deve depender exclusivamente da demonstração ao vivo para provar o funcionamento.

## O que não fazer

- não usar dados reais de colegas;
- não alterar código no momento da apresentação;
- não instalar APK na hora;
- não tentar demonstrar funções não testadas;
- não dizer que é um sistema pronto para produção;
- não esconder limitações: explicar o escopo.
