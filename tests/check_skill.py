#!/usr/bin/env python3
"""Structural acceptance checks for the-fast-way. Run from the skill root."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "SKILL.md"
README_PATH = ROOT / "README.md"

CJK = re.compile(r"[\u4e00-\u9fff]")
ORDER_MARKERS = (
    "1. gentle-grill-me",
    "2. musk-algorithm",
    "5. just-ten-more-loop",
)


def read_text(path: Path) -> str | None:
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    rest = text[3:]
    if rest.startswith("\r\n"):
        rest = rest[2:]
    elif rest.startswith("\n"):
        rest = rest[1:]
    match = re.search(r"\n---\s*(?:\n|$)", rest)
    if not match:
        return "", text
    return rest[: match.start()], rest[match.end() :]


def first_occurrences_in_order(text: str, needles: tuple[str, ...]) -> bool:
    lower = text.lower()
    positions: list[int] = []
    for needle in needles:
        found = lower.find(needle.lower())
        if found < 0:
            return False
        positions.append(found)
    return all(positions[i] < positions[i + 1] for i in range(len(positions) - 1))


def _posix_shell() -> str | None:
    if os.name != "nt":
        return "bash"
    git_bash = Path(r"C:\Program Files\Git\bin\bash.exe")
    if git_bash.is_file():
        return str(git_bash)
    return None


def _run(cmd: list[str], env: dict) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )


def _run_install(platform: str, env: dict) -> subprocess.CompletedProcess[str]:
    if os.name == "nt":
        return _run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(ROOT / "scripts" / "install.ps1"),
                platform,
            ],
            env,
        )
    return _run(["bash", str(ROOT / "scripts" / "install.sh"), platform], env)


def _copied_equal(dest: Path, src: Path) -> bool:
    return dest.is_file() and src.is_file() and dest.read_bytes() == src.read_bytes()


def main() -> int:
    skill = read_text(SKILL_PATH) or ""
    readme = read_text(README_PATH) or ""
    fm, body = split_frontmatter(skill)
    body_l = body.lower()
    fm_l = fm.lower()
    checks: list[tuple[str, bool]] = []

    def check(name: str, ok: bool) -> None:
        checks.append((name, bool(ok)))

    check("SKILL.md frontmatter name the-fast-way", bool(re.search(r"(?m)^name:\s*the-fast-way\s*$", fm)))
    check("description contains the fast way", "the fast way" in fm_l)
    check("description contains /the-fast-way", "/the-fast-way" in fm)
    check("description says explicit invocation always", "explicit invocation always" in fm_l)
    check(
        "description steps aside when this message names a leaf skill",
        "do not use when this message names" in fm_l,
    )
    check(
        "description triggers on uncertain or contradictory requirements",
        "uncertain" in fm_l and "contradict" in fm_l,
    )

    check("body names gentle-grill-me", "gentle-grill-me" in body_l)
    check("body names musk-algorithm", "musk-algorithm" in body_l)
    check("body names just-ten-more-loop", "just-ten-more-loop" in body_l)
    check("default order appears in sequence", first_occurrences_in_order(body, ORDER_MARKERS))
    check("body is a conductor", "conductor" in body_l)
    check("body forbids copying protocols", "do not copy" in body_l)
    check("body forbids merging in one pass", "do not merge" in body_l)
    check(
        "drop stops the path",
        "decision is drop" in body_l and "do not implement" in body_l and "do not hunt" in body_l,
    )
    check(
        "do not auto-run musk-algorithm after implement",
        "do not auto-run musk-algorithm" in body_l,
    )
    check("do not always start at the grill", "do not always start at gentle-grill-me" in body_l)
    check(
        "uncertain or contradictory requirements go to gentle-grill-me",
        "requirements are uncertain or contradict each other" in body_l
        and "next gate is" in body_l
        and "gentle-grill-me" in body_l,
    )
    check(
        "steps aside only if this message named a leaf skill",
        "this user message named a leaf skill" in body_l
        and "did not invoke the-fast-way" in body_l,
    )
    check(
        "after implement the next gate is just-ten-more-loop",
        "after implement, the next gate is just-ten-more-loop" in body_l,
    )
    check(
        "missing leaf SKILL.md is a stop",
        "if that" in body_l and "skill.md is missing" in body_l,
    )
    check("does not invent a musk-algorithm Decision", "do not invent a musk-algorithm" in body_l)
    check("one skill per pass", "one skill per pass" in body_l)
    check("conductor does not implement", "does not implement" in body_l)
    check(
        "does not wait for another /the-fast-way",
        "do not wait for another /the-fast-way" in body_l,
    )
    check("re-enters the entry table after a leaf stop", "re-enter the entry table" in body_l)
    check(
        "asks once whether to implement after keep",
        "ask once whether to implement" in body_l,
    )

    english_files = [
        SKILL_PATH,
        README_PATH,
        ROOT / "ARCHITECTURE.md",
        ROOT / "scripts" / "install.ps1",
        ROOT / "scripts" / "install.sh",
        ROOT / "tests" / "check_skill.py",
        ROOT / "tests" / "test_skill_contract.py",
    ]
    for path in english_files:
        text = read_text(path) or ""
        check(f"{path.relative_to(ROOT).as_posix()} is English", not CJK.search(text))
    check("SKILL.md body is English", not CJK.search(body))
    check("scripts/install.ps1 exists", (ROOT / "scripts" / "install.ps1").is_file())
    check("scripts/install.sh exists", (ROOT / "scripts" / "install.sh").is_file())
    check("install.sh has no CR", b"\r" not in (ROOT / "scripts" / "install.sh").read_bytes())
    gitattributes = read_text(ROOT / ".gitattributes") or ""
    check("gitattributes forces install.sh LF", "scripts/install.sh" in gitattributes and "eol=lf" in gitattributes)
    mode = subprocess.run(
        ["git", "ls-files", "-s", "scripts/install.sh"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    check("install.sh is executable in git", mode.stdout.startswith("100755"))
    check("README install path", "~/.grok/skills/the-fast-way/" in readme)
    check("README documents GROK_HOME", "GROK_HOME" in readme)
    check("README hermes install path", "~/.hermes/skills/the-fast-way/" in readme)
    check("README documents HERMES_HOME", "HERMES_HOME" in readme)
    check("README names gentle-grill-me", "gentle-grill-me" in readme)
    check("README names musk-algorithm", "musk-algorithm" in readme)
    check("README names just-ten-more-loop", "just-ten-more-loop" in readme)
    check(
        "README clones gentle-grill-me from GitHub",
        "https://github.com/endeavoryen/gentle-grill-me" in readme.lower(),
    )
    check(
        "README clones musk-algorithm-skill from GitHub",
        "https://github.com/endeavoryen/musk-algorithm-skill" in readme.lower(),
    )
    check(
        "README clones just-ten-more from GitHub",
        "https://github.com/endeavoryen/just-ten-more" in readme.lower(),
    )
    install_ps = read_text(ROOT / "scripts" / "install.ps1") or ""
    install_sh = read_text(ROOT / "scripts" / "install.sh") or ""
    check("install.ps1 clones gentle-grill-me", "github.com/EndeavorYen/gentle-grill-me.git" in install_ps)
    check("install.ps1 clones musk-algorithm-skill", "github.com/EndeavorYen/musk-algorithm-skill.git" in install_ps)
    check("install.ps1 clones just-ten-more", "github.com/EndeavorYen/just-ten-more.git" in install_ps)
    check("install.ps1 honors SkipLeaves", "SkipLeaves" in install_ps and "THE_FAST_WAY_SKIP_LEAVES" in install_ps)
    check("install.sh clones gentle-grill-me", "github.com/EndeavorYen/gentle-grill-me.git" in install_sh)
    check("install.sh honors skip-leaves", "--skip-leaves" in install_sh and "THE_FAST_WAY_SKIP_LEAVES" in install_sh)
    check("this repo does not vendor leaf SKILL.md copies", not (ROOT / "leaves").exists())
    check(
        "README steps aside only when this message names a leaf skill",
        "if this message names one of those skills" in readme.lower(),
    )
    gitignore = read_text(ROOT / ".gitignore") or ""
    check(".gitignore lists .just-ten-more/", ".just-ten-more/" in gitignore)
    check(".gitignore lists .gentle-grill/", ".gentle-grill/" in gitignore)
    ignore_proc = subprocess.run(
        ["git", "check-ignore", "-q", "--", ".just-ten-more/review-log.jsonl"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    check(
        "git ignores .just-ten-more/review-log.jsonl",
        ignore_proc.returncode == 0,
    )

    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp) / "dest"
        dest.mkdir()
        env = {
            **{k: v for k, v in os.environ.items()},
            "USERPROFILE": str(dest),
            "HOME": str(dest),
            "THE_FAST_WAY_SKIP_LEAVES": "1",
        }
        env.pop("GROK_HOME", None)
        env.pop("HERMES_HOME", None)
        proc = _run_install("grok", env)
        installed = dest / ".grok" / "skills" / "the-fast-way"
        src_skill = SKILL_PATH.read_text(encoding="utf-8") if SKILL_PATH.is_file() else ""
        src_readme = README_PATH.read_text(encoding="utf-8") if README_PATH.is_file() else ""
        check(
            "install grok copies SKILL.md",
            proc.returncode == 0 and (installed / "SKILL.md").is_file(),
        )
        check("install grok copies README.md", (installed / "README.md").is_file())
        check(
            "copied SKILL.md matches source",
            _copied_equal(installed / "SKILL.md", SKILL_PATH) and bool(src_skill),
        )
        check(
            "copied README.md matches source",
            _copied_equal(installed / "README.md", README_PATH) and bool(src_readme),
        )

        proc_all = _run_install("all", env)
        check("install all succeeds", proc_all.returncode == 0)
        check(
            "install all copies claude SKILL.md",
            (dest / ".claude" / "skills" / "the-fast-way" / "SKILL.md").is_file(),
        )
        check(
            "install all copies cursor SKILL.md",
            (dest / ".cursor" / "skills" / "the-fast-way" / "SKILL.md").is_file(),
        )
        check(
            "install all copies hermes SKILL.md",
            (dest / ".hermes" / "skills" / "the-fast-way" / "SKILL.md").is_file(),
        )

        hhome = dest / "custom-hermes"
        env_hermes = {**env, "HERMES_HOME": str(hhome)}
        proc_hermes = _run_install("hermes", env_hermes)
        hermes_installed = hhome / "skills" / "the-fast-way"
        check(
            "HERMES_HOME dest copies SKILL.md",
            proc_hermes.returncode == 0 and (hermes_installed / "SKILL.md").is_file(),
        )

        ghome = dest / "custom-grok"
        env_home = {**env, "GROK_HOME": str(ghome)}
        proc_home = _run_install("grok", env_home)
        grok_installed = ghome / "skills" / "the-fast-way"
        check(
            "GROK_HOME dest copies SKILL.md",
            proc_home.returncode == 0 and (grok_installed / "SKILL.md").is_file(),
        )
        check(
            "GROK_HOME dest copies README.md",
            (grok_installed / "README.md").is_file(),
        )

        if os.name == "nt":
            bad_ps = _run_install("nope", env)
            check("install.ps1 rejects unknown platform", bad_ps.returncode != 0)

        shell = _posix_shell()
        if shell is None and os.name == "nt":
            check("install.sh checks skipped without posix shell", True)
        else:
            check("posix shell available to test install.sh", shell is not None)
        if shell:
            bad_sh = _run([shell, str(ROOT / "scripts" / "install.sh"), "nope"], env)
            check("install.sh rejects unknown platform", bad_sh.returncode != 0)
            sh_home = dest / "sh-home"
            sh_home.mkdir()
            env_sh = {**env, "HOME": str(sh_home)}
            env_sh.pop("GROK_HOME", None)
            proc_sh = _run([shell, str(ROOT / "scripts" / "install.sh"), "grok"], env_sh)
            sh_skill = sh_home / ".grok" / "skills" / "the-fast-way" / "SKILL.md"
            check(
                "install.sh grok copies SKILL.md",
                proc_sh.returncode == 0 and sh_skill.is_file(),
            )

    failed = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
    if failed:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
