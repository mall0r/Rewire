# Changelog

Todos as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não publicado]

## [0.1.3] - 2026-09-03

### Corrigido
- `build_final_args` poupava erroneamente opções do launcher (como `--oom-score-adjust` do Proton) ao montar a linha de comando final

## [0.1.2] - 2026-08-31

### Adicionado
- Empacotamento Debian/Ubuntu via script `pkg-deb` e `dpkg-deb` (`make pkg-deb`)
- Empacotamento RPM (Fedora/RHEL/openSUSE) via script `pkg-rpm` e `rpmbuild` (`make pkg-rpm`)
- Makefile: detecção de `PYTHON` e versão derivada automaticamente de `__init__.py`; alvos `pkg-deb` e `pkg-rpm`

## [0.1.1] - 2026-08-31

### Adicionado
- Empacotamento para Arch Linux via PKGBUILD e Makepkg (`make pkg-arch`)
- Empacotamento binário via PyInstaller (`make binary`)
- Makefile com alvos `dev`, `test`, `build`, `binary`, `pkg-arch` e `clean`
- Licença GPL-3.0-or-later e exigência de Python >= 3.12

### Corrigido
- `make clean` interrompido pelo `pkill -f "rewire"` que também matava o processo do Makefile

## [0.1.0] - 2026-08-31

### Adicionado
- Intercepta `%command%` da Steam e substitui o executável conforme configuração
- Suporte a Proton (substitui apenas o alvo após `waitforexitandrun`)
- Suporte a jogos nativos (substitui o comando inteiro)
- Arquivo de configuração INI em `~/.config/rewire/rewire.conf`
- Logging detalhado em `~/.cache/rewire/rewire.log`
- Variáveis de ambiente configuráveis: `REWIRE_LOG`, `REWIRE_LOG_LEVEL`
- Entry point `rewire` para uso em opções de inicialização da Steam
