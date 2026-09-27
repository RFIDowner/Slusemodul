# Slusemodul

Modulær duesluse for PigeonPal: duene går én og én over innebygde 125 kHz RFID-spoler, slik at hver chipring leses sikkert ved hjemkomst. Alle deler printes i PETG på Bambu Lab A1 (maks 256 × 256 × 256 mm).

## Versjoner

| Versjon | Hva | Status |
|---|---|---|
| **v4.2** | **Som v4.1, men 8-kantede gafler som hviler mot karkanten. Terskelstangen er fjernet.** | **Gjeldende – STL og STEP klar** |
| v4.1 | Som v4, men vegger og tak er én hette. To print totalt. | Erstattet av v4.2 |
| v4 | Ett kar (200 mm): forgang med elektronikk + rett spole, gafler, klikk-feste | Erstattet av v4.1 (kar, lokk og gafler er like) |
| v3 | Tre moduler A–M–B med svalehaleskjøt (rett spole + diamantspole) | Erstattet av v4. Modul B er printet. |
| v2 | Ett kar med to spoler og sidekammer | Kun tegning |
| v1 | Første tegning, én diamantspole | Kun tegning |

Hvorfor v4: diamantspolen i v3 er 141 mm lang langs løpet, så to duer kunne stå i lesesonen samtidig. Den rette spolen er 100 mm, og forgangen foran holder neste due utenfor lesesonen.

## v4.2 – gjeldende modell

Som v4.1, med to endringer i utgangen:

- **8-kantede gafler**, 6 mm over flatene, med et rundt øye (Ø9) rundt akselen. De printes liggende på en flate, uten støtte.
- **Karkanten er stopperen.** Akselen står der den var (x = 188, 116 mm over gulvet). Gaflene henger ca. 7° på skrå fra akselen og ut over karets endekant. Endekanten har en skråflate (1,2 mm inn i toppen, 10 mm ned) som gaflene ligger flatt mot. Gaflene går 2 mm lenger ned enn skråflaten. Terskelstangen er fjernet.
- Kontrollert i modellen: gaflene stopper mot karet med en gang de dyttes utover, og kan svinge ca. 80° innover i slaget før de treffer taket.

| Print | Fil | Mål på platen |
|---|---|---|
| 1 | `stl/v4.2/sluse_v4.2_print1_kar_og_gafler.stl` – kar (gulvet ned) + 5 gafler | 200 × 219 × 32 mm |
| 2 | `stl/v4.2/sluse_v4.2_print2_hette_og_lokk.stl` – hette (taket ned) + lokk | 200 × 227 × 133 mm |

Bilder: `tegninger/v4.2/`. Generator: `generator/sluse_v4_2_step.py`.

## v4.1 – vegger og tak som én hette (erstattet av v4.2)

Samme kar, lokk, gafler og terskelstang som v4. Endringen er at begge veggene og taket er smeltet sammen til **én hette**. Den printes opp-ned: taket ligger på platen og veggene står rett opp.

| Print | Fil | Mål på platen |
|---|---|---|
| 1 | `stl/v4.1/sluse_v4.1_print1_kar_og_gafler.stl` – kar (gulvet ned) + 5 gafler + terskelstang | 200 × 224 × 32 mm |
| 2 | `stl/v4.1/sluse_v4.1_print2_hette_og_lokk.stl` – hette (taket ned) + lokk | 200 × 227 × 133 mm |

- Hetta klikkes ned i karet med de samme tre tappene per vegg som i v4. Klikket mellom tak og vegg er borte.
- Veggfoten er 12 mm bred (var 20 mm) med 45° skråkant, slik at den kan printes uten støtte når hetta står opp-ned.
- Hetta er 133 mm høy på en bedslinger. U-formen er stivere enn to løse vegger, men bruk gjerne brim og litt lavere hastighet på yttervegg.
- Delene finnes også hver for seg i `stl/v4.1/` og `step/v4.1/`, og samlet i `step/v4.1/sluse_v4.1_sammenstilling.step`.
- Bilder: `tegninger/v4.1/`. Generator: `generator/sluse_v4_1_step.py`.

Ikke testet på print ennå: klaringene på klikk-tappene. Mothaken på tappene har en 0,9 mm flat kant som blir et lite overheng i print 2, men det er for kort til å trenge støtte.

## v4 – ett kar, løse vegger og tak (erstattet av v4.1)

Ett kar på 200 × 150 mm, gulvet 32 mm over landingsbrettet:
- **Forgang (0–90 mm):** elektronikkammer under gulvet. Lokk fra undersiden med fire M3-skruer og spor for Ø2 silikonsnor. Hull i sideveggen for PG7-kabelnippel.
- **Leser (90–200 mm):** rett 10 × 10 cm-spole i lomme under 4 mm gulv. Spolen presses opp nedenfra, og fire fjærende klikk-neser holder den. Kabelen går inn i kammeret gjennom et hull høyt i skilleveggen.
- **Gafler i utgangen:** fem Ø6 × 116 mm som henger til 3 mm over gulvet mot en terskelstang på slusesiden. De svinger bare innover.
- **Klikk-feste uten skruer:** veggene har tre tapper hver ned gjennom gulvet i spoledelen. Taket klikker inn i et spor på utsiden av veggenes topplist.

| Fil | Innhold |
|---|---|
| `stl/v4/` | Kar, lokk, vegg høyre/venstre, tak, gafler + terskel. Print-orientert, ingen støtte. |
| `step/v4/` | Samme deler i montert posisjon, og `sluse_v4_sammenstilling.step` med alt samlet (inkl. spole og aksel som referanse). |
| `tegninger/v4/` | Bilder av montert modell og undersiden. |
| `generator/sluse_v4_step.py` | Lager alle v4-filene (krever `pip install cadquery`). |

Kjøpedeler: aksel Ø3 × 130 mm rustfri, Ø2 silikonsnor, 4 × M3 × 8 mm skruer til lokket.

Ikke testet på print ennå: klaringene på klikk-festene (standardverdier for PETG) og at klikk-nesene passer spolen (dimensjonert for nøyaktig 100 × 100 mm ytre mål).

Mulig endring senere: la gaflene henge utenfor karets endevegg, slik at karkanten blir stopperen og terskelstangen kan fjernes.

## v3 – tre moduler (erstattet av v4)

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

## Status (v3-deler)

| Del | Status |
|---|---|
| Modul B – kar med diamantlomme | STL klar, testprint pågår |
| Modul B – veggpanel høyre/venstre | STL klar |
| Modul B – takpanel | STL klar |
| Modul B – bobs, stoppstang, sperrelister | ikke laget ennå |
| Hele v3 (A + M + B) som STEP, tre bodies | klar |
| v4 – ett kar, klikk-feste, gafler | STL og STEP klar |
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
