# ClassBase — Relatório acadêmico base

> Documento-base para o trabalho do 1º ano do Ensino Médio Técnico em Desenvolvimento de Sistemas — ETEC Cônego José Bento.
>
> Integrantes: Enzo Gonçalves Azevedo + 3 integrantes a preencher.
>
> Professor(a): a preencher.
>
> Jacareí — SP, 2026.

## Resumo

O ClassBase é um aplicativo mobile desenvolvido em Python com Kivy e SQLite para cadastro e gerenciamento básico de alunos. O sistema implementa autenticação local e as quatro operações de CRUD: criar, consultar, atualizar e excluir registros. Cada aluno possui RM, nome e curso, sendo o RM único no banco de dados. O aplicativo funciona de forma offline, armazena os dados localmente e pode ser empacotado como APK Android com Buildozer.

A proposta prioriza um escopo adequado a um projeto escolar: arquitetura compreensível, funcionamento demonstrável, baixo custo de infraestrutura e domínio do código pelo grupo. O projeto foi validado com testes automatizados e também em um aparelho Android real.

## 1. Introdução

Sistemas de cadastro são uma aplicação clássica de banco de dados porque exigem armazenamento, consulta, atualização, exclusão e validação de informações. O ClassBase foi desenvolvido para aplicar esses conceitos em um aplicativo mobile simples de gerenciamento de alunos.

O problema escolhido é organizar registros básicos de alunos em uma interface que possa ser utilizada diretamente em um dispositivo Android, sem depender de internet, servidor externo ou serviços pagos.

## 2. Objetivo geral

Desenvolver um aplicativo mobile em Python capaz de cadastrar, consultar, editar e excluir alunos, armazenando os dados de forma persistente em banco SQLite e disponibilizando uma interface adequada para Android.

## 3. Objetivos específicos

- Implementar autenticação local.
- Cadastrar alunos com RM, nome e curso.
- Garantir que o RM seja único.
- Listar os alunos cadastrados.
- Pesquisar por RM, nome ou curso.
- Editar registros existentes.
- Excluir registros mediante confirmação.
- Persistir os dados após fechar e reabrir o aplicativo.
- Gerar um APK Android instalável.
- Validar o sistema com testes automatizados e em aparelho real.

## 4. Requisitos funcionais

| ID | Requisito |
|---|---|
| RF01 | Permitir login local no aplicativo. |
| RF02 | Cadastrar aluno com RM, nome e curso. |
| RF03 | Impedir cadastro com campos obrigatórios vazios. |
| RF04 | Impedir RM duplicado. |
| RF05 | Exibir a quantidade de alunos cadastrados. |
| RF06 | Listar os alunos armazenados. |
| RF07 | Pesquisar alunos por RM, nome ou curso. |
| RF08 | Editar RM, nome e curso de um aluno. |
| RF09 | Excluir aluno após confirmação. |
| RF10 | Manter os dados salvos após reiniciar o aplicativo. |

## 5. Requisitos não funcionais

- Aplicação executável em Android.
- Funcionamento offline.
- Interface legível em tela de celular.
- Armazenamento local sem necessidade de servidor.
- Código dividido por responsabilidades.
- Senhas não armazenadas em texto puro.
- Consultas SQL parametrizadas.
- APK reproduzível a partir do projeto versionado.

## 6. Tecnologias utilizadas

### 6.1 Python

Python é a linguagem principal da aplicação. Foi escolhida por ser a linguagem utilizada no projeto e permitir implementar regras de negócio, validações, acesso ao SQLite e integração com a interface.

Alternativas possíveis seriam Java, Kotlin, JavaScript/TypeScript ou Dart. Entretanto, essas opções exigiriam introduzir outra linguagem como principal no projeto.

### 6.2 Kivy

Kivy é o framework utilizado para criar a interface gráfica. Ele permite construir aplicações multiplataforma utilizando Python e possui suporte para empacotamento Android.

Foi escolhido porque permite manter a maior parte do projeto em Python. Flutter e React Native também seriam opções modernas, mas utilizariam principalmente Dart ou JavaScript/TypeScript. O desenvolvimento Android nativo com Kotlin seria mais integrado à plataforma, porém fugiria do requisito de manter Python como linguagem central.

### 6.3 SQLite

SQLite é o banco de dados local utilizado pelo ClassBase. Ele funciona em um único arquivo, não exige servidor e é adequado para uma aplicação offline com poucos usuários simultâneos.

MySQL e PostgreSQL seriam mais indicados caso o sistema precisasse de servidor central, múltiplos dispositivos conectados ao mesmo banco ou sincronização online.

### 6.4 Buildozer

Buildozer é utilizado para automatizar o empacotamento do projeto Kivy em APK Android. O ambiente de build foi preparado no WSL2 com Ubuntu.

## 7. Arquitetura

A aplicação foi separada em três partes principais:

1. **Interface Kivy:** telas, botões, campos e navegação.
2. **Lógica Python:** validações e regras de fluxo.
3. **Persistência SQLite:** armazenamento de usuários e alunos.

