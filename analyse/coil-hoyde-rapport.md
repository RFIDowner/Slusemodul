# Chipring-lesing i duefelle: lav eller hevet spole?

## 1. Kort svar

**Ikke bygg forhøyningen.** Monter spolen rett under et tynt gulv slik at ringen passerer 0,5–2 cm over viklingen (alternativ A). Det er teoretisk klart sterkest, og konklusjonen A > B gjelder uansett hvilken vei transponderaksen i ringen peker. Å legge spolen 5–10 cm under fuglen (alternativ B) flytter ringen til den delen av feltet der du målte *maks* rekkevidde på benken, dvs. null margin: 8–10 cm er lesegrensen for beste orientering på spoleaksen, ikke en driftshøyde. For en ring med horisontal transponderakse er 7–10 cm under terskel for alle ringrotasjoner (0,36–0,80× terskel i modellen), og 5 cm er marginalt. Det beste svaret er likevel ikke bare "lavt", men "lavt pluss riktig spolegeometri", se punkt 4.

## 2. Teorien, punkt for punkt

Alle tall er fra en Biot–Savart-modell av din 10 × 10 cm luftspole (ren Python, `coil_field_biot_savart.py` i denne mappen), verifisert mot lærebokformelen for senterfeltet (2√2·μ0·I/(π·a) = 11,31 µT per ampere-vikling). Terskelen er kalibrert fra din benketest: B_thr = feltet på aksen ved 9 cm = 14,6 % av senterfeltet. Absoluttverdiene skalerer med N·I; alle *forhold* (marginer, lesbar lengde) er uavhengige av det.

**a) Feltstyrke mot høyde.** På aksen er feltet nesten flatt så lenge høyden er mye mindre enn halvbredden (5 cm): 99 % av senterverdien ved 0,5 cm, 95 % ved 1 cm, 83 % ved 2 cm, 68 % ved 3 cm, 41 % ved 5 cm, 24 % ved 7 cm, 19 % ved 8 cm, 11,5 % ved 10 cm, deretter mot 1/z³ (Microchip AN678: feltet faller som r⁻³ og er hovedbegrensningen for rekkevidde). Ved 0,5–1 cm ligger vertikalfeltet 6,5–6,8× over terskelen (ca. 16 dB; 5,1–5,3× hvis reell grense er 8 cm). Ved 5–10 cm er du på den delen av kurven som faller med eksponent −1,6 (5–7 cm), −1,9 (7–8 cm) og −2,1 (8–10 cm), på vei mot −3. AN678/AN710s optimumsregel (sløyferadius ≈ 1,414 × leseavstand) sier bare at ved 8–10 cm ville en 14–28 cm bred sløyfe gitt mer felt per ampere-vikling; 10 cm-spolen leser der (det viser testen din), men den jobber utenfor sitt optimum, uten margin.

**b) Feltretning mot høyde og sideveis posisjon.** Inne i sløyfen nær overflaten er feltet vertikalt; rett over en leder er det horisontalt og sirkulært rundt tråden (≈ μ0·N·I/(2π·d), 1/d-lov). Rett over spolens senter er horisontalkomponenten *eksakt null i alle høyder* (symmetri). Feltets helning fra vertikal rett over tråden: 84° ved 0,5 cm, 78° ved 1 cm, 67° ved 2 cm, 59° ved 3 cm, 48° ved 5 cm, 40° ved 7 cm, 33° ved 10 cm. Jo høyere du går, desto mer *vertikalt* blir feltet også over trådene, og horisontalmaksimum flytter seg utover (5,5–6,5 cm fra senter ved 7–10 cm) og krymper til ~0,5× aksefeltet i samme høyde. Høyde gir altså ingen orienteringsgevinst for en fotring; forholdet horisontal/vertikal er låst til ~0,5 for alle høyder ≥ 3 cm.

