# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.3] - 2026-09-03

### Fixed
- `build_final_args` was incorrectly dropping launcher options (such as Proton's `--oom-score-adjust`) when assembling the final command line

## [0.1.2] - 2026-08-31

### Added
- Debian/Ubuntu packaging via `pkg-deb` script and `dpkg-deb` (`make pkg-deb`)
- RPM packaging (Fedora/RHEL/openSUSE) via `pkg-rpm` script and `rpmbuild` (`make pkg-rpm`)
- Makefile: automatic `PYTHON` detection and version derivation from `__init__.py`; `pkg-deb` and `pkg-rpm` targets

## [0.1.1] - 2026-08-31

### Added
- Arch Linux packaging via PKGBUILD and Makepkg (`make pkg-arch`)
- Binary packaging via PyInstaller (`make binary`)
- Makefile with `dev`, `test`, `build`, `binary`, `pkg-arch` and `clean` targets
- GPL-3.0-or-later license and Python >= 3.12 requirement

### Fixed
- `make clean` interrupted by `pkill -f "rewire"` which also killed the Makefile process

## [0.1.0] - 2026-08-31

### Added
- Intercepts Steam's `%command%` and replaces the executable based on configuration
- Proton support (replaces only the target after `waitforexitandrun`)
- Native game support (replaces the entire command)
- INI configuration file at `~/.config/rewire/rewire.conf`
- Detailed logging to `~/.cache/rewire/rewire.log`
- Configurable environment variables: `REWIRE_LOG`, `REWIRE_LOG_LEVEL`
- `rewire` entry point for use in Steam launch options
