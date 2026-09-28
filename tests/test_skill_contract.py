#!/usr/bin/env python3
"""Run the skill contract checks under pytest."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))

import check_skill  # noqa: E402


def test_skill_contract() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "tests" / "check_skill.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def _skill_with_description(tmp_path: Path, length: int) -> Path:
    source = check_skill.SKILL_PATH.read_text(encoding="utf-8")
    description = "description: " + "x" * length + "\n"
    replaced = re.sub(r"(?ms)^description:.*?(?=^\S)", lambda _: description, source, count=1)
    path = tmp_path / "SKILL.md"
    path.write_text(replaced, encoding="utf-8")
    assert len(check_skill.description_text(check_skill.split_frontmatter(replaced)[0])) == length
    return path


def test_description_over_1024_fails(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert check_skill.main(skill_path=_skill_with_description(tmp_path, 1025)) == 1
    assert "FAIL description at most 1024 characters" in capsys.readouterr().out.splitlines()


def test_description_of_1024_passes(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    check_skill.main(skill_path=_skill_with_description(tmp_path, 1024))
    assert "PASS description at most 1024 characters" in capsys.readouterr().out.splitlines()


@pytest.mark.parametrize(
    ("frontmatter", "expected"),
    [
        ("description: >\n  one two\n  three\nname: x", "one two three"),
        ("description: |\n  one\n  two\n", "one\ntwo"),
        ("description: 'quoted value'\n", "quoted value"),
        ('description: "quoted value"\n', "quoted value"),
        ("description: plain value\n", "plain value"),
        ("description: plain value # comment\n", "plain value"),
        ("description: aaa\n  bbb\nname: x", "aaa bbb"),
        ('description: "aaa\n  bbb"\nname: x', "aaa bbb"),
        ("description: 'it''s'\n", "it's"),
        ("description:\n  aaa\n  bbb\n", "aaa bbb"),
        ("description: |\n  aaa\n    bbb\n", "aaa\n  bbb"),
        ("description: >\n  aaa\n\n  bbb\n", "aaa\nbbb"),
    ],
)
def test_description_text_parses_scalar_styles(frontmatter: str, expected: str) -> None:
    assert check_skill.description_text(frontmatter) == expected