**c) cos-θ-kobling og fotringen.** Indusert spenning i tag-spolen er V = 2πf·N·S·Q·B·cos α (AN678/AN710): bare feltkomponenten *langs transponderaksen* teller. Hvor aksen peker inne i ringen er avgjørende:
- *Horisontal akse* (typisk Hitag S-modul 8 × 10 mm i "knollen", radial eller tangential): ringen kobler kun til horisontalfeltet, som finnes bare nær lederne. Dette er det PIT-/fiskeri-litteraturen kaller "pass-over"-geometri: taggen leses best rett over tråden, rekkevidden er kortere enn "pass-through", og to separate deteksjoner per passering er mulig (Oregon RFID; LF 125 kHz-studien av steinsporing: "i vinkelrett konfigurasjon er deteksjonen svak, taggen kan bare detekteres over antennens kanter"). Ringen roterer fritt rundt beinet, så azimut er tilfeldig per passering. En ring hvis akse tilfeldigvis står *på tvers* av gangretningen og går nøyaktig på midtlinjen ser By = 0 i alle høyder. Det er et geometriproblem, ikke et høydeproblem.
- *Vertikal akse* (spole viklet rundt ringens omkrets, jf. EP2036001): ringen kobler til vertikalfeltet, hele sløyfeinteriøret er lesesone, og benketesten er direkte representativ.
- Beinet (tarsometatarsus) står ikke loddrett, anslagsvis 20–40° fra vertikal i stående stilling og mer under steget. Med 30° helning får en "horisontal-akse"-ring en Bz-kobling på ca. 0,5·Bz, som i praksis fjerner azimut-nullet i alternativ A, gjør 5 cm marginalt lesbart for alle rotasjoner og lar 7–10 cm forbli under terskel.

**d) Margin: dypt inne i feltet vs. nær maks rekkevidde.** Realistisk minsteavstand transponder–leder er 1–2 cm (viklingsbunt 2–5 mm + gulv 3–10 mm + knollens høyde over sålen), 1,5–3 cm i standfasen og 3–5 cm i svingfasen. 0,5 cm-raden under er en teoretisk grense, ikke driftspunktet. Overkobling/detuning ved lav høyde er ikke et problem for en mm-stor fotringtransponder: k ≈ 0,01 over tråden mot kritisk kobling k_c = 1/√(Q1·Q2) ≈ 0,05, dvs. ≥ 4× underkoblet, ingen frekvenssplitting (PMC5017394). Både energioverføring og lastmodulasjon tilbake til leseren skalerer med samme gjensidige induktans, så nærmere ring forbedrer begge samtidig.

| Avstand ring–vikling | Vertikal akse: margin på aksen | Vertikal akse: lesbar lengde av 18 cm | Horisontal akse, beste rotasjon: margin over leder | Horisontal akse, verste rotasjon m/ 30° beinhelning | Horisontal akse, beste rotasjon: lesbar lengde |
|---|---|---|---|---|---|
| 0,5 cm (teoretisk) | 6,8× | hele | 24× | – | 9 cm (to bånd) |
| 1 cm | 6,5× | hele | 11,8× | 4,5× | 11 cm (to bånd) |
| 2 cm | 5,7× | 13,5 cm | 5,5× | 2,9× | 14 cm |
| 3 cm | 4,7× | 11,5 cm | 3,3× | 2,3× | 14 cm |
| 5 cm | 2,8× | 11,5 cm | 1,5× | 1,4× | 11 cm |
| 7 cm | 1,65× | 9,5 cm | 0,80× | 0,8× | 0 |
| 8 cm | 1,28× | 7,5 cm | 0,61× | – | 0 |
| 10 cm | 0,79× | 0 | 0,36× | – | 0 |

Ved 0,5–1 cm er lesesonen for horisontal akse *to* 4,5–5,5 cm brede bånd sentrert på de to tverrtrådene (ca. 2,6–7,6 cm fra senter ved 1 cm), med et null over senteret. Gangbane 2,5 cm ut av senter gir lengre lesbar sone (opptil 17,5 cm ved 2–3 cm) fordi sidetrådene bidrar med By. Forhold lav/høy for horisontal akse: 1 cm mot 5/7/8/10 cm = 7,8× / 15× / 20× / 33×, dvs. 18–30 dB kastet bort uten noen orienteringsgevinst. Ved 7–10 cm er beste horisontalfelt 0,36–0,80× terskelen; med modellens usikkerhet (±1,27×) er 7 cm "ikke pålitelig", 8–10 cm "ikke lesbar". Ved 5 cm faller omtrent halvparten av ringrotasjonene under terskel uten beinhelning.

