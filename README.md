# Standard rada sa AI agentima

Vendor-neutralan standard za rad sa AI coding agentima — Claude Code, Codex,
Cursor, pi, crush, OpenCode i drugi. Ne zavisi od jednog modela, alata ni
projekta.

> **Model radi. Mehanizam provodi. Evidence potvrđuje. Nezavisni reviewer
> pokušava oboriti rezultat. Čovjek odlučuje.**

Aktuelna verzija: **v1.3** (`STANDARD.md`). Istorija promjena je u Prilogu C.

## Šta dobijaš

- **8 invarijanti** koje nijedan projekat ni task ne može oslabiti (npr.
  implementer ne pregleda sam sebe, tvrdnja nije dokaz, nema merge-a bez
  ljudske odluke).
- **Deterministički risk checklist** (H1–H7, M1–M4) koji određuje koliko
  procesa task treba — LOW, MEDIUM ili HIGH.
- **Task Contract**, **verify gate** kao Definition of Done i **nezavisni
  review** sa jasnim verdiktom.
- **Kontinuitet konteksta**: zone popunjenosti, checkpoint, SELF HANDOFF,
  kompakcija i reorijentacija, da rad preživi promjenu sesije ili modela.
- Šablone za kontrakt, report, review, checkpoint i projektni override.

## Kako početi

1. Pročitaj `STANDARD.md` §19 (usvajanje), zatim §0, §1, §3 i §4.
2. Kloniraj repo na stalnu lokaciju, npr. `~/agent-standard`.
3. Globalni router za svoje agente:
   ```bash
   python install.py --dry-run    # pokaže šta bi se promijenilo
   python install.py --install    # upiše blok i napravi backup
   python install.py --check      # provjeri da je instalirani blok aktuelan
   ```
   Instaler mijenja samo blok između `AGENT-STANDARD` markera; ostatak
   tvojih konfiguracionih fajlova ostaje netaknut.
4. U svaki projekat dodaj kratak blok u `AGENTS.md` koji upućuje na
   standard i verziju, i `.agent-standard.yml` iz `templates/`.

## Sadržaj repoa

| Fajl | Namjena |
|---|---|
| `STANDARD.md` | kanonski standard |
| `GLOBAL_ROUTER.md` | kratak sažetak koji `install.py` upisuje u globalnu konfiguraciju agenata |
| `install.py` | instalacija, provjera i uklanjanje router bloka (samo standardna biblioteka) |
| `templates/` | Task Contract (kratki i puni), implementation i review report, checkpoint, projektni override |
| `archive/` | ranije verzije i kandidati, samo kao istorija |
| `reports/` | izvještaji o implementaciji samog standarda |

## Prilagođavanje

Projekat smije **pooštriti** pravila, nikad ih oslabiti. Šta smiješ
prilagoditi, a šta ne, piše u `STANDARD.md` §19.3.

Jezik standarda je srpski (latinica); tehnički identifikatori su na
engleskom.
