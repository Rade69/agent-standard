---
task_id: AGENT-STD-001
role: implementer
agent: Claude Code
model: claude-sonnet-5
branch: n/a (novi repo, nema prethodnog brancha)
base_commit: n/a (prvi commit)
head_commit: 49afc5d
risk: MEDIUM
status: DONE
---

## Korak 0 — odluke Human Ownera

```text
a) Status standarda v1.1: USVOJEN (korisnik, verbatim: "Usvojen je.")
b) Remote repo: https://github.com/Rade69/agent-standard (korisnik dao URL direktno)
c) Pokrivenost u fazi 1: Pi, Crush, OpenCode i Cursor (korisnik: "Da ulaye i pi
   i crush i open code i Cursor") — PROŠIRENJE originalnog kontrakta, koji je
   u Koraku 0c pitao samo za Pi/Crush. OpenCode i Cursor nisu bili u §3 tabeli
   ni u allowed_paths originalnog kontrakta; uključeni su po eksplicitnoj
   korisničkoj odluci, ne agentskoj inicijativi.
d) MiniMax: izostavljen za fazu 1 (korisnik: "je za sada izostavljen").
e) v0.2 standard u ~/.claude/CLAUDE.md: korisnik izabrao opciju A1
   ("Ukloni referencu + obriši oba stara fajla") preko AskUserQuestion gate-a.
```

## Korak 1 — Inventar (read-only, prije instalacije)

```text
OS: Windows (MINGW64_NT-10.0-26300, x86_64)
Korisnik: radovan
HOME: C:\Users\38765
```

Instalirani agenti i verzije:

| Agent | Verzija | Napomena |
|---|---|---|
| Claude Code | 2.1.236 | |
| Codex | — | binarni CLI nije instaliran na ovoj mašini; postoji samo CODEX_HOME config direktorijum |
| Pi | 1.0.2 | |
| Crush | v0.87.0 | |
| OpenCode | 1.18.31 | |
| Cursor | n/a | nema plain-text global rules mehanizam na ovoj mašini (vidi Korak 1b) |

CODEX_HOME = `H:\CodexData\.codex` (env varijabla postavljena, različito od
naivnog defaulta `~/.codex`).

Ciljni globalni fajlovi — stanje PRIJE instalacije (snimljeno iz
`.bak-20261007-094648` kopija, pravljenih neposredno prije prvog upisa):

| Agent | Stvarna putanja | Postojao? | Linije | Bajtovi | sha256 (prije) |
|---|---|---|---|---|---|
| claude-code | `~/.claude/CLAUDE.md` | DA | 21 | 1041 | `bb63a204...90054bd5` |
| codex | `$CODEX_HOME/AGENTS.md` | DA | 6 | 244 | `fed57249...bcdb8243` |
| pi | `~/.pi/agent/APPEND_SYSTEM.md` | DA | 38 | 3352 | `9c4fb84c...66b830ea` |
| crush | `~/.config/crush/CRUSH.md` | DA | 67 | 3028 | `db68bb8b...1aabfce9` |
| opencode | `~/.config/opencode/instructions.md` | DA | 40 | 1877 | `d527cbb8...51f7c3ca` |

### Odstupanja od kontrakta — putanje (korigovane kroz stvarnu inspekciju mašine, ne pretpostavku)

Kontrakt je putanje za Pi/Crush eksplicitno označio UNVERIFIED i tražio da se
"utvrde iz dokumentacije alata na mašini ili iz stvarnog ponašanja, ne
pretpostavkom" (§Korak 1). Stvarne putanje se razlikuju od kontraktovih
pretpostavki:

```text
codex:  kontrakt pretpostavio ~/.codex/AGENTS.md
        stvarno: $CODEX_HOME/AGENTS.md → H:\CodexData\.codex\AGENTS.md
pi:     kontrakt pretpostavio ~/.pi/agent/AGENTS.md
        stvarno: ~/.pi/agent/APPEND_SYSTEM.md
crush:  kontrakt pretpostavio ~/.config/AGENTS.md (generic)
        stvarno: ~/.config/crush/CRUSH.md — generic fajl ne postoji, nije u upotrebi
opencode: nije bio u kontraktu — dodat po korisničkoj odluci u Koraku 0c
```