**e) Oppholdstid og telegramrepetisjon.** EM4100/TK4100 sender 64 bit kontinuerlig ved RF/64: 64 × 512 µs ≈ 33 ms per telegram, ≤ 66 ms sammenhengende felt garanterer ett komplett telegram (RDM6300 leverer pakke hvert ~65 ms). Er leseren en RDM6300/EM4100-modul, er ringene EM4100/TK4100-kompatible; Hitag S (kommandostyrt, T0 = 8 µs, anslått samme størrelsesorden fra T0/twsc, ikke målt full lesesyklus) gjelder da ikke. Duer på tredemølle er kjørt ved 0,20–0,40 m/s (JEB 209:292); løp begynner rundt 0,75–0,9 m/s (Gatesy & Dial 1993; Fujita 2002). Men gangen er ikke jevn: foten står stille i standfasen (~0,25 s) eller svinger 2–4 cm over gulvet i ~0,15–0,2 s, ca. dobbelt så fort som kroppen. Med ett 10 cm-kvadrat og to lesebånd 10 cm fra hverandre er det grovt ~1/3 sjanse for at ingen stans havner i et bånd (horisontal akse); da må ringen leses i svingfasen ved 3–4 cm (2–3× margin, 60–80 ms = 1–2 EM4100-telegram, knapt for en Hitag S-handshake). Tid er ikke flaskehalsen, men sammenhengende lesesoner (vertikal akse, figur-8 eller flere ledere på tvers) er å foretrekke, nok et argument mot forhøyning.

**f) Kommersiell praksis.** Benzing G2 (15 × 19 cm per felt), Bricon (1–6 felt) og Unikon ("two-field pad") er flate flerfeltspader i 22–27 mm tykke hus, montert i eller under ≤ 15 mm kryssfiner (Bricon); ringen passerer derfor typisk 2–4 cm fra viklingen, innenfor sonen der modellen gir 3–5× margin, aldri 5–10 cm. FCI krever sikker lesing innenfor 5 cm. At Bricons "5–7 cm"-test er en marginkontroll med håndholdt ring og ikke driftshøyde, er vår tolkning, ikke leverandørens ord.

## 3. Hva benketesten sier, og ikke sier

Den sier hvor terskelen ligger for beste orientering (≈ 0,12–0,19 × senterfeltet) og at leser + spole + ring fungerer. På spoleaksen er feltet rent vertikalt. At ringen leses på aksen ved 8–10 cm betyr derfor at transponderaksen hadde en vesentlig vertikal komponent *i testorienteringen*. Hvordan holdt du ringen?

- Holdt du den **flatt, slik den sitter på beinet** (ringplanet parallelt med spolen): da er aksen vertikal på fuglen, benketesten er direkte representativ, og Bz-kolonnen gjelder. A gir 6–9× margin over hele sløyfen; B ved 5 cm gir 2,8× og fungerer, men 7,7 dB dårligere og uten reserve for høydevariasjon; 8 cm 1,28×, 10 cm ingen lesing. Figur-8/skjevstilling er da ikke nødvendig.
- Holdt du den **på høykant / med knollen flatt** (aksen horisontal på beinet): da gjelder kant-/pass-over-analysen, og geometrivalg i punkt 4 blir nødvendig, ikke valgfritt.

Testen sier ikke noe om gangfart, beinhelning, ringrotasjon eller om foten faktisk krysser en leder. Bruk 8–10 cm kun som terskelreferanse, aldri som driftshøyde.

## 4. Anbefaling, rangert

