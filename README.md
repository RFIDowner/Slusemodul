# Slusemodul

Modulær duesluse for PigeonPal: duene går én og én over innebygde 125 kHz RFID-spoler, slik at hver chipring leses sikkert ved hjemkomst. Alle deler printes i PETG på Bambu Lab A1 (maks 256 × 256 × 256 mm).

## Versjoner

| Versjon | Hva | Status |
|---|---|---|
| **v7.4** | **Som v7.3, men sporet for leseren under gulvet er 1,5 mm høyere (3 mm)** | **Gjeldende – STL og STEP klar, ikke printet** |
| v7.3 | Som v7.2, men én avstiver per side i stedet for kryss (den fra foten av første stolpe) | Erstattet av v7.4 (bare leserholderen i plinten er endret) |
| v7.2 | Som v7.1, med fem fanggafler ved utgangen: rett gavl med overligger i siste takstol, tverrstang i ører på toppramma, gafler med nøkkelhull-nav | Erstattet av v7.3 (bare avstiverne er endret) |
| v7.1 | Som v7, med hel yttervegg ved avstemmingskortet og fire festeører med skruehull | Erstattet av v7.2 (plint, skuff og splinter er like) |
| v7 | To deler: plint (bunn med el-rom og spolelomme) og hette (fire takstoler med kryss) som står i hull i plinten. Fire splinter. Ingen støtte i printen | Erstattet av v7.1 (hull rett ut i −y-veggen ved slaget) |
| v6 | Ett stykke: Stigs sluse med spisse portaler, forgang med el-rom under gulvet, ribber, spole i lomme, skuff fra siden | Erstattet av v7 (krevde støtte under hele gulvet) |
| v5 | Skuff-lokk uten lange spor, kroker og trykknapper for hetta, tak som flygende due, dobbel spileavstand | Erstattet av v6 (to deler, kar + hette) |
| v4.3 | Kabelføring, kortfeste, skyvelokk løftet 4 mm, leser i tørt rom, gafler med nav | Erstattet av v5 (gafler og kortfeste er like) |
| v4.2 | Som v4.1, men 8-kantede gafler som hviler mot karkanten. Terskelstangen er fjernet. | Erstattet av v4.3. Karet er printet. |
| v4.1 | Som v4, men vegger og tak er én hette. To print totalt. | Erstattet av v4.2 |
| v4 | Ett kar (200 mm): forgang med elektronikk + rett spole, gafler, klikk-feste | Erstattet av v4.1 (kar, lokk og gafler er like) |
| v3 | Tre moduler A–M–B med svalehaleskjøt (rett spole + diamantspole) | Erstattet av v4. Modul B er printet. |
| v2 | Ett kar med to spoler og sidekammer | Kun tegning |
| v1 | Første tegning, én diamantspole | Kun tegning |

Hvorfor v4: diamantspolen i v3 er 141 mm lang langs løpet, så to duer kunne stå i lesesonen samtidig. Den rette spolen er 100 mm, og forgangen foran holder neste due utenfor lesesonen.

## v7.4 – gjeldende modell

Som v7.3, med én endring: **sporet for leseren** i leserholderen under gulvet er 1,5 mm høyere. Stig fant at det var for tett mellom gulvet og de to leppene. Sporet er nå 3,0 mm høyt (v7.3: 1,5 = leser 1,0 + 0,5). Leppene er fortsatt 1 mm, så skinnene går 1,5 mm lenger ned, til z 24 (kortets overside er z 21). Bredden er uendret. Hette, skuff, splinter og gafler er uendret.

| Print | Fil | Mål på platen |
|---|---|---|
| 1 | `stl/v7.4/sluse_v7.4_print1_plint_lokk_splinter.stl` – plint (gulvet ned) + skuff + 4 splinter | 246 × 221 × 32 mm |
| 2 | `stl/v7.4/sluse_v7.4_hette.stl` – hette (toppramma, ørene og tverrstangen ned, brim) | 184 × 126 × 187 mm |
| 3 | `stl/v7.4/sluse_v7.4_print3_gafler.stl` – 5 gafler, flatt | 164 × 130 × 15 mm |

