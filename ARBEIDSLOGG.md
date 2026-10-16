# Arbeidslogg — Slusemodul

Nyeste øverst. Oppdateres hver økt. Modellbeskrivelser per versjon står i `README.md`.

## Setting og arbeidsfordeling

| Hvem | Rolle | Gjør |
|---|---|---|
| **Stig** | Eier, designer | Bestemmer form og prinsipp, tegner egne forslag i Fusion, ser på hver STEP før commit, printer og tester |
| **Jonas** | Ingeniør (PCB) | Bekrefter kortets mål, kontakter og LED-header når slusa trenger det |
| **Claude** | Verktøy | Skriver generatorene, regner på fjærer og printbarhet, lager STEP/STL/bilder, oppdaterer README og logg, committer. Foreslår, endrer ikke uten OK |

Arbeidsform: ett punkt om gangen. Claude foreslår med begrunnelse → Stig sier OK → generator → bilder og mål → Stig ser i Fusion → commit på `v5-skuff-kroker`. Push når Stig sier det.

---

## 2026-10-16 (Stig + Claude) — v5, v6 og v7

### Status
| | |
|---|---|
| Branch | `v5-skuff-kroker` fra `main` (d8e5e75, v4.3). Ikke pushet, ikke merget |
| Commits | `ae9ce90` v5 (to deler, erstattet samme dag), `85b5834` v6 (ett stykke) |
| Gjeldende modell | v7: STL og STEP klar, ikke printet. Ikke committet ennå, Stig skal se på STEP |
| Neste | Stig ser på v7 i Fusion → commit → print |

### Gjort i dag
- **v5:** kar + hette med kroker ved inngangen og trykknapper ved slaget, tak som flygende due, skuff fra inngangsenden. Lagt bort samme dag fordi Stig kom med sin egen modell.
- **v6:** bygd etter Stigs Fusion-modell «nyeste antenne løsning» (`stl/v5/`): ett stykke, spisse portaler, ribber over forgangen, spiler i karveggene, el-rom under gulvet, spolelomme, skuff fra −y-siden med skjult tunge. Spiss topp i alle veggmellomrom (Stigs ønske). LED-hullet fjernet (Stigs ønske). Målt av Claude: 212 × 128 × 197 mm, 371 cm³ ≈ 470 g PETG.
- **Problem med v6:** stående print trenger støtte under hele gulvet (el-rom og spolelomme). Stig vil ikke ha det. Derfor v7.
- **v7:** bygd etter Stigs eget forslag (kveld): to deler, stolpene går rett ned i hull i plinten, ingen klips. Først sju like takstoler; Stig slanket til fire (tok 2, 4 og 6), gavl 6 mm, og la til én skrå avstiver per side som går gjennom stolpene. Splint i fire hull. Hette 462 → 151 cm³. Se README. Claudes Forslag A (skjørt, neser, fjærtunger) og den foreslåtte bunnlista ble forkastet av Stig.

### Beslutninger
- Ordbruk: **plint** = bunnen (gulvplaten 32 mm høy med el-rom og spolelomme under, og åpningen for skuffen). **Hette** = ribber, portaler, spiler og toppramme. **Skuff** = lokket under el-rommet.
- Fjærer alltid i printplanet, tøyning under 1 %. Ingenting i første lag. Ingen hull gjennom gulvet.
- Spolen klikker inn nedenfra som i v4.3 (fire fjærende felt med nese).
- Idéen om å stoppe printen og legge spolen inn er forlatt (Stig 16. okt).
- Gafler (envegs) utsettes. Claudes råd når de kommer: ved utgangsportalen, lengde fra dreiepunkt ca. 140 mm over gulvet.
- Stigs egne filer ligger i `stl/v5/` (`nyeste antenne løsning.f3d` og `.stl`). Kan flyttes senere.
- Urelatert fil `stl/v4.3/bobil kjøkkenhylle nederst.stl` er med vilje ikke committet.