**Felles for alle:** spole rett under gulvet. 3–10 mm PETG er fint (Bricon tillater 15 mm kryssfiner); det som teller er total avstand ring–vikling ≤ 2–3 cm. Ingen metall, folie, netting eller karbonfylt plast mellom spole og fot (skinndybde 0,2–0,26 mm i Cu/Al ved 125 kHz gir titalls dB skjerming pluss detuning). Spolen bør være minst like bred som gangbanen (10–12 cm), så enten 12–14 cm sløyfe eller to sløyfer side om side. Lag et kort kanalløp så fuglen må *gå* over spolen, ikke hoppe; hopp over paden er den vanligste feilårsaken i praksis. Hold leser og evt. andre 125 kHz-spoler ≥ 1 m fra hverandre.

1. **Lav montering + ledere langs OG på tvers av gangbanen** (høyest sikkerhet, middels innsats). Kvadratisk sløyfe kombinert med en langsgående figur-8 (byttet/multiplekset, eller to leserkanaler): verste-azimut-margin 10,8× / 5,0× / 3,0× ved 1/2/3 cm. Alternativt kvadrat + liten vertikal veggspole (akse på tvers av passasjen) for tverr-azimuten. Merk: figur-8 med felles midtleder *på tvers* dobler feltet over midtlederen (79/39/18/11/5 µT per A-vikl. ved 0,5/1/2/3/5 cm, ved lik strøm per sløyfe) og flytter nullet til ytterkantene, men fjerner ikke tverr-azimut-nullet på midtlinjen. Induktansen omtrent dobles, så ved samme drivspenning blir gevinsten mindre og leseren må tunes på nytt. Patent 5602556 (figur-8 gir felt parallelt med antennen) og 8558751 (dobbel sløyfe med alternerende fase mot orienteringsvarians, 125 kHz) beskriver prinsippet.
2. **Lav montering + én sløyfe dreid 45° ("diamant") eller 15–30° skjev**, minst tre ledere på tvers av banen (best nytte/innsats). Diamant: verste-azimut 7,9× / 3,2× / 1,7× ved 1/2/3 cm for et bein 2 cm fra midten, 4,1× / 1,1× / 0,5× 0,5 cm fra midten og null eksakt på midtlinjen, men 5,3× / 3,0× / 2,3× også på midtlinjen med 30° beinhelning. Chipringen sitter på ett bein ca. 1–1,5 cm fra kroppens midtlinje, og fuglen vandrer, så midtlinje-nullet er lite i praksis, men ikke null. Forskyvning 2,5 cm fra midtlinjen gir tverr-azimut-dekning, men bare 0,8× / 1,4× / 1,8× / 1,6× margin ved 0,5/1/2/3 cm, ikke tilstrekkelig alene.
3. **Lav montering + én kvadratisk sløyfe sentrert, trådene på tvers** (enklest). To 4,5–5,5 cm brede lesebånd med 9–12× margin (beste rotasjon), men ~5–15 % av rotasjonene bommer på midtlinjen ved 0,5–2 cm, og ~1/3 av passeringene får ingen stans i et bånd. Godt nok hvis aksen viser seg å være vertikal.
4. **Vertikal portalsløyfe fuglen går gjennom**, ca. 12 × 18 cm: svært høydetolerant (10 × 10-modellen ga 45/25/15,5/12,7/11,3 µT per A-vikl. ved 0,5–5 cm over gulvet) og orienteringsrobust for akse langs gangretningen; mer mekanikk og trenger sidespole for tverr-aksen.
5. **Forhøyet gangbane, spole 5–10 cm under (B):** dårligst. Horisontal akse: null lesing ved ≥ 7 cm, marginalt ved 5 cm. Vertikal akse: 2,8× ved 5 cm, 1,28× ved 8 cm, ingen ved 10 cm, alt uten reserve for høydevariasjon. Ikke anbefalt.

## 5. Benketest du kan gjøre i kveld

**Test 0 (5 min, avgjør aksen):** sett ringen på en vertikal pinne nøyaktig som på beinet (ringplanet horisontalt). Senk den til 1 cm over spolens *senter* og over en *kanttråd*. Leser bare over kanten → horisontal akse, punkt 4.1–4.2 er nødvendig. Leser best over senter → vertikal akse, punkt 4.3 holder.

