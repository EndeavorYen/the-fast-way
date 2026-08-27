---
name: the-fast-way
description: >
  Route work onto one skill at a time: gentle-grill-me, musk-algorithm,
  implement, then just-ten-more-loop. Use when the user says the fast way,
  which skill, from idea to merge, don't dig faster, or runs /the-fast-way.
  Use when requirements are uncertain or contradict each other.
  Explicit invocation always runs. Do not use when this message names
  gentle-grill-me, musk-algorithm, just-ten-more, or just-ten-more-loop
  and does not invoke the-fast-way.
---

Speak in the user's language.

This skill is a conductor. The sequence is the fast way. Do not merge
skills in one pass. Do not copy their protocols into this file. Load the
named skill and follow that skill's SKILL.md until it stops. Then come
back here. Do not wait for another /the-fast-way.

Step aside only if this user message named a leaf skill and did not invoke the-fast-way.
Then use that leaf skill and do not take the session back. Prior turns, and this
conductor naming the next skill, do not count as the user naming a leaf skill.

## Entry

Pick the earliest incomplete gate. Explicit invocation always runs.

| If they are here | Start at |
| --- | --- |
| Still choosing what to do, what success is, or the cost if wrong | gentle-grill-me |
| Requirements are uncertain or contradict each other | gentle-grill-me |
| Intent settled; requirements not yet questioned | musk-algorithm |
| musk-algorithm Decision is keep, they asked to implement, work is not done | implement (not these three skills) |
| Something exists; they want evidence, a list, or fixes | just-ten-more or just-ten-more-loop |
| They said the fast way / from idea to merge / did not name a gate | Default order, from the first incomplete gate |

Do not always start at gentle-grill-me. A bug hunt that already has a
subject starts at just-ten-more-loop, not at the grill.

If requirements are uncertain or contradict each other, the next gate is
gentle-grill-me even if musk-algorithm already started. Do not keep musk
or implement while that contradiction is open.

Detect the earliest incomplete gate from this conversation and, if
present, `.gentle-grill/grill-log.jsonl`. Do not invent a musk-algorithm
Decision. If Decision is unknown, run musk-algorithm.

Load the leaf skill from the installed skill root for this agent. If that
SKILL.md is missing, stop and name the missing path. Do not inline the
missing skill.

List-only: just-ten-more, and only if they asked to list without fixing.
Fix until a round finds none: just-ten-more-loop.
After implement, the next gate is just-ten-more-loop, not just-ten-more.

## Default order

1. gentle-grill-me until the user confirms the close log.
2. musk-algorithm on the settled subject.
3. If Decision is drop: stop. Do not implement. Do not hunt.
4. If Decision is keep and they asked to implement: implement as a
   separate pass. This conductor does not implement.
5. just-ten-more-loop on what survived.

After implement, do not auto-run musk-algorithm. Re-run musk-algorithm
only if a new process appeared, a new automation appeared, or the
surviving operator surface still names a deleted process.

One skill per pass. After that skill's own stop, re-enter the entry table
and run the next incomplete gate. Keep conducting until a terminal stop:
Decision is drop, they decline implement, just-ten-more-loop finds none,
they asked for list-only and just-ten-more finds none, or they cancel.

A gentle-grill-me close is a completed pass, not a ban on later passes
in this conversation. Implement only after musk-algorithm keep and they
asked, as the next pass.

After musk-algorithm keep, ask once whether to implement. Do not
implement unless they asked. If they decline, stop.

## Rationalizations

- "Hunt first, it is faster" — the wrong skill is slower.
- "Grill, musk, and ten-more in one message" — never merge.
- "Musk said keep; rewrite in this pass" — implement is a separate pass.
- "Always start at the grill" — use the entry table.
- "Speed means skip owners" — that is digging faster.
- "Keep musk running; grill the contradiction later" — uncertain or
  contradictory requirements are gentle-grill-me now.
