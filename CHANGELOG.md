# Changelog

Todos as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não publicado]

## [0.1.1] - 2026-08-31

### Adicionado
- Empacotamento para Arch Linux via PKGBUILD e Makepkg (`make pkg-arch`)
- Empacotamento binário via PyInstaller (`make binary`)
- Makefile com alvos `dev`, `test`, `build`, `binary`, `pkg-arch` e `clean`
- Licença GPL-3.0-or-later e exigência de Python >= 3.14

### Corrigido
- `make clean` interrompido pelo `pkill -f "rewire"` que também matava o processo do Makefile

### Adicionado
- Intercepta `%command%` da Steam e substitui o executável conforme configuração
- Suporte a Proton (substitui apenas o alvo após `waitforexitandrun`)
- Suporte a jogos nativos (substitui o comando inteiro)
- Arquivo de configuração INI em `~/.config/rewire/rewire.conf`
- Logging detalhado em `~/.cache/rewire/rewire.log`
- Variáveis de ambiente configuráveis: `REWIRE_LOG`, `REWIRE_LOG_LEVEL`
- Entry point `rewire` para uso em opções de inicialização da Steam
