# Build Android do ClassBase

Configuração validada em 04/10/2026.

## Ambiente validado

- WSL2 com Ubuntu 24.04
- Python 3.12
- Java 17
- Buildozer 1.6.0
- Cython 0.29.34
- Android API 33
- Android mínimo API 24
- Arquitetura arm64-v8a
- python-for-android: branch develop

## Preparar o ambiente

Instale as dependências de sistema do Buildozer para Ubuntu 24.04 e Java 17.

Crie o ambiente de build com acesso aos pacotes de usuário:

```bash
python3 -m venv --system-site-packages .venv-build
source .venv-build/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install buildozer==1.6.0 Cython==0.29.34
```

Essa configuração é necessária no ambiente atualmente validado para compatibilidade com a preparação do python-for-android.

## Gerar APK

Na raiz do projeto:

```bash
buildozer -v android debug
```

O `buildozer.spec` usa `p4a.branch = develop` no toolchain validado.

## Resultados validados

### Baseline Android inicial

- Arquivo: `bin/classbase-0.1.0-arm64-v8a-debug.apk`
- Tamanho: 23.272.018 bytes
- Assinatura: APK Signature Scheme v2
- SHA-256: `6DC49552F5C641E08B0EAD358C9738F0E37BCF86C2D84E3FB4838CA4B4122AE0`

### RC funcional anterior (pré-branding)

- Commit do código: `219466c`
- Testes automatizados: 26/26 PASS
- Build Android: PASS
- Arquivo preservado no projeto: `dist/ClassBase-0.1.0-rc-debug.apk`
- Tamanho: 23.273.754 bytes
- Assinatura: APK Signature Scheme v2 válida
- SHA-256: `83F026EAE2B5E1EEA8CBD8D06DC2A1DAD167F94B399C7203C1A0D8436825F401`

### Release Candidate atual (branding)

- Commit do código: `54fb223`
- Tag: `android-branded-rc-0.1.0`
- Testes automatizados: 26/26 PASS
- Build Android: PASS
- Ícone próprio e presplash empacotados no APK
- `android.allowBackup=false` confirmado no Manifest compilado
- Arquivo preservado no projeto: `dist/ClassBase-0.1.0-branded-rc-debug.apk`
- Cópia para teste: `C:\\Users\\User\\Downloads\\ClassBase-0.1.0-debug.apk`
- Tamanho: 23.310.470 bytes
- Assinatura: APK Signature Scheme v2 válida
- SHA-256: `525FE263ED42F4E23AB6D1887A9B1B6FD279EB23DD9FE6708426A1F94FEBC9DB`

Os builds incrementais reutilizam o cache do toolchain; o Gradle do RC branded concluiu com `BUILD SUCCESSFUL` em cerca de 10 segundos.

## RC com QA física — atual

- Commit do código: `ee5216b`
- Tag: `android-qa-pass-0.1.0`
- Testes automatizados: 29/29 PASS
- Build Android: PASS
- Dispositivo: POCO C75 / modelo `2410FPCC5G`
- Android: 16
- ABI: arm64-v8a
- Arquivo preservado no projeto: `dist/ClassBase-0.1.0-qa-pass-debug.apk`
- Cópia usada na instalação: `C:\\Users\\User\\Downloads\\ClassBase-0.1.0-scrollfix-debug.apk`
- Tamanho: 23.310.834 bytes
- Assinatura: APK Signature Scheme v2 válida
- SHA-256: `6F412FD90FC1C29E1EE3E71EB3633676C5EDBE83C514593D8D8E84E0E43BBB45`

### QA física confirmada

- instalação e atualização do APK;
- abertura, presplash e tela de login;
- login válido e logout limpando os campos;
- cadastro, listagem, contador e pesquisa por RM/nome/curso;
- bloqueio de RM duplicado no cadastro e na edição;
- edição com salvamento enquanto o teclado está aberto;
- cancelamento e confirmação de exclusão;
- persistência SQLite após fechar/reabrir o app;
- persistência após atualização do APK;
- cartões mobile sem corte;
- formulários roláveis e botões acessíveis com teclado virtual;
- mensagem de cadastro concluído exibida em verde.

Os registros criados apenas para QA foram removidos ao final, deixando a tabela `alunos` vazia.

### Cobertura restante

Alguns casos de borda continuam cobertos por testes automatizados, mas não foram repetidos manualmente no aparelho nesta rodada, como login inválido, todos os campos obrigatórios vazios em sequência e stress de lista longa. Para a demonstração escolar, o gate crítico Android está aprovado.

Os APKs são artefatos de build e não devem ser versionados no Git.