Fluxo simplificado:

```text
Usuário
  ↓
Telas Kivy
  ↓
Classes Python das telas
  ↓
Repositories
  ↓
SQLite
```

A interface não executa SQL diretamente. As telas chamam os repositórios, que centralizam as operações de banco.

## 8. Banco de dados

### Tabela alunos

| Campo | Tipo | Regra |
|---|---|---|
| id | INTEGER | Chave primária e autoincremento |
| rm | TEXT | Obrigatório e único |
| nome | TEXT | Obrigatório |
| curso | TEXT | Obrigatório |

O RM é armazenado como texto porque funciona como identificador e não como número para operações matemáticas.

### Tabela usuarios

| Campo | Tipo | Regra |
|---|---|---|
| id | INTEGER | Chave primária |
| usuario | TEXT | Obrigatório e único |
| salt | BLOB | Salt aleatório |
| senha_hash | BLOB | Hash da senha |

## 9. CRUD

CRUD representa quatro operações fundamentais de sistemas com banco de dados:

- **Create:** cadastrar aluno — comando `INSERT`.
- **Read:** listar e pesquisar — comando `SELECT`.
- **Update:** editar aluno — comando `UPDATE`.
- **Delete:** excluir aluno — comando `DELETE`.

O ClassBase implementa as quatro operações.

## 10. Segurança e validações

O projeto inclui medidas compatíveis com o escopo escolar:

- senha armazenada com PBKDF2-HMAC-SHA256 e salt;
- 200.000 iterações de derivação da senha;
- comparação de hashes com `hmac.compare_digest`;
- consultas SQL parametrizadas;
- RM com restrição `UNIQUE` no SQLite;
- validação de campos obrigatórios;
- confirmação antes da exclusão;
- transações com commit e rollback;
- backup automático do banco desativado no Manifest Android.

O projeto não pretende substituir um sistema escolar real conectado à internet. Autenticação centralizada, controle de permissões avançado e backend remoto seriam melhorias de uma versão futura.

## 11. Interface

O aplicativo possui cinco telas principais:

1. Login.
2. Home.
3. Cadastro de aluno.
4. Lista/pesquisa de alunos.
5. Edição de aluno.

A interface foi adaptada após testes em celular real. Cadastro e edição utilizam conteúdo rolável para continuar utilizáveis com o teclado virtual aberto. Mensagens de sucesso e erro possuem diferenciação visual.

## 12. Testes e validação

A versão atual possui 29 testes automatizados cobrindo autenticação, CRUD, navegação, persistência, validações e comportamento da interface.

A versão Android também foi validada em aparelho real POCO C75 com Android 16. Entre os cenários testados fisicamente estão:

- instalação e atualização do APK;
- abertura e login;
- cadastro;
- contador da Home;
- listagem;
- pesquisa por RM, nome e curso;
- edição;
- proteção contra RM duplicado;
- cancelamento e confirmação de exclusão;
- persistência após reinício;
- persistência após atualização do APK;
- logout;
- comportamento com teclado virtual;
- feedback visual de sucesso.

## 13. Problemas encontrados e soluções

### Empacotamento Android

O primeiro build encontrou incompatibilidades no toolchain do python-for-android. A solução foi utilizar o branch `develop` do python-for-android, que continha a correção necessária para wheels Android nativos.

### Instalação no aparelho

A primeira tentativa via ADB foi bloqueada pelo verificador do Android/Google. O APK foi transferido ao dispositivo e instalado manualmente. Em atualizações posteriores, a instalação via ADB funcionou normalmente.

### Interface com teclado

Nos primeiros testes físicos, o teclado cobria os botões inferiores dos formulários. O problema foi resolvido combinando `Window.softinput_mode = "resize"` com formulários roláveis.

### Feedback de sucesso

A primeira versão utilizava a mesma cor para erro e sucesso. Após a QA física, mensagens de sucesso passaram a usar verde e erros continuam em vermelho.

## 14. Limitações atuais

- Banco exclusivamente local.
- Sem sincronização entre dispositivos.
- Um perfil simples de usuário.
- Sem recuperação de senha.
- Lista de cursos fixa no código.
- Sem painel web ou servidor.
- APK atual é um build de debug para apresentação/testes.

Essas limitações são compatíveis com o escopo definido para o trabalho.

## 15. Melhorias futuras

- API e banco central para sincronização.
- Perfis de usuário e permissões.
- Cadastro configurável de cursos.
- Exportação de dados.
- Backup controlado.
- Recuperação de senha.
- Versão release assinada para distribuição.
- Testes em diferentes modelos e tamanhos de tela.

## 16. Conclusão

O ClassBase atingiu os objetivos definidos para o MVP. O aplicativo possui CRUD completo, autenticação local, persistência SQLite, interface mobile, validações, testes automatizados e APK funcional em Android real.

A escolha de Python, Kivy e SQLite permitiu desenvolver uma solução sem infraestrutura paga e com complexidade adequada ao nível do projeto, mantendo separação clara entre interface, regras da aplicação e banco de dados.
