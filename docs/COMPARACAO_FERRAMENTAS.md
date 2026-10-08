# ClassBase — Comparação das ferramentas e justificativas

A resposta-base para qualquer comparação é:

> Não escolhemos uma ferramenta por ela ser melhor em todos os cenários. Escolhemos a opção mais adequada aos requisitos, ao escopo e às tecnologias previstas para o ClassBase.

## Python x Kotlin

### Por que Python?

- era a linguagem central prevista para o trabalho;
- permite lógica, validação e SQLite;
- integra diretamente com Kivy.

### Quando Kotlin seria melhor?

Para um aplicativo Android nativo maior, com integração profunda aos recursos do Android.

### Resposta curta

> Kotlin é uma opção muito forte para Android nativo, mas nosso projeto tinha Python como linguagem principal. Kivy permitiu manter Python também na interface.

## Python x Java

Java poderia atender o projeto, principalmente em Android ou desktop.

Não usamos porque introduziria outra linguagem sem necessidade para cumprir o escopo.

## Python x JavaScript/TypeScript

JavaScript/TypeScript poderia ser usado com React Native ou aplicações web.

Não era necessário adicionar outro ecossistema, pois Python + Kivy já atendia o requisito mobile.

## Kivy x Tkinter

### Tkinter

- simples;
- acompanha Python em muitos ambientes;
- muito usado em interfaces desktop.

### Kivy

- multiplataforma;
- melhor direcionado a interfaces touch/mobile;
- possui fluxo conhecido de empacotamento Android.

### Resposta

> Tkinter seria adequado para uma aplicação desktop simples. Como queríamos APK Android, Kivy era mais compatível com o objetivo.

## Kivy x Flutter

Flutter possui excelente ecossistema mobile e usa Dart.

Em um projeto comercial mobile poderia ser uma escolha muito forte.

No ClassBase, Kivy teve a vantagem de manter Python como linguagem principal.

## Kivy x React Native

React Native usa principalmente JavaScript/TypeScript.

Poderia produzir Android/iOS, mas adicionaria outra linguagem e ferramentas que não eram necessárias para o trabalho.

## Kivy x Android nativo

Android Studio + Kotlin oferece integração nativa mais direta.

Nossa escolha privilegia o requisito de Python.

Não é correto dizer que Kivy é “melhor”; ele é mais adequado ao conjunto de requisitos deste trabalho.

## SQLite x MySQL

### SQLite

- fica no próprio dispositivo;
- não exige servidor;
- funciona offline;
- adequado ao volume e ao escopo do projeto.

### MySQL

- normalmente usado com servidor;
- melhor para vários clientes compartilhando os mesmos dados;
- exigiria backend/API para um app mobile bem arquitetado.

### Resposta

> Se vários celulares precisassem compartilhar uma base central, MySQL seria uma opção mais adequada. Como o ClassBase é local e offline, SQLite resolve o problema com menos infraestrutura.

## SQLite x PostgreSQL

A lógica é semelhante ao MySQL.

PostgreSQL é excelente para sistemas cliente-servidor, regras avançadas e múltiplos usuários simultâneos.

O ClassBase não precisava de servidor central.

## SQLite x Firebase

Firebase facilitaria recursos de nuvem e sincronização.

Não utilizamos porque:

- internet não era requisito;
- adicionaríamos dependência de serviço externo;
- o trabalho precisava demonstrar banco e CRUD de forma clara;
- SQLite permite trabalhar diretamente com SQL relacional.

## SQLite x JSON/TXT

JSON é um formato de arquivo, não substitui todos os recursos de um banco relacional.

Com SQLite usamos:

- UNIQUE;
- chave estrangeira;
- JOIN;
- transações;
- GROUP BY;
- ORDER BY;
- integridade referencial.

## Buildozer x Android Studio

Eles não têm exatamente a mesma função no nosso fluxo.

Android Studio é uma IDE e conjunto de ferramentas para desenvolvimento Android, principalmente Java/Kotlin.

Buildozer automatiza o empacotamento de aplicações Python/Kivy usando o python-for-android e ferramentas do Android.

## Buildozer x PyInstaller

PyInstaller é muito usado para empacotar Python para desktop.

Para nosso APK Android, Buildozer + python-for-android era o fluxo apropriado.

## Git x cópias de pasta

Sem Git seria comum surgir:

```text
ClassBase-final
ClassBase-final2
ClassBase-final-agora
```

Git registra alterações por commit, permite branches e recuperação de versões.

## GitHub x Google Drive

Google Drive armazena arquivos.

GitHub é voltado a repositórios Git e mostra:

- commits;
- branches;
- diferenças;
- histórico;
- tags/releases.

Drive pode complementar, mas não substitui o versionamento de código.

## GitHub x GitLab

Os dois poderiam atender.

Escolhemos GitHub porque atendia nosso fluxo e já era o serviço utilizado pelo grupo.

Não existe necessidade de afirmar que GitHub é tecnicamente superior para este projeto.

## WSL x máquina virtual

### WSL

- executa Linux integrado ao Windows;
- menor atrito com arquivos/ferramentas;
- suficiente para o Buildozer.

### Máquina virtual

Também poderia funcionar, mas adicionaria um sistema virtual completo e maior consumo de recursos.

## WSL x Linux instalado diretamente

Linux nativo também seria válido.

WSL permitiu manter o ambiente principal Windows e ainda executar o toolchain Linux necessário.

## Por que não usar nuvem/backend?

Porque a versão escolar precisava demonstrar:

- aplicativo mobile;
- Python;
- Kivy;
- banco;
- CRUD.

Um backend acrescentaria:

- servidor;
- API;
- autenticação remota;
- deploy;
- sincronização.

Isso aumentaria muito o escopo antes de existir um requisito real para compartilhamento entre dispositivos.

## Modelo de resposta para o professor

Quando ele perguntar “por que não usaram X?”, responda:

1. **X também seria possível.**
2. **Diga em que cenário X teria vantagem.**
3. **Explique o requisito do ClassBase.**
4. **Mostre por que nossa escolha atende melhor esse cenário.**

Exemplo:

> PostgreSQL também seria uma ótima opção para um sistema com vários dispositivos e banco central. No ClassBase os dados são locais e offline, então SQLite elimina a necessidade de servidor e ainda permite demonstrar SQL, CRUD e relacionamento entre tabelas.
