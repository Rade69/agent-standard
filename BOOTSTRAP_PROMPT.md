# Bootstrap prompt — agent sam postavlja standard

Kopiraj blok ispod u svog coding agenta (Claude Code, Codex, Cursor, pi,
crush, OpenCode…), u folderu u kojem želiš da radi. Agent će pročitati
standard, pregledati tvoje okruženje, pokazati plan i **pitati za potvrdu
prije svake izmjene**. Ništa ne pušuje i ne spaja bez tvoje izričite odluke.

Trajanje: 10–20 minuta, zavisno od broja projekata.

---

````text
ZADATAK: Postavi "Standard rada sa AI agentima" na ovom računaru i u mojim projektima.

Izvor standarda: https://github.com/Rade69/agent-standard (STANDARD.md, README.md,
install.py, templates/). Ja sam Human Owner: ja odlučujem; ti predlažeš, izvršavaš
potvrđeno i dokazuješ izvršnim outputom.

Odgovaraj na jeziku na kojem ti pišem.

=== PRAVILA KOJA VAŽE CIJELO VRIJEME ===
- Prije SVAKE izmjene fajla, instalacije ili git operacije pokaži šta tačno radiš
  i čekaj moje "da". Čitanje i dry-run ne traže potvrdu.
- Ne pušuj, ne spajaj i ne briši ništa bez moje izričite odluke za tu konkretnu akciju.
- Tuđe nekomitovane izmjene u projektima ne diraš: ako ih ima, ne radiš u tom
  radnom folderu nego u zasebnom git worktree-u ili na zasebnoj grani.
- Ne pretražuješ cijeli disk: projekte mi navedi ti iz onoga što ti kažem, ili me pitaj.
- Tajne (ključevi, tokeni, lozinke, .env sadržaj) nikad ne ispisuješ, ne kopiraš i ne
  upisuješ u fajlove.
- Ne slabiš postojeća pravila projekta: postojeći AGENTS.md/CLAUDE.md dopunjuješ, ne
  prepisuješ. Ako postojeće pravilo protivrječi invarijantama standarda, prijavi to
  kao nalaz — ne ispravljaj sam.
- "Radi" bez komande, outputa i exit koda nije dokaz. Exit kod uzimaš od prave
  komande, ne kroz pipe.
- Svaku fazu završi kratkim izvještajem i stani.

=== FAZA 1 — IZVIĐANJE (samo čitanje) ===
1. Provjeri da postoje git i Python 3 (verzije).
2. Pitaj me gdje želim kanonsku kopiju standarda (predlog: ~/agent-standard).
   Ako tamo već postoji klon, prijavi granu, verziju iz STANDARD.md i git status.
3. Pročitaj README.md i u STANDARD.md sekcije §19, §0 i §1 (ne cijeli fajl).
4. Pitaj me za listu projekata (putanje) koje treba povezati sa standardom.
   Za svaki projekat utvrdi, samo čitanjem:
   - da li je git repo, trenutna grana, ima li nekomitovanih izmjena,
     da li je lokalna grana ispred origin-a (nepušovani commitovi);
   - postoje li AGENTS.md, CLAUDE.md, .agent-standard.yml i da li već pominju standard i koju verziju;
   - koja je postojeća komanda za lint i testove (pyproject/package.json/Makefile/CI workflow) —
     samo je pronađi, ne izmišljaj je;
   - postoji li CI (npr. .github/workflows).
5. Prikaži nalaze kao tabelu i STANI.

=== FAZA 2 — PLAN ===
1. Kloniraj ili osvježi standard tek poslije moje potvrde, pa pokreni
   `python install.py --dry-run` i pokaži doslovan output: koje globalne fajlove bi
   promijenio (Claude Code, Codex, pi, crush, OpenCode). Alati kojih nema se ne diraju.
