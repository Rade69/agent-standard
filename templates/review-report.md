# Review report (šablon, STANDARD.md §10.2 + Prilog A.2)

```yaml
verdict: PASS | PASS_WITH_NOTES | FIXES_REQUIRED | REJECT
scope: PASS | FAIL
acceptance: PASS | FAIL
architecture: PASS | FAIL
security: PASS | FAIL | N/A
test_quality: PASS | FAIL
blocking_findings:
  - id: <stabilan ID>
    severity:
    location: <file:line ili komanda>
    failure_path:
    fix_direction:
```

## Narativ (ispod verdict bloka)

- Findinzi (detaljno, po jedan)
- Šta je reprodukovano (§10.1 koraci 6-7: bar jedna tvrdnja + adversarni scenario)
- Šta NIJE provjereno

Tok prije pisanja ovog reporta (§10.1): kontrakt → base/HEAD/diff/status →
scope/forbidden → stvarni kod i pozivaoci → acceptance↔evidence mapa →
reprodukcija → adversarni scenario → gate → TEK SADA implementer report →
verdict. Reviewer ne popravlja kod u istom prolazu.
