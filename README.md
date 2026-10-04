# ClassBase

Aplicativo mobile para gerenciamento de alunos desenvolvido em Python com Kivy e SQLite.

## Escopo

- Login
- Cadastro de alunos
- Listagem e pesquisa
- Edição
- Exclusão com confirmação
- RM único
- Persistência local com SQLite
- APK Android via Buildozer

## Ambiente

- Windows: Python 3.13 + Kivy 2.3.1
- WSL Ubuntu 24.04: Python 3.12 + Buildozer 1.6.0
- Java 17 para o toolchain Android

## Estado atual

- Ambiente Windows/WSL configurado
- Banco SQLite e repositório de alunos implementados
- Navegação Kivy com Login, Home, Cadastro, Alunos e Edição
- Cadastro integrado ao SQLite
- Pesquisa por RM, nome ou curso
- Edição integrada ao SQLite
- Exclusão integrada ao SQLite
- Contador de alunos na Home
- 19 testes automatizados passando
- Login real: pendente
- Build APK: pendente

## Executar no Windows

```powershell
.\.venv\Scripts\python.exe main.py
```

## Executar os testes

```powershell
.\.venv\Scripts\python.exe -m unittest discover -v
```

O banco de produção é salvo no diretório de dados do usuário da aplicação, o que também é compatível com o armazenamento gravável no Android.
