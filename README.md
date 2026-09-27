# Slusemodul

Modulær duesluse for PigeonPal: duene går én og én over innebygde 125 kHz RFID-spoler, slik at hver chipring leses sikkert ved hjemkomst. Alle deler printes i PETG på Bambu Lab A1 (maks 256 × 256 × 256 mm).

## Konsept (v3)

Slusa består av tre moduler som skyves sammen ovenfra med svalehaleskjøt:

| Modul | Lengde | Innhold |
|---|---|---|
| **A** – inngang | 110 mm | Rett 10 × 10 cm-spole, trådene på tvers av løpet |
| **M** – midt | 90 mm | Elektronikkammer under gulvet (PigeonPal-PCB + to lesermoduler), lokk fra undersiden |
| **B** – utgang | 150 mm | Diamantspole (dreid 45°) + bobs som bare svinger innover |

- Løpet er 110 mm innvendig bredde og 120 mm åpningshøyde. Gulvet ligger 32 mm over landingsbrettet.
- Vegger og tak er spiler, så slusa er gjennomsiktig og ikke oppleves som en tunnel.
- De to spolene har ulik orientering (rett og diamant), så de feiler på forskjellige ringvinkler. Det gir reell redundans, ikke bare dobbelt opp.
- Rekkefølgen A → B gir retning. Firmware dedupliserer samme chip-ID fra begge portene (J3/J4).
- Elektronikken ligger i en modul uten spole, minst ca. 5 cm fra nærmeste vikling.

Bakgrunnen for høydevalget (ring 9–14 mm over viklingen, ikke 5–10 cm) står i [`analyse/coil-hoyde-rapport.md`](analyse/coil-hoyde-rapport.md).

## Status

| Del | Status |
|---|---|
| Modul B – kar med diamantlomme | STL klar, testprint pågår |
| Modul B – veggpanel høyre/venstre | STL klar |
| Modul B – takpanel | STL klar |
| Modul B – bobs, stoppstang, sperrelister | ikke laget ennå |
| Hele v3 (A + M + B) som STEP, tre bodies | klar |
| Modul A og M – printbare delfiler | ikke laget ennå |
| Klikk-/snapp-feste i stedet for skruer | planlagt |

## Mapper

- `stl/modul_B/` – ferdige STL-filer, allerede lagt i print-orientering (ingen støtte).
- `step/` – STEP-filer til Fusion, i montert posisjon:
  - `sluse_v3_komplett_3_bodies.step` – hele slusa, der A, M og B er hver sin body (kar, vegger og tak smeltet sammen per modul).
  - `sluse_v3_modul_*.step` – én modul per fil.
  - `step/modul_B/` – modul B delt opp i de fire delene som printes (kar, vegg høyre/venstre, tak), og en sammenstilling.
- `generator/` – Python-skript som lager STL-ene. Alle mål er parametre øverst i hver fil.
- `tegninger/v1…v3/` – tekniske tegninger (SVG/PNG) og skriptene som lager dem.
- `analyse/` – rapport om spolehøyde og lesesikkerhet, med Biot–Savart-modellen av spolen.

## Lage STL på nytt

```bash
pip install manifold3d numpy
python generator/modul_B_kar.py
python generator/modul_B_vegg.py
python generator/modul_B_tak.py
```

STL-ene skrives til `stl/modul_B/`. STEP-filene lages med `generator/modul_B_step.py` og `generator/sluse_v3_step.py` (krever `pip install cadquery`). Forhåndsvisninger (SVG) havner i samme mappe, men holdes utenfor git.

## STEP i Fusion

- **Som eget design:** File → Open → Open from my computer → velg `.step`.
- **Inn i et design du jobber med:** last opp filen i Data Panel, høyreklikk den og velg **Insert into Current Design**.
- Modellene kommer inn som solider uten parametre. Bruk Press/Pull, skisser og Combine for å endre dem.

## Print-innstillinger (PETG, A1)

- 0,20–0,28 mm lag, 2 vegger, 10–15 % infill.
- Skjørt, ikke brim.
- Ingen støtte: alle deler er orientert slik at hulrom og lommer åpner oppover.
- Legg inn raskere hastigheter enn Generic PETG-profilen, for eksempel yttervegg 120 mm/s og indre vegg 200 mm/s.

## Kjøpedeler

- Bobs-aksel: Ø3 × 150 mm, rustfri eller messing. Ikke vanlig stål nær spolene.
- Treskruer 3,5 × 25 mm til veggføtter og feste mot landingsbrettet.
- Skruer 3 × 12 mm til takpanel.
- Kabelnippel eller Ø2 silikonsnor til pakning i modul M.