Sammenstillingen `step/v7.4/sluse_v7.4_sammenstilling.step`, delene i `step/v7.4/`, bilder i `tegninger/v7.4/` (`sluse_v7.4_leserholder.png` er et snitt gjennom holderen), laget av `generator/render_v7_4.py`. Generator: `generator/sluse_v7_4_step.py`.

## v7.3 (erstattet av v7.4)

Som v7.2, med én endring etter Stigs ønske: kryssene i sideveggene er borte. Hver side har nå **én avstiver** 4 × 4 mm på 45°, den som er festet i foten av første stolpe (ved inngangen, x 6,6) og går opp gjennom de to mellomstolpene inn i toppramma ved siste takstol (x 169,6). Avstiveren fra foten av siste stolpe er fjernet. Plint, skuff, splinter og gafler er uendret.

Én diagonal holder veggen like stiv mot skjevhet som et kryss (den tar strekk den ene veien og trykk den andre), men den er alene om det. Hetta er 166 cm³ (v7.2: 172).

| Print | Fil | Mål på platen |
|---|---|---|
| 1 | `stl/v7.3/sluse_v7.3_print1_plint_lokk_splinter.stl` – plint (gulvet ned) + skuff + 4 splinter | 246 × 221 × 32 mm |
| 2 | `stl/v7.3/sluse_v7.3_hette.stl` – hette (toppramma, ørene og tverrstangen ned, brim) | 184 × 126 × 187 mm |
| 3 | `stl/v7.3/sluse_v7.3_print3_gafler.stl` – 5 gafler, flatt | 164 × 130 × 15 mm |

Sammenstillingen `step/v7.3/sluse_v7.3_sammenstilling.step`, delene i `step/v7.3/`, bilder i `tegninger/v7.3/` (`sluse_v7.3_side.png` viser avstiveren), laget av `generator/render_v7_3.py`. Generator: `generator/sluse_v7_3_step.py`. Mål og begrunnelser for gaflene står under v7.2.

## v7.2 (erstattet av v7.3)

Som v7.1, med fanggafler ved utgangen etter Stigs forslag. Plinten, skuffen og splintene er uendret.

- **Siste takstol har rett gavl.** Døra er et rektangel 116 × 113 mm (høyden er holdt). Over den ligger en overligger, 3 mm høy, som stikker 4 mm ut mot slaget (til x 173) og har 45° skrå oppover på begge sider. Gavlplata over er 4 mm som før, men rett helt opp til toppramma. Overliggeren er stopperen for gaflene.
- **Ører og tverrstang.** Toppramma (5 × 10 mm) er forlenget 13,5 mm forbi siste takstol på begge sider, til x 185,5. Mellom ørene ligger en tverrstang 6 × 8 mm (6 langs løpet, 8 høy) med 1,5 mm fas på hjørnene, oversiden i flukt med toppen av hetta. Hetta printes på hodet, så stangen ligger med en 3 mm flate rett på plata, som toppramma. Ingen bro, ingen støtte. Hetta blir 184 mm lang på plata.
- **Fem gafler** henger fra tverrstangen rett bak siste takstol: 8-kant stang 6 mm (som v4.3), 157 mm fra navsenter til tupp, tuppen 3 mm over gulvet. Hver gaffel hviler av egen tyngde mot overliggerens ytterkant, 1,3° inn i slaget. En due fra løpet dytter gaffelen inn i slaget, den svinger fritt. En due fra slaget presser gaffelen mot overliggeren, den står fast.
- **Nøkkelhull-nav.** Navet er 22 × 13 mm med en spiss på 8,5 mm mot slaget. Hullet er en 8-kant med 45° tak (inskrevet radius 4,57, 0,3 mm klaring til stangens hjørner), og en slisse 6,3 mm bred ut mot gavlen. Tverrstangen (6 tynn, 8 høy) går bare gjennom slissen når gaffelen peker vannrett inn i slaget: hold gaffelen vannrett, senk navet over stangen, slipp. Hengende, og i hele svingen, står stangens 8 mm på tvers av slissen, så gaffelen kan ikke falle av. Av igjen: løft gaffelen til vannrett og dra opp. Ingen fjæring.
- **Avstand.** Navene er 22 mm lange med 22,5 mm deling, så de fem navene fyller 112 av 116 mm mellom ørene og holder avstanden selv (0,5 mm luft mellom hvert, 2 mm til ørene). Gaflene står ved y 0, ±22,5, ±45; ytterste gaffel 10 mm fra beinet. Navet går klar av gavlplata med 3 mm i ro og 1,3 mm når gaffelen svinger.
- **Print.** Gaflene printes liggende på siden mot gavlen: navets to føtter ved slissen og stangens flate ligger på plata, taket over hullet er 45°. Fem i ett print.

