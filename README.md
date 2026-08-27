# the-fast-way

> **TL;DR** — This is the fast way. Owners, then build. Ten more last. Don't dig faster.

A conductor skill. One `/the-fast-way` picks the current gate and keeps
routing until a terminal stop. It does not run grill, Musk's five steps,
or the hunt inside this file. They do not re-type the slash after each
gate unless they named a leaf skill (that skill then owns the rest).

Works as a Grok skill. The same `SKILL.md` copies onto Claude, Cursor, and Hermes.

## Quick start

Clone, install, then say `the fast way` or `/the-fast-way`.

```powershell
.\scripts\install.ps1 grok
```

```bash
./scripts/install.sh grok
```

Use `claude`, `cursor`, `hermes`, or `all` instead of `grok`.

## Default order

1. **gentle-grill-me** — intent, success, cost if wrong. Stop until the close log is confirmed.
2. **musk-algorithm** — named owners, delete, then the rest of the five steps. **Drop → stop.**
3. **Implement** — only if Decision is keep and they asked. Not these three skills.
4. **just-ten-more-loop** — evidence, fix or block, until a round finds none.

After implement, do not auto-run musk-algorithm. Ten more last.

## Entry

Do not always start at the grill.

| If they are here | Start at |
| --- | --- |
| Still choosing what to do | gentle-grill-me |
| Requirements uncertain or contradictory | gentle-grill-me |
| Intent settled, requirements not questioned | musk-algorithm |
| Keep + asked to implement | implement |
| Thing exists; list or fix | just-ten-more / just-ten-more-loop |
| "the fast way" / from idea to merge | first incomplete gate |

If this message names one of those skills and does not invoke the-fast-way, that skill wins. This conductor steps aside.

Never merge them in one pass.

## Install

One argument: `grok` | `claude` | `cursor` | `hermes` | `all`. Default `all`. Unknown platform is rejected.

Default install copies this conductor, then `git clone --depth 1` these GitHub repos (not vendored here) and runs each repo's own installer for the same platform:

- https://github.com/EndeavorYen/gentle-grill-me
- https://github.com/EndeavorYen/musk-algorithm-skill
- https://github.com/EndeavorYen/just-ten-more

`just-ten-more` installs both `/just-ten-more` and `/just-ten-more-loop`. `git` must be on PATH. If a leaf installer rejects `hermes`, that leaf is skipped on hermes only.

CI / offline: `.\scripts\install.ps1 grok -SkipLeaves` or `THE_FAST_WAY_SKIP_LEAVES=1`. Unix: `./scripts/install.sh grok --skip-leaves`.

| Platform | Skill root |
| --- | --- |
| grok | `~/.grok/skills/the-fast-way/` |
| claude | `~/.claude/skills/the-fast-way/` |
| cursor | `~/.cursor/skills/the-fast-way/` |
| hermes | `~/.hermes/skills/the-fast-way/` |

```text
# Windows
.\scripts\install.ps1 grok
.\scripts\install.ps1 claude
.\scripts\install.ps1 cursor
.\scripts\install.ps1 hermes
.\scripts\install.ps1 all

# Unix
./scripts/install.sh grok
./scripts/install.sh claude
./scripts/install.sh cursor
./scripts/install.sh hermes
./scripts/install.sh all
```

If `GROK_HOME` is set, the grok target is `$GROK_HOME/skills/the-fast-way/`.
If `HERMES_HOME` is set, the hermes target is `$HERMES_HOME/skills/the-fast-way/`.

Claude and Cursor always use the home paths in the table.

The destination contains `SKILL.md` and `README.md`. Restart the agent if it was already running.

Confirm:

```powershell
Test-Path "$env:USERPROFILE\.grok\skills\the-fast-way\SKILL.md"
```

```bash
test -f ~/.grok/skills/the-fast-way/SKILL.md && echo installed
```

Uninstall: delete the skill directory. Nothing else is registered.

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.grok\skills\the-fast-way"
```

```bash
rm -rf ~/.grok/skills/the-fast-way
```

Repeat for claude, cursor, and hermes if you installed `all`. If you used `GROK_HOME` or `HERMES_HOME`, delete those paths instead.

## Usage

**Explicit (always):** `/the-fast-way`, or `the fast way` / `from idea to merge`. Explicit invocation always runs.

**Automatic (only when it fits):** they ask which skill to run, or they want idea-to-merge without naming a gate. It does **not** steal the turn when this message names gentle-grill-me, musk-algorithm, just-ten-more, or just-ten-more-loop and does not invoke the-fast-way.

## Layout

```
SKILL.md                     Agent prompt
README.md                    This file
ARCHITECTURE.md              Maintainer layout
scripts/install.ps1          Windows installer
scripts/install.sh           Unix installer (git 100755, LF)
tests/                       Structural + install acceptance
```

Installed skill root: `SKILL.md`, `README.md`.
