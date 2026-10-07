---
title: "Primjena Opšteg standarda na novi/postojeći projekat"
purpose: "Kratak, project-agnostic vodič — kako da svaki projekat Human Ownera počne koristiti OPSTI_STANDARD_RADA_SA_AI_AGENTIMA.md, bez da se on kopira ili prepravlja po repou."
companion_to: "OPSTI_STANDARD_RADA_SA_AI_AGENTIMA.md (isti direktorijum)"
date: "2026-09-23"
---

# Primjena Opšteg standarda na novi/postojeći projekat

Ovaj fajl odgovara na jedno pitanje: **"Imam standard, imam novi/postojeći
projekat — kako da ga stvarno počnem koristiti tamo?"**

Standard sam po sebi (`OPSTI_STANDARD_RADA_SA_AI_AGENTIMA.md`) živi
**globalno, van svakog repoa** (`~/.claude/standards/`), baš da se ne
kopira i ne rasklapa po svakom projektu ponaosob — jedan izvor istine,
svaki projekat mu se referencira.

## Korak 0 — Da li projekat već ima svoj proces?

**Ima** (npr. `AGENTS.md`/`CLAUDE.md`/`docs/*_WORKFLOW.md` sa risk-tier
pravilima, Task Contract obrascem itd.):

→ NE prepisivati taj dokument. Dodati kratku sekciju-pokazivač na standard,
sa jasnim pravilom prvenstva — vidi Korak 2. Projektna pravila koja su
STROŽIJA ili KONKRETNIJA uvijek pobjeđuju (standard §1.2 to sam kaže).

**Nema** (nov projekat, ili postojeći bez formalizovanog procesa):

→ Standard postaje efektivni default odmah. Projektu treba samo tanak
`AGENTS.md` router (vidi Korak 1) — ne treba pisati vlastiti 30-sekcijski
dokument od nule.

## Korak 1 — Tanak router fajl (`AGENTS.md` ili ekvivalent)

Svaki projekat treba MALI ulazni fajl koji agent pročita prvi, čak i ako
sve ostalo dolazi iz globalnog standarda:

```markdown
# AGENTS.md — <Projekat>

1. Pročitaj `~/.claude/standards/OPSTI_STANDARD_RADA_SA_AI_AGENTIMA.md`
   (globalni proces — uloge, risk tier, Task Contract, context strategy,
   verification, review).
2. Pročitaj ovaj fajl za PROJEKAT-SPECIFIČNE dopune/izuzetke ispod.
3. Pročitaj `.agent/CURRENT_STATE.md` (ako postoji) ili ekvivalentan
   living-status fajl.
4. Pročitaj konkretan Task Contract prije koda.

## Projekat-specifične dopune

<ovdje ide SAMO ono što je različito ili dodatno od standarda — ne
ponavljati ono što standard već kaže>
```

Ovo je isti "thin router" princip koji AI Campaign Studio već koristi za
sopstveni `AGENTS.md` (samo umjesto da sav sadržaj bude lokalni, veći dio
sada dolazi iz globalnog standarda).

## Korak 2 — Mapiraj uloge na STVARNE agente tog projekta

Standard govori o ulogama (Coordinator/Implementer/Reviewer/Integrator),
ne o konkretnim imenima. Svaki projekat ima drugačiji raspoloživi set
alata. Napiši eksplicitnu tabelu u router fajlu:

```markdown
| Uloga | Ko na OVOM projektu |
|---|---|
| Coordinator | ... |
| Implementer | ... |
| Reviewer (adversarial) | ... (ili: "nema drugog agenta -- Human Owner
  radi drugi pregled ručno, vidi napomenu niže") |
```

**Ako projekat nema drugog agenta za nezavisan review** — to je legitimno
stanje, ali standard §2.1 i dalje traži da implementer ne recenzira
sopstveni netrivijalan rad. Rješenje bez drugog agenta: Human Owner radi
taj drugi pregled sam (bar za MEDIUM/HIGH), ili se HIGH taskovi na tom
projektu svjesno rjeđe rade dok se ne nabavi drugi reviewer. Ne
preskakati review korak samo zato što je alat nedostupan — to je isti
princip kao "Codex privremeno nedostupan → Human Owner bira zamjenu po
tasku" iz AI Campaign Studio prakse, ne "review se ne radi".

## Korak 3 — Podesi risk-tier PRAGOVE veličini projekta

Standard §4 daje OPŠTE kriterijume (migracija, security, shared contract
→ HIGH). Ono što svaki projekat mora sam odlučiti je **koliko HIGH
poslova zaista postoji** i da li LOW/MEDIUM sme imati skraćenu putanju
(jedan nezavisan pregled → odmah merge, bez posebnog čovjek-odobrenja po
tasku — AI Campaign Studio ovo zove "§29").

Solo hobby projekat bez pravih korisnika/podataka razumno ima ŠIRU
LOW/MEDIUM zonu i užu HIGH zonu nego projekat sa pravim korisnicima,
platnim podacima ili produkcijskom bazom. Ovo je Human Owner odluka po
projektu, ne nešto što se izvodi automatski iz standarda.

## Korak 4 — Ne uvoditi sve mehanizme odjednom

Isto pravilo kao i za bilo koji drugi alat/proces (vidi
`GRAFT_ADOPTION_PLAYBOOK.md` za identičnu lekciju primijenjenu na
code-intelligence alat): **big-bang usvajanje cijelog standarda odjednom,
retroaktivno na cio postojeći projekat, je greška.** Umjesto toga:

1. Odaberi 3-4 mehanizma sa najvećom polugom ZA TAJ projekat (ne moraju
   biti isti kao na drugom projektu — npr. projekat koji često mijenja
   agenta/sesiju će najviše profitirati od Context Checkpoint-a §7 i
   Reorientation Check-a §8.2; projekat sa čestim paralelnim radom
   najviše od Conflict taksonomije §10.2).
2. Primijeni ih počev od SLJEDEĆEG stvarnog taska, ne retroaktivno.
3. Poslije 5-10 taskova (standard §23 pilot princip), odluči šta ostaje
   standardna praksa, šta se prilagođava, šta se odbacuje kao suvišno za
   taj projekat.

## Korak 5 — Zabranjeni obrazac koji vrijedi svugdje

Standard §9 i §28 imaju jedno pravilo koje je vrijedno ponoviti u SVAKOM
projektu bez izuzetka, jer je uzrok stvarne, dokumentovane greške u
najmanje jednom projektu Human Ownera:

> **Tool self-report (npr. "X tokena ušteđeno") nije projektni evidence.**
> Nikad ga ne prenositi korisniku kao provjerenu činjenicu bez unakrsne
> provjere protiv stvarnog mjerila tog alata.

## Kontrolna lista za brzi start na novom projektu

```text
[ ] Router fajl (AGENTS.md ili ekvivalent) postoji i pokazuje na
    ~/.claude/standards/OPSTI_STANDARD_RADA_SA_AI_AGENTIMA.md
[ ] Tabela uloga → stvarni agenti tog projekta napisana
[ ] Risk-tier pragovi (šta je LOW/MEDIUM/HIGH ZA OVAJ projekat) odlučeni
    od strane Human Ownera, ne pretpostavljeni
[ ] Living-status fajl (CURRENT_STATE.md ili ekvivalent) postoji ili je
    planiran
[ ] Task Contract template dogovoren (može biti standardov §5.1 obrazac
    doslovno, ne treba izmišljati novi)
[ ] 3-4 mehanizma sa najvećom polugom identifikovana za PRVI pilot
[ ] Prvi sljedeći task koristi novi proces -- ne retroaktivna primjena
```