2. Za svaki projekat predloži tačno:
   a) blok koji ide na vrh AGENTS.md (ispod prvog naslova; ako AGENTS.md ne postoji,
      novi kratak AGENTS.md sa samo tim blokom i naslovom projekta):

      <!-- AGENT-STANDARD-PROJECT:BEGIN version=<verzija iz STANDARD.md> -->
      ## Standard rada sa AI agentima (v<verzija>)

      Ovaj projekat prati `STANDARD.md` v<verzija> iz repoa agent-standard (lokalno
      `<putanja kanonske kopije>/STANDARD.md`, javno https://github.com/Rade69/agent-standard).
      Standard se ne kopira u repo; projektni override je `.agent-standard.yml`.

      - Invarijante I-1…I-8 važe uvijek. Ovaj projekat ih smije pooštriti, nikad
        oslabiti; ostala projektna pravila imaju prednost gdje su stroža ili konkretnija.
      - Risk po H1–H7 / M1–M4 (§3). Završna stanja: DONE · BLOCKED · NEEDS_DECISION · HANDOFF.
      - Kontekst (§7.3–7.9): u WARNING zoni ne počinji novi veliki podproblem; u HARD
        zoni samo checkpoint + SELF HANDOFF (Prvo uradi / Ne ponavljaj / Pazi na), pa
        kompakcija ili HANDOFF. Procenat konteksta se ne izmišlja. Poslije kompakcije
        ili nove sesije: reorijentacija prije editovanja; stvarni Git ima prednost
        nad checkpointom.
      - Verify komanda (Definition of Done): `<pronađena komanda ili "NIJE DEFINISANA">`
      <!-- AGENT-STANDARD-PROJECT:END -->

      Ako blok sa tim markerima već postoji, zamjenjuješ samo sadržaj između markera.
   b) `.agent-standard.yml` iz templates/agent-standard.yml sa tačnom verzijom
      (ako postoji, mijenjaš samo standard_version);
   c) ako koristim Claude Code: sekciju "Compact Instructions" u CLAUDE.md projekta
      sa instrukcijom iz STANDARD.md §7.7 (pitaj da li je želim);
   d) granu na kojoj radiš (predlog: chore/agent-standard) i da li će se pušovati —
      NE pušuj ako je lokalna grana ispred origin-a, jer bi objavio moje nepušovane commitove.
3. Ako projekat nema verify komandu, predloži je kao preporuku u izvještaju — ne
   dodaj CI i ne mijenjaj build fajlove u ovom zadatku.
4. Prikaži cijeli plan kao listu akcija i STANI.

=== FAZA 3 — GLOBALNO (poslije potvrde) ===
1. `python install.py --install`, zatim `python install.py --check`.
2. Pokaži doslovan output i exit kod obje komande i gdje su backup fajlovi.

=== FAZA 4 — PROJEKTI (svaki projekat posebno potvrđen) ===
Za svaki projekat:
1. Napravi granu (ili worktree, ako ima tuđih nekomitovanih izmjena).
2. Primijeni samo ono što je u planu potvrđeno.
3. Pokaži `git diff --stat` i puni diff. Diff mora biti mali (desetine linija);
   ako je veći, objasni zašto (npr. promjena krajeva redova je greška — popravi je).
4. Commit sa porukom: "docs(agent): standard rada sa AI agentima v<verzija>",
   samo navedeni fajlovi (nikad `git add -A` / `git add .`).
5. Push i pull request samo ako sam to potvrdio za taj projekat.

=== FAZA 5 — IZVJEŠTAJ ===
Završi tabelom: alat/projekat · šta je urađeno · dokaz (komanda + exit kod) ·
šta je preskočeno i zašto · otvoreni nalazi (npr. projekat bez verify komande,
pravilo koje protivrječi invarijantama).
Zatim napiši 3 sljedeća koraka koje JA treba da uradim, npr.:
- pročitati STANDARD.md §0, §1, §3, §4;
- odlučiti ko mi je nezavisni reviewer (druga sesija ili drugi model bez konteksta implementera);
- prvi stvarni task uraditi sa kratkim Task Contractom (templates/task-contract-short.md).
Završno stanje: DONE · BLOCKED · NEEDS_DECISION · HANDOFF, uz razlog.
````

---

## Šta prompt namjerno ne radi

- Ne dodaje CI, ne mijenja build fajlove i ne piše testove: verify komandu samo
  pronalazi ili predlaže.
- Ne prepravlja postojeća pravila projekta, nego samo dodaje blok i prijavljuje
  kontradikcije.
- Ne spaja i ne pušuje bez tvoje odluke za svaki projekat posebno.

Detalji o tome šta smiješ prilagoditi, a šta ne: `STANDARD.md` §19.3.
