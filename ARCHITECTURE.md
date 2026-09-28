# the-fast-way architecture

Independent Grok skill. Same `SKILL.md` copies to Claude, Cursor, and Hermes. A conductor: it names the next skill. It does not inline gentle-grill-me, musk-algorithm, or just-ten-more-loop.

| | the-fast-way |
|---|---|
| Job | Pick the earliest incomplete gate; stay in charge until a terminal stop; one skill per pass |
| Default order | gentle-grill-me → musk-algorithm → implement → just-ten-more-loop |
| Drop | musk-algorithm Decision drop stops the path |
| After implement | just-ten-more-loop; do not auto-run musk-algorithm |
| Helper | None |

## File tree

```
LICENSE                     MIT, EndeavorYen 2026 (do not rewrite)
ARCHITECTURE.md             This file: layout and data flow
SKILL.md                    Agent prompt (YAML frontmatter + English body)
README.md                   Human story + install
scripts/install.ps1         Windows installer
scripts/install.sh          Unix installer (git 100755, LF-only)
tests/check_skill.py        Structural + install acceptance
tests/test_skill_contract.py  Thin pytest wrapper around check_skill.py
.gitignore                  __pycache__/, .pytest_cache/, .grok/, .just-ten-more/, .gentle-grill/
.gitattributes              scripts/install.sh text eol=lf
```

Installed skill root (`the-fast-way/`): `SKILL.md`, `README.md`. Not installed: `LICENSE`, `ARCHITECTURE.md`, `scripts/`, `tests/`.

## What each file owns

- **SKILL.md** — When to run (explicit invocation always; step aside only if this message named a leaf skill and did not invoke the-fast-way), the entry table, default order, drop-stop, stay in charge until a terminal stop. SKILL.md, README.md, and install scripts are English. Runtime may still speak the user's language.
- **README.md** — What it is, entry table, install table, `GROK_HOME` / `HERMES_HOME`.
- **scripts/install.ps1**, **scripts/install.sh** — Copy `SKILL.md` and optional `README.md`. One positional arg: `grok | claude | cursor | hermes | all` (default `all`). Default also clones https://github.com/EndeavorYen/gentle-grill-me, musk-algorithm-skill, and just-ten-more, then runs each leaf installer. `-SkipLeaves` / `--skip-leaves` / `THE_FAST_WAY_SKIP_LEAVES=1` skips clones. Leaf SKILL files are not stored in this repo.
- **tests/check_skill.py** — Named PASS/FAIL checks: frontmatter (parsed description at most 1024 characters), entry/order/drop/stay-in-charge bars, English body, installers, LF on `install.sh`, git mode `100755`, README paths, gitignore, tempdir install (never the real home).
- **tests/test_skill_contract.py** — `pytest` exec of `check_skill.py`; assert returncode 0.

## Data flow

```
trigger (/the-fast-way, the fast way, which skill, from idea to merge)
    -> load SKILL.md (agent)
    -> if this message named a leaf skill and did not invoke the-fast-way: stop; use that skill
    -> pick gate from positive signals (missing grill-log is not uncertainty)
    -> load that skill's SKILL.md; follow it until it stops
    -> re-enter entry table (do not wait for another /the-fast-way)
    -> musk-algorithm Decision drop: terminal stop
    -> keep: ask once to implement; decline is terminal stop
    -> keep + asked: separate implement pass, then just-ten-more-loop
    -> loop finds none: terminal stop
    -> do not auto-run musk-algorithm after implement
```

## Install destinations

Repo root is the parent of `scripts/`. Home: sh `$HOME`; ps1 `$env:USERPROFILE` else `$HOME`.

| Target | Destination |
| --- | --- |
| grok | `$GROK_HOME/skills/the-fast-way` if set, else `$HOME/.grok/skills/the-fast-way` |
| hermes | `$HERMES_HOME/skills/the-fast-way` if set, else `$HOME/.hermes/skills/the-fast-way` |
| claude | `$HOME/.claude/skills/the-fast-way` (no env override) |
| cursor | `$HOME/.cursor/skills/the-fast-way` (no env override) |

`all` = grok, claude, cursor, hermes in that order. Unknown platform: ps1 `ValidateSet` / throw; sh usage and exit 2.

Tests prove install in a tempdir with `USERPROFILE=HOME=tmp` and `GROK_HOME` / `HERMES_HOME` popped. Do not install into the real user home from tests.
