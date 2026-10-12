# Context checkpoint (šablon, STANDARD.md Prilog A.4)

```markdown
## CONTEXT CHECKPOINT
### Goal
### Granice (scope / out-of-scope / acceptance / nepromjenljive odluke)
### Urađeno
### Trenutno stanje (HEAD, status, polazni verify)
### Ključne odluke + razlog
### Oborene pretpostavke
### Relevantni fajlovi
### Promijenjeni fajlovi
### Evidence (komanda, rezultat, šta NIJE dokazano)
### Otvoreni findinzi / blokeri
### Sljedeća atomic akcija
### Ne ponavljati (pokušano X → nije radilo jer ...)
### SELF HANDOFF
- Prvo uradi:      jedna konkretna read-only ili atomska akcija
- Ne ponavljaj:    najvažniji oboren pristup
- Pazi na:         glavni otvoreni blocker, finding ili granica ovlaštenja
```

Checkpoint je engineering handoff, ne dnevnik (§7.6). Neprovjerena tvrdnja
nosi oznaku `UNVERIFIED`. Ne pretvara claim u činjenicu, ne skriva otvoreni
finding. Dobar checkpoint je nastavljiv: nova sesija bez starog chata može
potvrditi stanje, ponoviti ključni evidence i imenovati sljedeći korak (§7.8).
Kada se pravi i šta se smije u kojoj zoni konteksta: §7.4–7.5.
