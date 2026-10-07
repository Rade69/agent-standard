# Task Contract — MEDIUM / HIGH (šablon, STANDARD.md §5.2)

```yaml
task_id:
title:
goal:
risk: MEDIUM | HIGH
risk_answers:
coordinator:
implementer:
reviewers:
base_commit:
branch:
worktree:
dependencies:
allowed_paths:
forbidden_paths:
acceptance:
failure_conditions:
verify:          # komande
self_check:      # kako implementer sam vidi da radi
rollback:        # obavezno za HIGH
```

## Tijelo (proza, ispod YAML bloka)

- Kontekst i razlog
- Source of truth
- Scope i out-of-scope
- Relevantni fajlovi i integration points
- Test strategija
- Review fokus i oborive hipoteze
- Procjena paralelnog rada (§8 STANDARD.md)