| Print | Fil | Mål på platen |
|---|---|---|
| 1 | `stl/v7.2/sluse_v7.2_print1_plint_lokk_splinter.stl` – plint (gulvet ned) + skuff + 4 splinter | 246 × 221 × 32 mm |
| 2 | `stl/v7.2/sluse_v7.2_hette.stl` – hette (toppramma, ørene og tverrstangen ned, brim) | 184 × 126 × 187 mm |
| 3 | `stl/v7.2/sluse_v7.2_print3_gafler.stl` – 5 gafler, flatt | 164 × 130 × 15 mm |

Hette 172 cm³ (v7.1: 151), gaffel 5,9 cm³ hver. Sammenstillingen `step/v7.2/sluse_v7.2_sammenstilling.step`, delene i `step/v7.2/` (`sluse_v7.2_gaffel.step` er den midterste gaffelen i montert stilling). Bilder i `tegninger/v7.2/` (nye: `sluse_v7.2_gaffel*.png`, `sluse_v7.2_hette_print_stang.png`), laget av `generator/render_v7_2.py`. Generator: `generator/sluse_v7_2_step.py`.

Ikke testet på print ennå: tverrstangens 3 mm flate i første lag, nøkkelhullets 0,3 mm klaring, om 1,3° helling er nok til at gaflene alltid faller tilbake mot overliggeren.

## v7.1 (erstattet av v7.2)

Som v7, med to endringer. Hetta, skuffen og splintene er uendret.

- **Hel yttervegg ved avstemmingskortet.** I v7 gikk vinduet for spolens avstemmingskort (x 176..208, 8 mm høyt) tvers gjennom −y-veggen, så det ble et 32 × 8 mm hull rett ut. Nå er det en utsparing på innsiden, og ytterveggen er hel med 2,4 mm. Kortet har 10,9 mm plass ved siden av spolelomma (v6: 11,9).
- **Festeører:** to på hver kortside, i hjørnene, flate mot landingsbrettet. Hvert øre stikker 17 mm ut og er 16 mm bredt, ytterkanten flukter med langsiden. Skruehullet er 10 mm fra plintkanten: Ø4 gjennom en 6 mm flens, senket 90° til Ø8 for treskrue 3,5 mm. Over flensen er en kile på 45° tilbake til veggen, med Ø8 boring for skrutrekkeren, så øret printes uten støtte. Skrue 3,5 × 25 gir ca. 20 mm i treverket. Ørene ligger på x −17..0 og 212..229; x 0 er fortsatt plintkanten ved inngangen.

| Print | Fil | Mål på platen |
|---|---|---|
| 1 | `stl/v7.1/sluse_v7.1_print1_plint_lokk_splinter.stl` – plint (gulvet ned) + skuff + 4 splinter | 246 × 221 × 32 mm |
| 2 | `stl/v7.1/sluse_v7.1_hette.stl` – hette (toppramma ned, brim) | 170 × 126 × 187 mm |

Print 1 har bare 10 mm til overs på A1-platen langs x, så det er lite rom for brim der. Plint 184 cm³. Sammenstillingen `step/v7.1/sluse_v7.1_sammenstilling.step`, delene i `step/v7.1/`. Bilder i `tegninger/v7.1/` (nytt: `sluse_v7.1_oere.png`), laget av `generator/render_v7_1.py`. Generator: `generator/sluse_v7_1_step.py`.

## v7 (erstattet av v7.1)

v6 delt i to etter Stigs forslag: stolpene i hetta går rett ned i hull i plinten, så ingen klips eller fjærer trengs. Begge delene printes uten støtte.

