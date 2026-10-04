# ClassBase

Aplicativo mobile para gerenciamento de alunos desenvolvido em Python com Kivy e SQLite.

## Escopo

- Login local
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
- Banco SQLite implementado
- CRUD completo integrado à interface Kivy
- Pesquisa por RM, nome ou curso
- Contador de alunos na Home
- Login local com senha protegida por PBKDF2-HMAC + salt
- Logout limpa os campos e o feedback da tela de login
- Banco salvo no diretório gravável da aplicação
- Interface mobile revisada para telas pequenas
- Identidade Android própria com ícone e presplash
- Backup automático do banco desativado no Manifest Android
- 29 testes automatizados passando
- Build APK debug arm64-v8a: PASS (04/10/2026)
- Assinatura APK v2: PASS
- QA física crítica no POCO C75 / Android 16: PASS
- Cadastro e edição ajustados para uso com teclado virtual
- Feedback de sucesso validado em verde no aparelho real
- Persistência SQLite após reinício e atualização do APK: PASS

## Conta de demonstração

Enquanto o projeto está em desenvolvimento, a primeira execução cria:

- Usuário: `admin`
- Senha: `classbase123`

Essa credencial é apenas para desenvolvimento/apresentação e pode ser alterada antes da entrega final.

## Executar no Windows

```powershell
.\.venv\Scripts\python.exe main.py
```

## Executar os testes

```powershell
.\.venv\Scripts\python.exe -m unittest discover -v
```

O banco de produção é salvo no diretório de dados do usuário da aplicação, compatível com armazenamento gravável no Android.


## Documentação acadêmica e apresentação

- [Relatório acadêmico base](docs/RELATORIO_ACADEMICO.md)
- [Arquitetura](docs/ARQUITETURA.md)
- [Roteiro da apresentação](docs/APRESENTACAO.md)
- [Roteiro de demonstração](docs/ROTEIRO_DEMO.md)
- [Perguntas para defesa](docs/PERGUNTAS_DEFESA.md)
- [Plano de entrega](docs/PLANO_ENTREGA.md)
- [Build Android](docs/ANDROID_BUILD.md)
- [Checklist de QA física](docs/RELEASE_CHECKLIST.md)

A documentação acadêmica já está estruturada para a apresentação do grupo. Antes da entrega final, faltam apenas preencher os nomes dos outros integrantes e o nome do(a) professor(a).
