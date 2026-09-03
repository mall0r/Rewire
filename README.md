<p align="right">
  <a href="https://github.com/mall0r/Rewire/blob/main/README.md"><img src="https://img.shields.io/badge/en-US-darkblue.svg" alt="English"/></a>
  <a href="https://github.com/mall0r/Rewire/blob/main/docs/README.pt-BR.md"><img src="https://img.shields.io/badge/pt-BR-darkgreen.svg" alt="Portuguese"/></a>
</p>

# Rewire

Intercepts Steam's `%command%` launch option and replaces it with a configured command, per game.

## About

Rewire is a Linux utility that hooks into Steam's `%command%` launch option mechanism and replaces the game executable with a user-configured command. It supports both **Proton (Windows) games** and **native Linux games**, intelligently preserving the Proton scaffolding when needed.

## Features

- **Per-game configuration** — each game (by Steam App ID) gets its own section in the config file
- **Proton-aware command rewriting** — preserves `reaper`, `steam-launch-wrapper`, runtime entry points, and other launcher arguments while only swapping the target executable
- **Native Linux game support** — replaces the entire command with the configured replacement

## Requirements

- Python >= 3.12

## Installation

### Arch Linux (via AUR)

```sh
yay -S rewire
```

### Arch Linux (via Release)

Download the `.pkg.tar.zst` package from the [Releases](https://github.com/mall0r/Rewire/releases) page and install it:

```sh
sudo pacman -U ./rewire-0.1.3-1-any.pkg.tar.zst
```

### Debian / Ubuntu

Download the `.deb` package from the [Releases](https://github.com/mall0r/Rewire/releases) page and install it:

```sh
sudo apt install ./rewire_0.1.3_all.deb
```

### Fedora

Download the `.rpm` package from the [Releases](https://github.com/mall0r/Rewire/releases) page and install it:

```sh
# Fedora
sudo dnf install ./rewire-0.1.3-1.noarch.rpm
```

### Other systems

Download the standalone binary from the [Releases](https://github.com/mall0r/Rewire/releases) page, make it executable and add it to your `PATH`:

```sh
chmod +x rewire
mkdir -p ~/.local/bin
mv rewire ~/.local/bin/
export PATH="$PATH:$HOME/.local/bin"
```

To make the `PATH` change permanent, add the `export` line to your shell config:

```sh
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc   # bash
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.zshrc    # zsh
fish_add_path ~/.local/bin                                 # fish
```

## Configuration

Create the configuration file at `~/.config/rewire/rewire.conf`:

```ini
[730]
command = /path/to/my/replacement
```

Each section corresponds to a Steam App ID. The `command` value is the replacement command that will be run **in place of the game executable**. There is no `%command%` placeholder — what you set is exactly what gets executed.

## Usage

1. Open Steam and go to the game's properties
2. In **Launch Options**, set:

```
rewire %command%
```

3. Configure the replacement command in `~/.config/rewire/rewire.conf`
4. Launch the game

## License

[GPL-3.0-or-later](LICENSE)