- **Plinten** er v6 sin bunn: gulvplate 212 × 128 mm, 32 mm høy, el-rom under forgangen, skillevegg, spolelomme under karet, skuff fra −y-siden. Innenfor hver langsidevegg står en kloss under hver stolpe (åtte i alt), 13,4 mm lang og 7 mm inn fra veggen. I klossen er stolpehullet: 10,4 × 3,9 mm, 22 mm dypt fra gulvflaten, 0,5 mm skrå i kanten, 3 mm hull videre ned. Klossene i forgangen henger fra gulvet og stopper 8,5 mm over brettet, så skuffen går under. Printes med gulvet ned; el-rom og spolelomme er da åpne oppover.
- **Hetta** er fire like takstoler med samme spisse døråpning som v6 (116 bred, rette sider til 113, topp 158, 38°), jevnt fordelt fra x 1,6 til 172 med 43,5 mm lysåpning, bundet av en toppramme 5 × 10 mm langs hver langside. Beina er 10 mm tykke langs løpet og 5 mm brede på tvers, helt opp til toppen; gavlen over døråpningen mellom dem er 4 mm. Tappen er de midterste 3,5 mm av beinet og går 22 mm ned i hullet, klaring 0,2 mm per side. Hetta er 126 mm bred, så plintkanten stikker 1 mm utenfor. Et kryss av to avstivere 4 × 4 mm på 45° per side: hver går fra foten av en endestolpe, gjennom de to mellomstolpene (82 og 136 mm over gulvet), og inn i toppramma ved den andre endestolpen; de møtes midt i åpningen mellom stolpe 2 og 3. Ingen spiler, ingen bunnlist. Stig vet at duene får hodet inn mellom stolpene; 43 mm er nær det duefeller bruker mellom «bobs», så dette skal ses an på print. Printes med toppramma ned, 187 mm høy, med brim, uten overheng utover krysset på 45°.
- **Feste:** 4,2 mm vannrett hull gjennom plintvegg, kloss og stolpe ved første og siste takstol, begge sider. En printet splint (4 mm pinne med hode, slisset på langs, to tunger med 0,4 mm mothake som klikker bak klossen, tøyning 0,7 %) i hvert hull. M4 med mutter passer i samme hull. Montering: sett hetta rett ned, fire splinter inn. Løsne: dra splintene ut.
- **Flyttet for å gi plass til klossene:** leseren ligger 8 mm lenger inn fra −y-veggen (y −52..−37), strømkabelslissen i skilleveggen ved y −30..−25, spolens −y-nese ved x 128 og vinduet for avstemmingskortet ved x 176..208.
- **Skuffen** som v6.

| Print | Fil | Mål på platen |
|---|---|---|
| 1 | `stl/v7/sluse_v7_print1_plint_lokk_splinter.stl` – plint (gulvet ned) + skuff + 4 splinter | 212 × 221 × 32 mm |
| 2 | `stl/v7/sluse_v7_hette.stl` – hette (toppramma ned, brim) | 170 × 126 × 187 mm |

Ingen støtte i noen av printene. Plint 169 cm³, hette 151 cm³ (massivt volum; sliceren med to skall og 15 % fyll gir mindre i plast). Sammenstillingen `step/v7/sluse_v7_sammenstilling.step` (med kort, leser og spole som referanse), delene i `step/v7/`. Bilder i `tegninger/v7/`, laget av `generator/render_v7.py`. Generator: `generator/sluse_v7_step.py`.

Ikke testet på print ennå: 0,2 mm klaring i hullene, 165 mm frie stolper på 10 × 5 mm i printen (krysset binder dem for hver 50 mm langs løpet, ikke på tvers), splintens mothake.

## v6 (erstattet av v7)

Utgangspunktet er Stigs ett-stykks sluse «nyeste antenne løsning» (`stl/v5/`): kar 128 × 120 mm med spiss døråpning i begge ender og spiler i veggen. v6 beholder prinsippet, ett stykke printet stående, og legger til det v5 hadde under gulvet.

