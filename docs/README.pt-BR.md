<p align="right">
  <a href="https://github.com/mall0r/Rewire/blob/main/README.md"><img src="https://img.shields.io/badge/en-US-darkblue.svg" alt="English"/></a>
  <a href="https://github.com/mall0r/Rewire/blob/main/docs/README.pt-BR.md"><img src="https://img.shields.io/badge/pt-BR-darkgreen.svg" alt="Portuguese"/></a>
</p>

# Rewire

Intercepta a opção de lançamento `%command%` do Steam e a substitui por um comando configurado, por jogo.

## Sobre

Rewire é um utilitário Linux que se conecta ao mecanismo da opção de lançamento `%command%` do Steam e substitui o executável do jogo por um comando configurado pelo usuário. Ele suporta tanto **jogos Proton (Windows)** quanto **jogos nativos Linux**, preservando inteligentemente a estrutura do Proton quando necessário.

## Recursos

- **Configuração por jogo** — cada jogo (pelo Steam App ID) tem sua própria seção no arquivo de configuração
- **Reescrita de comando ciente de Proton** — preserva `reaper`, `steam-launch-wrapper`, pontos de entrada do runtime e outros argumentos de lançador, substituindo apenas o executável de destino
- **Suporte a jogos nativos Linux** — substitui o comando inteiro pela configuração do usuário

## Requisitos

- Python >= 3.12

## Instalação

### Arch Linux (via AUR)

```sh
yay -S rewire
```

### Arch Linux (via Release)

Baixe o pacote `.pkg.tar.zst` da página de [Releases](https://github.com/mall0r/Rewire/releases) e instale:

```sh
sudo pacman -U ./rewire-0.1.3-1-any.pkg.tar.zst
```

### Debian / Ubuntu

Baixe o pacote `.deb` da página de [Releases](https://github.com/mall0r/Rewire/releases) e instale:

```sh
sudo apt install ./rewire_0.1.3_all.deb
```

### Fedora / RHEL / openSUSE

Baixe o pacote `.rpm` da página de [Releases](https://github.com/mall0r/Rewire/releases) e instale:

```sh
# Fedora
sudo dnf install ./rewire-0.1.3-1.noarch.rpm
```

### Outros sistemas

Baixe o binário standalone da página de [Releases](https://github.com/mall0r/Rewire/releases), torne-o executável e adicione-o ao seu `PATH`:

```sh
chmod +x rewire
mkdir -p ~/.local/bin
mv rewire ~/.local/bin/
export PATH="$PATH:$HOME/.local/bin"
```

Para tornar a alteração do `PATH` permanente, adicione a linha `export` ao seu arquivo de configuração do shell:

```sh
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc   # bash
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.zshrc    # zsh
fish_add_path ~/.local/bin                                 # fish
```

## Configuração

Crie o arquivo de configuração em `~/.config/rewire/rewire.conf`:

```ini
[730]
command = /caminho/para/minha/substituicao
```

Cada seção corresponde a um Steam App ID. O valor `command` é o comando de substituição que será executado **no lugar do executável do jogo**. Não existe placeholder `%command%` — o que você definir é exatamente o que será executado.

## Uso

1. Abra o Steam e vá nas propriedades do jogo
2. Em **Opções de Lançamento**, defina:

```
rewire %command%
```

3. Configure o comando de substituição em `~/.config/rewire/rewire.conf`
4. Inicie o jogo

## Licença

[GPL-3.0-or-later](../../LICENSE)
