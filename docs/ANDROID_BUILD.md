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

O build de debug gerou `bin/classbase-0.1.0-arm64-v8a-debug.apk`.

- Tamanho: 23.272.018 bytes
- Assinatura debug validada com APK Signature Scheme v2
- SHA-256: `6DC49552F5C641E08B0EAD358C9738F0E37BCF86C2D84E3FB4838CA4B4122AE0`

O APK é artefato de build e não deve ser versionado no Git.