**Test 1 (høydeskann):** samme pinne, beveg ringen horisontalt tvers over spolen i fast høyde 0,5 / 1 / 2 / 3 / 5 / 8 cm over viklingen, sentrert bane og bane 2,5 cm ut av senter. Noter hvor den leser. Gjenta med ringen rotert 0°, 45° og 90° om pinnen.

Forventet (horisontal akse): ved 0,5–1 cm to smale bånd (4–6 cm) over trådene, null i midten; ved 2–3 cm bredere men svakere bånd; ved 5 cm sporadisk, avhengig av rotasjon; ved 8 cm ingenting. Forventet (vertikal akse): lesing over hele sløyfen ved 0,5–3 cm, krympende mot 7–8 cm, ingenting ved 10 cm. Forskjøvet bane bør gi lengre lesesone ved 1–3 cm.

**Det som bekrefter anbefalingen:** sikker lesing ved 1–3 cm (over trådene eller hele flaten) og tap ved 5–8 cm. **Det som velter den:** sikker lesing i alle rotasjoner ved 5–8 cm og *ikke* ved 1–2 cm; da er enten viklingen mye bredere/spolen tunet slik at nærsonen overkobler (front-end-problem, løses med Q/tuning), eller premissene om ringen er feil, og vi må se på den på nytt.

**Etter bygging:** test med aluminiums-forbundsringen montert som på fuglen, og logg med levende fugl i gangfart, ikke bare ringen på pinne; fotplassering i standfasen er den gjenværende feilkilden. Krav: sammenhengende lesing over ≥ 4 cm i alle rotasjoner ved faktisk gulvhøyde.

## 6. Usikkerheter

- Transponderaksen i ringen er ukjent; Test 0 avgjør. A > B holder i begge tilfeller, men geometrikravene avhenger av det.
- Modellen er en filamentær enkeltvikling i luft, uten gulv-/kroppstap. 40 µT-toppen ved 0,5 cm er overestimert for en flere mm bred viklingsbunt; verdiene ved 1–3 cm er robuste. En bunt av bredde w flater ut 1/d-loven for d < w.
- Terskel kalibrert til 9 cm; 8 cm krymper alle marginer 1,28×, 10 cm øker dem 1,26×. Ingen konklusjon endres.
- Beinhelning (20–40°), ringens vagging, eksakt beinhøyde over gulvet og stegmønster er antatt, ikke målt.
- Transpondertype (EM4100 vs Hitag S) påvirker telegramtid og H_min, ikke høydetrenden. Hitag S-timing er et estimat fra datablad-utdrag.
- Leserens følsomhet, Q og AGC kan gi egne nærsone-effekter; det er et front-end-problem, ikke et høydeproblem.
- Ingen sitater kunne verifiseres mot originaldokumentene i denne kontrollen (nettsperre); ordlyd fra Microchip, Oregon RFID, patenter, Bricon/Benzing/Unikon, FCI og tidsskrifter bør sjekkes mot PDF-ene før den siteres videre.

## 7. Kilder