### Beslutninger for v7 (Stig, 16. okt kveld)
- Stolper rett ned i hull. Alle stolper like. Sju per side: første og siste som i v6 (x 0 og 172), resten jevnt fordelt.
- Klaring 0,2 mm per side (Claude foreslo 0,3; Stig ville ha 0,2, Claude ikke uenig).
- Ingen vanntiltak for hullene: blinde hull, ingen dreneringsslisser. Et 3 mm hull i bunnen av hvert hull er greit, ikke mer.
- Hull i første lag mot platen er greit (plinten printes med gulvet ned).
- Ingen bunnlist i hetta. Takstolene bindes bare av toppramma. Alle takstoler har samme spisse vinkel.
- Stolpene kan være større enn v6 sine 4 mm, og gjerne hule. Claude valgte 10 × 8 mm massive: hule med 2 mm gods ville gitt et 6 × 4 mm hulrom og spart lite, og tappen ville blitt hul.
- Fillet bare der det trengs. Claude la ingen inn: takstolene er sammenhengende vegger uten innvendige hjørner som bærer last.
- Feste: fire 4,2 mm hull (første og siste takstol, begge sider), printet splint. M4 med mutter som reserve i samme hull.
- Slanking (Stig, sent 16. okt): takstol 2, 4 og 6 bort, 43,5 mm mellomrom. Claude innvendte at 43 mm er nær bob-avstanden i duefeller (45–50 mm) og at en due kan komme gjennom; Stig mener de ikke kommer gjennom og tar det. Ses an på print.
- Avstiver etter Stigs idé: én stav per side som går gjennom alle stolpene, 45° i stedet for 44° så den ender i toppramma. Stig ville så slanke mer og la til kryss (to staver) for å kunne gå ned i mål.
- Endelige mål (Stig, med Claudes ene endring): bein 10 × 5 (Stig foreslo 10 × 4, Claude ville ha 5 på tvers fordi krysset ikke stiver av på tvers), kryss 4 × 4, gavl 4, toppramme 5 × 10, tapp 10 × 3,5. Plinten tilbake til 128 mm bredde, døråpningen 116, hetta 126 bred. Hetta printes med brim.
- Due: Stig ønsket sin due fra el-boksen (flygende, strek) som kropp i åpningen mellom stolpene. Claude prøvde: hengt under toppramma må flat rygg og hode fylles opp mot ramma, og da blir den en klump; alle rotasjoner gir 14 mm overheng. Claude tegnet en sittende due på nytt, 3 mm, mellom stolpe 1 og 2. Stig forkastet den («bare å fjerne»). Ingen due i v7.
- Gjenstår fra samme diskusjon: loddrett pinne mellom stavene i de tre andre endeåpningene (Claudes forslag, Stig sa «lag kun duen nå»).

### Åpne spørsmål (til Stig)
- PETG eller ASA? (ASA tåler sol bedre, PETG er enklere å printe.)
- LED utvendig: hullet er fjernet. Hvis LED skal ut, må Jonas bekrefte header på kortet.
- Spolens siste ~37 mm ligger på gulvet uten vegger inne i slaget. Duer som står der kan leses uten å gå gjennom. Alternativer: flytt utgangsportalen til gulvenden, flytt spolen 40 mm, eller løs det i fastvaren.
- Festeører til slaget: ikke tegnet i v7 ennå.
- Duesilhuetten i taket (v5) er borte i v6. Vil Stig ha den tilbake?

### Antakelser
- Stigs modell er målt fra STL: kar 128 × 120, vegger 2 mm, døråpning 116 bred, rette sider til 95, topp 135. v6 bruker 113/158 fordi gulvet ligger 32 mm høyere.
- Kortet og leseren i sammenstillingen er referansemodeller etter v4.3-målene, ikke Jonas' siste kort.
- Bambu A1 printer 38°-overheng (52° fra vertikal) i PETG uten støtte. Ikke prøvd ennå.

---

## Tidligere (fra git-loggen)
- v4.3 (d8e5e75): kabelføring, kortfeste, skyvelokk, leser i tørt rom, gafler med nav. Printproblemer: 145 mm bro, tapper på tvers av lagene med ca. 8 % tøyning, renner i første lag. Dette er grunnen til reglene over.
- v4.2: karet er printet. v3: modul B er printet.
