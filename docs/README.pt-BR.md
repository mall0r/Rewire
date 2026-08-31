# Rewire

Wrapper simples em Python que intercepta o `%command%` da Steam e troca o
executável final por um configurado. Em jogos via Proton, mantém todo o
arcabouço (reaper, runtime, proton, `waitforexitandrun`) intacto e substitui
apenas o alvo que segue o último `waitforexitandrun`.

## Instalação

1. Instale o pacote. Para desenvolvimento (editable):

   ```bash
   pip install -e ".[dev]"
   ```

   Ou para instalação normal: `pip install . `. Isso disponibiliza o entry
   point `rewire` no seu PATH.

## Compilar pacote nativo da distro

O `Makefile` detecta a distro atual (via `/etc/os-release`) e gera o pacote
**nativo** adequado (`.pkg.tar.zst` no Arch, `.deb` no Debian/Ubuntu, `.rpm` no
Fedora/RHEL/openSUSE):

```bash
make                # gera o pacote nativo para a distro atual
make install        # gera e instala no sistema (pede sudo)
make wheel          # gera wheel + sdist do Python em dist/
make info           # mostra a distro detectada e as ferramentas disponíveis
make clean          # remove os artefatos de build
make help           # mostra todos os alvos
```

O empacotamento nativo exige as ferramentas de build da distro (instalar uma
vez):

| Família de distro | Pacotes necessários |
|---|---|
| Arch (CachyOS, Manjaro…) | `base-devel python-build python-installer python-setuptools python-wheel` |
| Debian/Ubuntu | `dpkg dpkg-dev python3-pip` |
| Fedora/RHEL/openSUSE | `rpm-build python3-pip` |

> Nota: os scripts `.deb`/`.rpm` geram o wheel do Python internamente, então
> também precisam de `pip` (`python3-pip`).


## Configuração

Edite `~/.config/rewire/rewire.conf`. É um arquivo INI: cada seção é o
**appid** de um jogo, e cada seção define um `command` (analisado com
`shlex.split`, portanto aspas e `$VAR` funcionam). Exemplo:

```ini
[730]                   ; appid do CS:GO
command = /path/to/another-executable --flag ~/.local/share/file
```

Para configurar um jogo, crie uma seção cujo **nome seja o appid** desse jogo.
A Steam define `STEAM_COMPAT_APPID` / `SteamAppId`; o rewire lê e procura a
seção correspondente.

## Uso na Steam

Nos **Argumentos de lançamento** do jogo:

```
rewire %command%
```

No momento da execução:

1. Detecta o appid do jogo.
2. Se existir uma seção com esse appid, substitui o executável pelo `command`
   dela.
3. Caso contrário, executa o `%command%` original da Steam sem alterações.

### Jogos via Proton

Se o `%command%` passar por Proton (contém `waitforexitandrun`), apenas o
**alvo** — o que vem depois do último `waitforexitandrun` — é substituído:

```
reaper SteamLaunch AppId=X -- steam-launch-wrapper -- runtime/_v2-entry-point
--verb=waitforexitandrun -- proton waitforexitandrun <SEU EXECUTÁVEL>
```

Para jogos nativos (sem Proton), o comando inteiro é substituído.

> Nota: o `rewire` apenas troca o executável executado. Qualquer outra
> personalização (env vars, MangoHud, prefixos) deve ir direto nos launch
> options da Steam — o `%command%` já repassa tudo isso sem alteração.

## Log detalhado

O wrapper gera um log em `~/.cache/rewire/rewire.log` com timestamp e PID, e
também no stderr. As linhas `EXEC` mostram o comando trocado para diagnóstico:

```
2026-08-31 12:13:53 [INFO] pid=36102 intercepted command: reaper SteamLaunch AppId=730 -- steam-launch-wrapper -- proton waitforexitandrun /path/to/old
2026-08-31 12:13:53 [INFO] pid=36102 substitution [730]: /path/to/new
2026-08-31 12:13:53 [INFO] pid=36102 EXEC: appid=730 intercepted='...' | sent='...' | replaced_target='/path/to/old'
```

Configurável por env vars:

| Variável | Descrição | Padrão |
|---|---|---|
| `REWIRE_LOG` | Caminho do arquivo de log | `~/.cache/rewire/rewire.log` |
| `REWIRE_LOG_LEVEL` | `DEBUG`, `INFO`, `WARNING`, `ERROR` | `DEBUG` |