- [Microchip AN678, RFID Coil Design](https://ww1.microchip.com/downloads/en/appnotes/00678b.pdf) – r⁻³-fall, cos α-kobling, optimumsregel for sløyferadius
- [Microchip AN710, Antenna Circuit Design for RFID Applications](https://ww1.microchip.com/downloads/en/appnotes/00710c.pdf)
- [Microchip DS51115, microID 125 kHz Design Guide](https://ww1.microchip.com/downloads/en/devicedoc/51115f.pdf)
- [OpenStax, Magnetic Field of a Current Loop](https://phys.libretexts.org/Bookshelves/University_Physics/University_Physics_(OpenStax)/University_Physics_II_-_Thermodynamics_Electricity_and_Magnetism_(OpenStax)/12:_Sources_of_Magnetic_Fields/12.05:_Magnetic_Field_of_a_Current_Loop) – Biot–Savart, aksefelt
- [IntechOpen, LF/HF RFID coupling and H_min](https://www.intechopen.com/chapters/57275)
- [Finkenzeller, RFID Handbook, 3. utg.](https://www.wiley.com/en-us/RFID+Handbook:+Fundamentals+and+Applications+in+Contactless+Smart+Cards,+Radio+Frequency+Identification+and+Near+Field+Communication,+3rd+Edition-p-9780470695067)
- [Oregon RFID, Antenna types (pass-over vs pass-through)](https://www.oregonrfid.com/resources/antenna-types/)
- [Biomark PIT-tag antennas](https://www.biomark.com/pit-tag-antennas/) og [AFS/Biomark antenner](https://units.fisheries.org/fits/solution/fish-tracking/rfid/biomark-antennas/)
- [NOAA, PIT-antenne feltgeometri](https://repository.library.noaa.gov/view/noaa/50485/noaa_50485_DS1.pdf)
- [Zentner et al. 2021, PIT-antenne deteksjon vs orientering](https://agriculture.okstate.edu/departments-programs/natural-resource/research/natural-resource-labs/shoup-fisheries-management-and-fisheries-ecology-lab/zentner_et_al_2021.pdf)
- [Pebbles tracking with LF RFID multi-loop reader (kantdeteksjon i vinkelrett orientering)](https://www.researchgate.net/publication/270337982_Pebbles_Tracking_Thanks_to_RFID_Lf_Multi-Loops_Inductively_Coupled_Reader) / [HAL](https://centralesupelec.hal.science/hal-01104660)
- [US 5602556, figur-8-sløyfe med felt parallelt med antennen](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5602556)
- [US 8558751, dobbel sløyfe med alternerende fase, 125 kHz](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8558751)
- [PMC5017394, kritisk kobling og frekvenssplitting](https://pmc.ncbi.nlm.nih.gov/articles/PMC5017394/)
- [EP0884700B1, Deister/Unikon flerfelts duepad](https://patents.google.com/patent/EP0884700B1/en)
- [EP2036001B1, transponder-fotring for duer](https://patents.google.com/patent/EP2036001B1/de)
- [FCI, krav til elektronisk konstatering](https://img.pigeonsfci.net/uploads/files/20241104/87de9a8ee1972ad0ccb38cbf030db2be.pdf)
- [Benzing G2 antenne](https://www.benzing.cc/benzing-g2-antenna/) og [Benzing antennepader](https://www.benzinguk.com/product-category/antenna-pads/)
- [Bricon Speedy manual](https://www.bricon.be/uk/manuals/Speedy%20UK-14.pdf) / [manualslib](https://www.manualslib.com/manual/1304348/Bricon-Speedy.html)
- [Unikon loft-system](https://www.unikon.co.uk/loft/) og [Unikon manual](http://www.unikon-usa.com/us/files/unikon_manual_010307.pdf)
- [Hitag S256 duefotring](https://zdcard.en.made-in-china.com/product/pSImxjvKbuYM/China-RFID-Racing-Pigeon-Foot-Ring-Hitag-S256-for-Tauris-Ets-Clocking-System.html)
- [EM4100 datablad](https://download.mikroe.com/documents/accessories/rfid/125khz/rfid-card-125khz-em4100-datasheet.pdf) og [EM4100-protokoll](https://www.priority1design.com.au/em4100_protocol.html)
- [RDM6300 (Tasmota-dok.)](https://tasmota.github.io/docs/RDM6300/)
- [NXP Hitag S datablad](https://media.digikey.com/pdf/Data%20Sheets/NXP%20PDFs/HTS.pdf)
- [J. Exp. Biol. 209:292, duer på tredemølle 0,20–0,40 m/s](https://journals.biologists.com/jeb/article/209/2/292/16277/Influence-of-the-behavioural-context-on-the)
- [Skinndybde-kalkulator](https://www.firgelliauto.com/blogs/engineering-calculators/skin-depth-calculator) og [RFID-skjerming](https://rfid4u.com/rfid-shielding-and-blocking-materials/)
- [pigeons.biz, installasjon av elektronisk klokke](https://www.pigeons.biz/threads/electric-clock-installation.65274/)