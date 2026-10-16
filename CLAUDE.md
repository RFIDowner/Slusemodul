# Slusemodul — arbeidsregler for Claude

Les `ARBEIDSLOGG.md` først. Den har status, beslutninger, gjenstående og antakelser. `README.md` beskriver modellene (hva hver versjon er, mål, filer).

## Prosjekt
- 3D-printet duesluse for PigeonPal. Duene går én og én over en 125 kHz RFID-spole; PCB-en fra `../Kicad-PigeonPal-PCB` sitter i et el-rom under gulvet.
- Modellene lages av Python-generatorer i `generator/` (cadquery). De skriver STEP til `step/vN/`, STL til `stl/vN/`, bilder til `tegninger/vN/`.
- Printer: Bambu Lab A1 (maks 256 × 256 × 256 mm), PETG.
- Eier: Stig (ikke ingeniør). Ingeniør på PCB: Jonas. Stig ser på modellene i Fusion 360.

## Regler (fra Stig)
1. Jobb på egen branch. **Aldri `main`.** Nå: `v5-skuff-kroker`.
2. Én logisk endring per commit. Commit-melding sier hva og hvorfor.
3. Ett steg om gangen: foreslå → Stig sier OK → gjør → vis bilder og mål → Stig ser på STEP i Fusion → commit.
4. Ingen endringer i modellen uten OK. Når Stig sier «ingen kode nå», bare diskuter.
5. Push kun når Stig sier det, og kun til arbeidsbranchen.
6. Ryddighet: ingen etterlatte filer, hver versjon i egen mappe, README oppdatert i samme commit som modellen.
7. Skriv antakelser og beslutninger i `ARBEIDSLOGG.md`.

## Designregler (avtalt med Stig)
- Alle fjærer ligger i printplanet, aldri på tvers av lagene. Tøyning under 1 % (maks 2 %).
- Ingenting fint i første lag mot platen (renner, slisser, neser).
- Ingen hull gjennom gulvet ned i el-rommet (vann).
- Overheng maks 45°; buer er to rette linjer. Klaring 0,3 mm i skyveflater.
- Skjulte låser som bare Stig vet om (negl/kniv i hakk), ingen skruer, ingen pakning.
- Støtte i printen unngås. Stig vil helst ha få print, men ikke støtte under hele gulvet.

## Kjøring
```
python -X utf8 generator/sluse_v6_step.py     # modell + sjekk (solid, kollisjon, mål)
python -X utf8 generator/render_v6.py         # PNG til tegninger/v6/
```
`-X utf8` trengs fordi konsollen er cp1252. cadquery ligger i system-Python 3.12 (`pip install cadquery`). Generatorene sjekker selv at delene er gyldige solider og at ingenting kolliderer.

## Fallgruver
- Stigs `.f3d`-filer kan ikke leses (zstd + Parasolid). Be om STL eller STEP.
- Render: cadquery → trimesh (`subdivide_to_size(12)`) → matplotlib, ellers blir dybdesorteringen feil.
- Koordinater i v6/v7: X langs løpet (0 = inngang, 212 = slaget), Y på tvers, Z opp (0 = landingsbrett, gulvtopp 32).
