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

## Resultado validado

O build de debug gera `bin/classbase-0.1.0-arm64-v8a-debug.apk`.

Último APK validado da revisão atual:

- Commit funcional: `219466c`
- 26/26 testes automatizados: PASS
- Build Android: PASS
- Assinatura debug: APK Signature Scheme v2 válida
- Tamanho do APK final validado: 23.273.754 bytes
- SHA-256: `83F026EAE2B5E1EEA8CBD8D06DC2A1DAD167F94B399C7203C1A0D8436825F401`
- Cópia para teste: `C:\Users\User\Downloads\ClassBase-0.1.0-debug.apk`

Os builds incrementais passaram a reutilizar o cache do toolchain, reduzindo o tempo de empacotamento após a compilação inicial.

## Pendência de gate

O APK ainda precisa de QA em aparelho Android real: instalação, abertura, login, CRUD completo, persistência após reiniciar o aplicativo, teclado/botão voltar e logout.

O APK é artefato de build e não deve ser versionado no Git.
