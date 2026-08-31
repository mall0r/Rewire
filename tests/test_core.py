"""Tests for rewire.core: appid detection and command rebuilding."""

import os

import pytest

from rewire.core import build_final_args, detect_appid, resolve_replacement
from rewire.config import GENERIC_KEY, load_config


class TestDetectAppid:
    def test_returns_steam_compat_appid(self):
        assert detect_appid({"STEAM_COMPAT_APPID": "730"}) == "730"

    def test_returns_steamappid_fallback(self):
        assert detect_appid({"SteamAppId": "730"}) == "730"

    def test_steam_compat_takes_precedence(self):
        env = {"STEAM_COMPAT_APPID": "730", "SteamAppId": "999"}
        assert detect_appid(env) == "730"

    def test_ignores_non_numeric(self):
        assert detect_appid({"STEAM_COMPAT_APPID": "abc"}) is None

    def test_ignores_empty(self):
        assert detect_appid({"STEAM_COMPAT_APPID": "  "}) is None

    def test_returns_none_when_absent(self):
        assert detect_appid({}) is None

    def test_defaults_to_process_environ(self, monkeypatch):
        monkeypatch.setenv("STEAM_COMPAT_APPID", "440")
        assert detect_appid() == "440"


class TestBuildFinalArgs:
    @pytest.mark.parametrize(
        "original",
        [
            ["game", "--flag"],
            [],
        ],
    )
    def test_native_replaces_everything(self, original):
        replacement = ["echo", "hi"]
        final, replaced = build_final_args(original, replacement)
        assert final == replacement
        assert replaced == original

    def test_proton_replaces_target(self):
        original = [
            "reaper",
            "SteamLaunch",
            "--",
            "steam-launch-wrapper",
            "--",
            "runtime/_v2-entry-point",
            "--verb=waitforexitandrun",
            "--",
            "proton",
            "waitforexitandrun",
            "old_game",
        ]
        replacement = ["new_game"]
        final, replaced = build_final_args(original, replacement)
        assert final == original[:10] + replacement
        assert replaced == ["old_game"]

    def test_empty_replacement_returns_original(self):
        original = ["old_game"]
        final, replaced = build_final_args(original, [])
        assert final == original
        assert replaced == []


class TestResolveReplacement:
    def test_no_match_returns_none(self, tmp_path):
        config = tmp_path / "rewire.conf"
        config.write_text("[999]\ncommand = echo x\n")
        cfg = load_config(config)
        section, args = resolve_replacement("730", cfg)
        assert section is None
        assert args == []

    def test_match_returns_section_and_args(self, tmp_path):
        config = tmp_path / "rewire.conf"
        config.write_text("[730]\ncommand = /bin/new --flag\n")
        cfg = load_config(config)
        section, args = resolve_replacement("730", cfg)
        assert section == "730"
        assert args == ["/bin/new", "--flag"]

    def test_splits_command_with_shlex(self, tmp_path):
        config = tmp_path / "rewire.conf"
        config.write_text(f"[1]\n{GENERIC_KEY} = echo '$HOME hi'\n")
        cfg = load_config(config)
        _, args = resolve_replacement("1", cfg)
        assert args == ["echo", "$HOME hi"]

    def test_appid_none_returns_none(self, tmp_path):
        config = tmp_path / "rewire.conf"
        config.write_text("[730]\ncommand = echo x\n")
        cfg = load_config(config)
        section, args = resolve_replacement(None, cfg)
        assert section is None
        assert args == []


class TestLoadConfig:
    def test_missing_file_returns_empty_config(self, tmp_path):
        cfg = load_config(tmp_path / "nonexistent.conf")
        assert cfg.sections() == []

    def test_reads_sections(self, tmp_path):
        config = tmp_path / "rewire.conf"
        config.write_text("[730]\ncommand = echo x\n")
        cfg = load_config(config)
        assert cfg.has_section("730")