Nema `AGENTS.override.md` ni za codex ni za pi. Crush `crushrc` ne sadrži
`global_context_paths` override — `~/.config/crush/CRUSH.md` je potvrđeno
stvarni, aktivni globalni fajl.

### Cursor — BLOCKED

Pretraženo `~/.cursor/**` i `AppData/Roaming/Cursor/User/settings.json` —
nema plain-text "User Rules" fajla na ovoj mašini. Marker-block mehanizam ne
može se primijeniti. Cursor ostaje van ovog taska (BLOCKED), ostali agenti
nastavljaju per kontraktovo pravilo ("taj agent ide u BLOCKED za ovaj task,
ostali nastavljaju").

## Korak 2 — Kanonski repo

Struktura kreirana po §3 kontrakta u `~/agent-standard/`:

```text
STANDARD.md            1179 linija, 43378 bajtova, sha256=ced4c845...5b0c09e3a
GLOBAL_ROUTER.md        51 linija,   2361 bajtova, sha256=112e881e...6367e8a3db0
templates/              task-contract-short.md, task-contract-full.md,
                        implementation-report.md, review-report.md,
                        checkpoint.md, agent-standard.yml
install.py
tests/test_install.py
archive/                arhivirane v0.2 datoteke (vidi Korak 1e niže)
```

`GLOBAL_ROUTER.md` je 51 linija / 2361 bajt — unutar granice ≤100
linija/≤6 KiB iz acceptance kriterija. Sadržaj je prepisan verbatim iz
Priloga A kontrakta, bez odstupanja.

### Korak 1e — v0.2/v1.1 koegzistencija (NEEDS_DECISION, riješeno)

Prije instalacije v1.1, `~/.claude/CLAUDE.md` je referencirao stari
`OPSTI_STANDARD_RADA_SA_AI_AGENTIMA.md` (v0.2). Ovo je prijavljeno korisniku
kao Facts-vs-Decision (ne odlučeno samostalno), uz opcije A (ukloni
referencu + obriši stare fajlove) i B (zadrži oboje). Korisnik je izabrao
**A1** preko AskUserQuestion gate-a.

Izvršeno:
- Arhivirane kopije (PRIJE brisanja) u `~/agent-standard/archive/`:
  `OPSTI_STANDARD_RADA_SA_AI_AGENTIMA_v0.2.md` (32560 B),
  `PRIMJENA_NA_NOVI_PROJEKAT_v0.2-companion.md` (6127 B).
- Originali obrisani iz `~/.claude/standards/` (direktorijum ostaje, prazan).
- Sekcija "## Opšti standard rada sa AI agentima" uklonjena iz
  `~/.claude/CLAUDE.md` (Edit tool, prije instalacije markera).

Napomena (I-5 disciplina, samoprijavljeno): arhiviranje NIJE bilo eksplicitno
zatraženo — korisnikova odluka A1 je tražila brisanje bez pomena arhive. Ipak
sam arhivirao prije brisanja kao reverzibilnu mjeru, pošto je potvrđeno da
`~/.claude` NIJE git repo (brisanje bi inače bilo trajno nepovratno). Ovo je
blaža, reverzibilnija verzija zatražene akcije, ne promjena njenog ishoda —
ali se eksplicitno prijavljuje ovdje radi transparentnosti.

## Korak 3 — install.py + testovi + mutaciona provjera

`pytest tests/ -v` → **17 passed** (svježi rerun, exit kod 0, output iznad u
sesiji). Testovi pokrivaju: novi fajl, postojeći fajl bez bloka (i provjera
da nastaje tačno jedan `.bak-*` sa originalnim sadržajem), postojeći fajl sa
starim blokom (replace, idempotentnost), `--check` (match/drift/missing
block/missing file), `--uninstall` (ukloni samo blok / no-op kad nema bloka
ili fajla), CRLF, UTF-8 BOM, dva BEGIN markera (refuses), BEGIN bez END
(refuses).

**Manuelna mutaciona provjera (obavezna po Koraku 3):** privremeno
izmijenjena linija u `plan_for()` iz

```python
new_text = block + "\n\n" + text if text else block + "\n"
```

u

```python
new_text = block + "\n"
```

Rezultat: `test_prepend_block_keeps_existing_content_byte_identical` →
**FAILED** (`AssertionError: assert False` na `new_text.endswith(original)`).
Mutacija vraćena, puni suite ponovo pokrenut → **17/17 PASSED**. Ovim je
dokazano da test stvarno pada ako `install.py` prepiše cijeli fajl umjesto da
sačuva sadržaj van markera — test nije kozmetički.

## Korak 4 — Dry run i STOP gate

`python install.py --dry-run` pokrenut prije bilo kakvog upisa; za svih 5
ciljeva vraćeno `[dry-run] PREPEND-BLOCK <path> (backup first)` jer nijedan
fajl nije imao postojeći marker. Prikazano Human Owneru prije nastavka.
Nastavak autorizovan eksplicitnim "nastavi" korisnika.

## Korak 5 — Instalacija

```text
$ python install.py --install
claude-code: PREPEND-BLOCK C:\Users\38765\.claude\CLAUDE.md (backup: CLAUDE.md.bak-20261007-094648)
codex: PREPEND-BLOCK H:\CodexData\.codex\AGENTS.md (backup: AGENTS.md.bak-20261007-094648) — path resolved via CODEX_HOME env var, not the ~/.codex default
pi: PREPEND-BLOCK C:\Users\38765\.pi\agent\APPEND_SYSTEM.md (backup: APPEND_SYSTEM.md.bak-20261007-094648) — contract assumed AGENTS.md; the real file is APPEND_SYSTEM.md
crush: PREPEND-BLOCK C:\Users\38765\.config\crush\CRUSH.md (backup: CRUSH.md.bak-20261007-094648) — contract also listed ~/.config/AGENTS.md (generic); that file does not exist on this machine and is not used
opencode: PREPEND-BLOCK C:\Users\38765\.config\opencode\instructions.md (backup: instructions.md.bak-20261007-094648) — not in the original contract table; added as a phase-1 target per Korak 0c
```

Backup je napravljen za svih 5 fajlova PRIJE upisa (potvrđeno postojanjem
`.bak-20261007-094648` kopija sa sadržajem identičnim pre-install stanju iz
Koraka 1).

```text
$ python install.py --check
claude-code: OK C:\Users\38765\.claude\CLAUDE.md
codex: OK H:\CodexData\.codex\AGENTS.md
pi: OK C:\Users\38765\.pi\agent\APPEND_SYSTEM.md
crush: OK C:\Users\38765\.config\crush\CRUSH.md
opencode: OK C:\Users\38765\.config\opencode\instructions.md
$ echo $?
0
```

(Napomena: terminal prikazuje `�` umjesto `—` u napomenama zbog
codepage/UTF-8 mismatcha u Git-Bash konzoli na Windowsu — kozmetički problem
samo terminalnog prikaza, ne utiče na sadržaj upisan u fajlove, potvrđeno
diff-om niže.)

### Diff prije/poslije — promjena SAMO unutar markera

Za svih 5 fajlova: `diff -u <backup> <novi>` pokazuje isključivo dodatih 54
linija na vrhu (marker blok), i potvrđeno (`tail`/`grep -F`) da originalni
sadržaj iz backupa postoji netaknut, bajt-za-bajt, kao sufiks novog fajla.

```text
claude-code: PASS — originalni sadržaj (21 linija, "# Globalna korisnička
             uputstva" + Jev sekcija bez v0.2 reference) sačuvan u cjelini
codex:       PASS — originalni Jev-only sadržaj (6 linija) sačuvan u cjelini
pi:          PASS — originalni sadržaj (38 linija: jezik/stil/Jev) sačuvan
crush:       PASS — originalni sadržaj (67 linija) sačuvan
opencode:    PASS — originalni sadržaj (40 linija: radne instrukcije/Jev) sačuvan
```

Nijedan forbidden_path nije diran (nema izmjena u `~/.claude/settings.json`,
`~/.codex/config.toml`, ni u projektnim repoima).

## Korak 6 — Bihevioralna proba (§7)

Proba izvedena STVARNIM one-shot (non-interaktivnim) pozivima svakog CLI-ja
(`claude -p`, `pi --print`, `crush run`, `opencode run`) u praznom
privremenom direktorijumu `/tmp/agent-std-probe-empty` (bez projektnog
AGENTS.md/CLAUDE.md) — jača potvrda nego ručna nova-sesija provjera iz
kontrakta, pošto je ponovljiva i skriptovana. Pitanje:

```text
"Bez čitanja fajlova: koja je invarijanta I-1 iz standarda rada sa agentima,
i gdje se nalazi puni standard? Odgovori kratko."
```

| Agent | Odgovor (doslovno) | Rezultat |
|---|---|---|
| claude-code | "I-1: Implementer nije formalni nezavisni reviewer vlastitog netrivijalnog rada. Puni standard: `~/agent-standard/STANDARD.md`" | **PASS** |
| pi | "I-1: Implementer nije formalni nezavisni reviewer vlastitog netrivijalnog rada. Puni standard: `~/agent-standard/STANDARD.md` (čitaju se samo potrebne sekcije, ne cijeli)." | **PASS** |
| crush | "I-1: Implementer nije formalni nezavisni reviewer vlastitog netrivijalnog rada. Puni standard: `~/agent-standard/STANDARD.md`." | **PASS** |
| opencode | "I-1: Implementer nije formalni nezavisni reviewer vlastitog netrivijalnog rada. Puni standard: `~/agent-standard/STANDARD.md`." | **PASS** |
| codex | nije probano — CLI binarni nije instaliran na ovoj mašini (vidi Korak 1) | **BLOCKED (ne-primjenjivo)** |
| cursor | nije probano — nema mehanizma na ovoj mašini (vidi Korak 1) | **BLOCKED** |

Dodatni kontraktov zahtjev za Claude Code — `/memory` mora prikazati
`~/.claude/CLAUDE.md` kao učitan: **NIJE provjereno u ovoj sesiji.** `/memory`
je UI-only slash komanda i ne radi kroz `claude -p` neinteraktivni mod
(testirano: vraća generički odgovor, ne memory-listing). Sâm tačan
behavioralni odgovor (I-1 + putanja, iz prazne fascikle, bez projektnih
fajlova) je jak indirektan dokaz da je `~/.claude/CLAUDE.md` učitan, ali
formalni `/memory` check zahtijeva ručnu interaktivnu sesiju korisnika.

## Korak 7 — Commit i push kanonskog repoa

```text
$ git init
$ git add .gitignore GLOBAL_ROUTER.md STANDARD.md install.py templates/ tests/ archive/
$ git commit -m "Initial commit: agent-standard v1.1 canonical repo ..."
[master (root-commit) 49afc5d] 13 files changed, 3397 insertions(+)
$ git branch -M main
$ git remote add origin https://github.com/Rade69/agent-standard.git
$ git push -u origin main
 * [new branch]      main -> main
```

Remote je bio prazan prije pusha (`git ls-remote` vratio exit 0, bez
referenci) — nije prepisan ni jedan postojeći sadržaj.

Napomena (I-5/git identitet): ovaj novi repo nije imao git identitet ni
globalno ni lokalno (`fatal: unable to auto-detect email address`). Globalni
git config NIJE mijenjan (zabranjeno). Postavljen je **lokalni** (samo za
ovaj repo) identitet `user.name=Radovan`, `user.email=radovan@agent-standard.local`,
po istoj konvenciji koja već postoji u FlowOS repou (`radovan@flowos.local`)
— nije izmijenjen nijedan postojeći identitet, samo dodat novi za fajl koji
ga nije imao.

`.gitignore` dodat (nije bio u originalnom kontraktovom §3 stablu) da
isključi `.mypy_cache/`, `.pytest_cache/`, `__pycache__/` i `.bak-*` fajlove
iz verzionisanja — cache artefakti i mašinski-specifični backupi ne
pripadaju kanonskom repou koji se distribuira na GitHub.

## Self-check (acceptance kriteriji kontrakta)

```text
[x] ~/agent-standard je git repo, prvi commit 49afc5d, pushovan na
    https://github.com/Rade69/agent-standard (main)
[x] STANDARD.md bajt-identičan priloženom v1.1 (sha256=ced4c845...5b0c09e3a)
[x] GLOBAL_ROUTER.md: 51 linija, 2361 B — unutar ≤100/≤6KiB
[x] pytest tests/ → 17 passed, exit 0 (svježi rerun u ovoj sesiji)
[x] --dry-run pokrenut prije --install (Korak 4)
[x] .bak-<timestamp> postoji za svih 5 fajlova, PRIJE izmjene
[x] --check → exit 0 poslije instalacije (stvaran exit kod, ne kroz pipe)
[x] diff svakog fajla prije/poslije: promjena SAMO unutar markera (5/5 PASS)
[x] bihevioralna proba PASS za claude-code/pi/crush/opencode (4/4);
    codex i cursor eksplicitno BLOCKED sa razlogom (nisu instalirani/nemaju
    mehanizam na ovoj mašini)
[x] nijedan forbidden_path diran
```

## Šta NIJE provjereno

```text
- /memory check za Claude Code (vidi Korak 6) — zahtijeva ručnu
  interaktivnu sesiju, nije izvodljivo kroz claude -p.
- Codex bihevioralna proba — CLI nije instaliran na ovoj mašini; config
  fajl JE instaliran i ispravan (potvrđeno --check), ali live-loading od
  strane Codex agenta nije testiran.
- Ponašanje na Fedora mašini — van scope-a ovog taska (AGENT-STD-020).
- MiniMax — eksplicitno izostavljen po korisničkoj odluci (Korak 0d).
```

## Otvoreni findinzi

```text
- Kozmetički: terminal (Git-Bash na Windowsu) prikazuje em-dash (—) iz
  install.py-jevih note poruka kao � zbog codepage mismatcha. Ne utiče na
  sadržaj fajlova (potvrđeno diff-om). Nije blokirajuće, nije popravljeno
  u ovom tasku (van scope-a — kozmetika stdout-a alata, ne sadržaj koji
  se instalira).
```

## Rollback

```text
python install.py --uninstall   # uklanja samo marker blokove, ostatak netaknut
ili: vratiti .bak-20261007-094648 fajlove preko instaliranih
```

Kanonski repo (`~/agent-standard`) se može ostaviti bez uticaja ako se
blokovi uklone — ne utiče na ništa dok nije instaliran.

## Sljedeći korak

```text
- AGENT-STD-002/003/004 (faza 2: validatori, gitleaks, Claude Code hookovi)
  — van scope-a, zasebni HIGH-risk taskovi.
- AGENT-STD-01x (faza 3: rollout po projektu, redoslijed AI Campaign
  Studio → FlowOS) — van scope-a, zasebni taskovi.
- AGENT-STD-020 (Fedora instalacija) — van scope-a, zaseban task.
- Preporuka: korisnik ručno potvrdi /memory u interaktivnoj Claude Code
  sesiji kad bude zgodno, radi zatvaranja jedinog preostalog NIJE
  provjereno stavka iz Koraka 6.
```