- **Gulvplate 212 × 128 mm,** 32 mm over brettet, flat hele veien. Forgang x 0..88 med el-rom under, skillevegg, kar 90..212 med spolelommen under gulvet (6 mm dyp, fire fjærende felt med klikk-nese, som v4.3). De siste 40 mm av gulvet mot slaget har ingen vegger.
- **Fire ribber over forgangen,** 4 mm tykke, hver med spiss døråpning innvendig og flat topp, 17 mm åpning mellom. En toppramme, bjelke langs hver langside bundet av ribbe 1 og portalene, binder dem. Hvert mellomrom i veggene, mellom ribber og mellom spiler, har spiss topp med samme 38° som døråpningen. Ingen broer i modellen.
- **Portaler** ved x 88 og 168 med samme døråpning: 116 mm bred, rette sider til 113 mm, topp i 158, vegghøyde 165. Buen er to rette linjer med 38° fra vannrett, så den printes uten støtte. Vinkelen er én parameter i generatoren.
- **Karets sidevegger** har to spiler à 10 mm med 18 mm åpning, bunnbånd og toppbånd 12 mm.
- **El-rom** 28 mm høyt: kort på tre tapper og to kroker, komponentsiden ned. Leserholder ved skilleveggen med 1,5 mm bredere og 0,2 mm høyere spor enn v4.3. Spoletråder og strømkabel gjennom slisser i skilleveggen (Sika).
- **Skuffen** skyves inn fra −y-siden, kortsiden først, 4 mm over brettet, mellom fire kiler og fire stoppere på endeveggen og skilleveggen. Tunge i kanten ved åpningen med 2 mm nese som klikker opp bak veggkanten, usynlig utenfra. Åpne: negl eller kniv i hakket under tungen, dra ned, trekk ut. Ingen fingerhull. Tre dreneringsslisser.
- Ingen gafler i v6 ennå. Festeører kommer i en senere versjon.

| Print | Fil | Mål på platen |
|---|---|---|
| 1 | `stl/v6/sluse_v6_print_kar_og_lokk.stl` – kar stående + lokk flatt ved siden av | 212 × 221 × 197 mm |

Støtte i printen: under hele gulvet (el-rom og spolelomme), trekkes ut nedenfra. Ingen andre steder. Karet er 371 cm³, rundt 470 g PETG.

Sammenstillingen `step/v6/sluse_v6_sammenstilling.step` (med kort, leser og spole som referanse). Bilder i `tegninger/v6/`, laget av `generator/render_v6.py`. Generator: `generator/sluse_v6_step.py` (krever `pip install cadquery`).

Ikke testet på print ennå: buen på 38° i PETG, lokktungen (nese 2 mm, holder 0,7 mm), og at støtten under gulvet lar seg trekke ut uten å skade klikk-nesene for spolen.

## v5 (erstattet av v6)

Printproblemene i v4.3 er borte: spalten for lokket ga en 145 mm bro i karprinten, veggtappene var for korte og stive (ca. 8 % tøyning) og sto på tvers av lagene, og rennene og slissene lå i første lag mot platen. I v5 ligger alle fjærer i printplanet med tøyning under 1 %, og ingenting ligger i første lag.

- **Skuffen (lokket)** skyves inn fra inngangsenden som før, 4 mm over brettet, så slusa kan stå montert. Endeveggen er åpen under lokket, så det finnes ingen spalte. Fire korte kiler under og fire stoppere over (15 mm hver, i sideveggene) fører lokket. Bakerst i lokket er en tunge (2 mm tykk, 20 mm lang) som fjærer ned, med nese som klikker bak en kloss under gulvet når lokket er helt inne. Åpne: finger i hullet i tungen, dra ned, skyv ut. Ingen pakning, ingen skruer.
- **Hetta** har ingen tapper gjennom gulvet, og karet har ingen renner. Ved inngangen henger en L-krok per vegg ned på utsiden av endeveggen, med nese i et hakk (utenfor løpet). Ved slaget henger en flik med vindu per vegg, og en vannrett fjærbjelke i karets endevegg (to slisser) klikker ut gjennom vinduet. Montering: hekt inngangsenden, senk slagenden til det klikker. Løsne: trykk de to knappene bak på karet inn, og løft.
- **Taket** er ramme (to skinner og to tverrstykker) med en flygende due i midten og fire fjærlinjer. Største åpning 29 mm, målt som største innskrevne sirkel. Generatoren sjekker at ingen åpning er over 32 mm.
- **Spiler:** 4 à 10 mm per vegg, 28,8 mm lysåpning (v4.3: 7 à 8 mm, 16 mm).
- Uendret: gafler med nav, aksel, kortfeste, leserholder, spoleneser, kabelslisser i skilleveggen, strømkabel under sideveggen.

