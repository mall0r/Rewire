# Rewire

Simple Python wrapper that intercepts Steam's `%command%` and swaps the final
executable for a configured one. For Proton games it keeps the whole
scaffolding (reaper, runtime, proton, `waitforexitandrun`) intact and replaces
only the target that follows the last `waitforexitandrun`.

> **Versionamento Semântico**: este projeto segue o
> [SemVer](https://semver.org/lang/pt-BR/). Mudanças estão documentadas no
> [CHANGELOG.md](CHANGELOG.md).

## Instalação

1. Install the package. For development (editable) use:

   ```bash
   pip install -e ".[dev]"
   ```

   Or for a regular install: `pip install . `. This provides the `rewire`
   entry point on your PATH.

## Configuração

Edit `~/.config/rewire/rewire.conf`. It is an INI file: each section is a
game's **appid**, and each section defines a `command` (parsed with
`shlex.split`, so quotes and `$VAR` work). Example:

```ini
[730]                   ; CS:GO appid
command = /path/to/another-executable --flag ~/.local/share/file
```

To target a game, create a section whose **name is that game's appid**. Steam
sets `STEAM_COMPAT_APPID` / `SteamAppId`; rewire reads it and looks up the
matching section.

## Uso na Steam

In the game's **Launch options**:

```
rewire %command%
```

At runtime:

1. Detect the game's appid.
2. If a section with that appid exists, replace the executable with its
   `command`.
3. Otherwise, run Steam's original `%command%` unchanged.

### Jogos via Proton

If `%command%` goes through Proton (contains `waitforexitandrun`), only the
**target** — what comes after the last `waitforexitandrun` — is replaced:

```
reaper SteamLaunch AppId=X -- steam-launch-wrapper -- runtime/_v2-entry-point
--verb=waitforexitandrun -- proton waitforexitandrun <SEU EXECUTÁVEL>
```

For native games (no Proton), the entire command is replaced.

> Note: `rewire` only swaps the executed target. Any other customization
> (env vars, MangoHud, prefix commands) should be added directly to the Steam
> launch options — `%command%` already forwards those unchanged.

## Log detalhado

The wrapper logs to `~/.cache/rewire/rewire.log` with timestamp and PID, and to
stderr. The `EXEC` lines show the swapped command for diagnosis:

```
2026-08-31 12:13:53 [INFO] pid=36102 intercepted command: reaper SteamLaunch AppId=730 -- steam-launch-wrapper -- proton waitforexitandrun /path/to/old
2026-08-31 12:13:53 [INFO] pid=36102 substitution [730]: /path/to/new
2026-08-31 12:13:53 [INFO] pid=36102 EXEC: appid=730 intercepted='...' | sent='...' | replaced_target='/path/to/old'
```

Configurable via env vars:

| Variável | Descrição | Padrão |
|---|---|---|
| `REWIRE_LOG` | Caminho do arquivo de log | `~/.cache/rewire/rewire.log` |
| `REWIRE_LOG_LEVEL` | `DEBUG`, `INFO`, `WARNING`, `ERROR` | `DEBUG` |