| Print | Fil | Mål på platen |
|---|---|---|
| 1 | `stl/v5/sluse_v5_print1_kar_og_gafler.stl` – kar (gulvet ned) + 5 gafler | 201 × 239 × 32 mm |
| 2 | `stl/v5/sluse_v5_print2_hette_og_lokk.stl` – hette (taket ned, kroker og fliker øverst) + lokk (undersiden ned, nesen opp) | 206 × 230 × 148 mm |

Sammenstillingen `step/v5/sluse_v5_sammenstilling.step` (med kort, leser, spole og aksel som referanse), delene hver for seg i `step/v5/` og `stl/v5/`. Bilder i `tegninger/v5/`, laget av `generator/render_v5.py`. Generator: `generator/sluse_v5_step.py` (krever `pip install cadquery shapely`).

Ikke testet på print ennå: klaringene krok/hakk (0,3 mm) og flik/knapp (0,4 mm), og at lokktungen klikker med passe kraft (nesen er 1,6 mm høy, klossen holder 0,7 mm). Duesilhuetten er et første utkast og kan byttes fritt, generatoren måler åpningene på nytt.

## v4.3 (erstattet av v5)

Erfaring fra v4.2-printen: klikk-nesene som holder spolen er perfekte og er uendret. Endringene:

- **Lokket** under el-rommet er løftet 4 mm over brettet, så det aldri står i vann. Det skyves inn fra inngangsenden i spor (kile under og skinne over, begge med 45° så de printes uten støtte) og låses med en klikk-tunge bak endeveggen. Fingerhull Ø7 i tungen: løft tungen og dra. Tre dreneringsslisser ved skilleveggen. Ingen skruer, ingen pakning.
- **Leseren** (35 × 15 × 1 mm) sitter i tørt rom, i en holder i hjørnet ved skilleveggen. Den skyves inn mot skilleveggen og holdes av en liten kul. Kabler ut i begge ender.
- **Skilleveggen** har to slisser, begge åpne nedenfra: 2 mm sprekk for spoletrådene rett foran leserens ende, og 5 mm slisse for strømkabelen. Tettes med Sika etter at kablene er lagt. Det er de eneste åpningene inn i el-rommet.
- **Strømkabelen** kommer inn under sideveggen gjennom en slisse 5 × 6 mm i underkanten, rett etter skilleveggen. PG7-hullet er borte.
- **PigeonPal-PCB** henger under gulvet på tre avstandsklosser med styretapper i H4, H3 og H1 (mål fra KiCad-filen), og holdes av to fjærende kroker. Komponentsiden vender ned mot lokket. Pluggkanten (J9, J3, J4) vender mot −y med 55 mm fri plass foran pluggene. Bøy krokene ut for å ta av kortet.
- **Gaflene** har en 8-kantet nav på 21 mm langs akselen. Fem naver fyller 105 av 110 mm, så de holder avstanden selv med 1 mm mellom hver. Stangen ligger flush med navet på utsiden, så gaffelen ligger flatt i printen.
- **Fjernet:** ribbene under leseren (107 mm broer i printen, ingen funksjon) og det blinde Ø6-hullet i skilleveggen.
- Slissene for veggtappene har runde ender.

| Print | Fil | Mål på platen |
|---|---|---|
| 1 | `stl/v4.3/sluse_v4.3_print1_kar_og_gafler.stl` – kar (gulvet ned) + 5 gafler | 200 × 239 × 32 mm |
| 2 | `stl/v4.3/sluse_v4.3_print2_hette_og_lokk.stl` – hette (taket ned) + lokk (oversiden ned) | 200 × 230 × 133 mm |

Sammenstillingen `step/v4.3/sluse_v4.3_sammenstilling.step` har kortet, leseren, spolen og akselen som referanser. Bilder i `tegninger/v4.3/`. Generator: `generator/sluse_v4_3_step.py`.

Ikke testet på print: lokkets spor (0,3 mm klaring), klikk-tungen, krokene på kortet og leserholderen (0,15 mm kul).

## v4.2 – 8-kantede gafler mot karkanten (erstattet av v4.3)

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
