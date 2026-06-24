---
name: semantic-stack
description: Skriv SEO-optimerade svenska artiklar genom ett flerstegs flöde — term-extraktion (NeuronWriter-stil) från topp 10 SERP, research via fulltextshämtning, artikelplan enligt Rank2Bank (Korays holistiska SEO-metodik), artikel enligt Matyas SEO-skrivriktlinjer, och slutfil med frontmatter. Stödjer `auto:`-prefix för icke-stop körning. Triggar på "semantic-stack", "ny artikel", "skriv artikel", "SEO-artikel", eller när användaren ger ett sökord/sökfras att producera artikel kring.
---

# semantic-stack

Detta är ett flerstegs-flöde för att producera en SEO-optimerade svensk artikel utifrån ett sökord eller en sökfras. Flödet följer Korays semantiska SEO-metodik (Rank2Bank) för planering och Matyas svenska skrivriktlinjer för utförande. Term-extraktion i NeuronWriter-stil från topp 10 SERP säkerställer kvantitativ vokabulärtäckning.

---

## ⛔ Absoluta förbud — läs detta först

Dessa regler gäller alltid, oavsett läge, batch-storlek eller tidspress:

1. **Web-research är obligatorisk.** Steg 1 (WebSearch + fetch av minst 7 URLs) FÅR INTE hoppas över. Artiklar skrivna enbart från träningsdata räknas inte som giltiga semantic-stack-outputs — de saknar termtäckning, saktuell data och direktcitat.

2. **Ingen artikel utan terms.json.** terms.json är artikelns kontrakt. Utan den finns det inget sätt att verifiera termtäckning. En artikel utan terms.json är inte färdig, oavsett hur bra den läser.

3. **Aldrig bulk utan per-entitet-flöde.** Om N artiklar ska skrivas körs Steg 1–5 för varje entitet separat, i tur och ordning. Det är ej tillåtet att aggregera N entiteter i ett enda agent-prompt och be dem skriva från minnet. Genvägen "skriv snabbt från träningsdata" producerar ytliga artiklar utan SEO-värde.

4. **Subagenter måste ha research-data i prompten.** Om subagenter används för att skriva artikeln (Steg 4–5) måste de få `research.md`, `plan.md` och `terms.json` som explicit kontext — inte en bullet-lista med fakta från moderagentens träningsdata. Subagenter som skriver från bullet points hoppar de facto över Steg 1–3.

5. **Effektivitet ersätter inte kvalitet.** Det är alltid bättre att leverera 3 artiklar med full research än 30 artiklar från minnet. Kommunicera detta till användaren om de ber om bulk-generering i ett tempo som inte medger riktigt flöde.

---

**Två lägen:**

- **Step-by-step (default):** Pausa efter varje steg, visa resultatet, vänta på godkännande. Användbart när du vill granska och justera.
- **Auto-mode (`auto:`-prefix på sökordet):** Kör alla fem steg i ett svep utan godkännanden. Slutrapport visas på en gång. Användbart när intake är bekant och du litar på flödet.

All output mot användaren och alla genererade filer ska vara på svenska.

## Argumentparsning

Användaren anropar skillen med valfri kombination av prefix, domän och sökord:

| Syntax | Beteende |
| :--- | :--- |
| `/semantic-stack reavinstskatt gammalt hus` | Step-by-step, sajt-detektering via preset/memory/intake |
| `/semantic-stack auto:reavinstskatt gammalt hus` | Auto-mode, sajt-detektering via preset/memory/intake |
| `/semantic-stack teknikhajen.se reavinstskatt gammalt hus` | Step-by-step, sajt **auto-detekteras från domänen** |
| `/semantic-stack auto:teknikhajen.se reavinstskatt gammalt hus` | Auto-mode + domän-detektering = **nollfrågor**, fire-and-forget |

**Parse-logik (i ordning):**

1. **Strippa `auto:`-prefix** om det finns (case-insensitive). Sätt internt `$AUTO_MODE = true`.
2. **Identifiera domän** i första token efter strippning:
   - Innehåller token en punkt och slutar på en känd TLD (`.se`, `.com`, `.org`, `.net`, `.io`, `.nu`, `.eu`, `.dk`, `.no`, `.fi`, `.de`, `.uk`)? → Behandla som domän. Sätt `$DOMAIN = token`, ta bort token från resterande input.
   - Annars: `$DOMAIN = null`.
3. **Resterande input** = sökordet/sökfrasen.

**Exempel parsing:**

| Input | $AUTO_MODE | $DOMAIN | Sökord |
| :--- | :--- | :--- | :--- |
| `reavinstskatt gammalt hus` | false | null | "reavinstskatt gammalt hus" |
| `auto:mbappe lön` | true | null | "mbappe lön" |
| `teknikhajen.se reavinstskatt` | false | teknikhajen.se | "reavinstskatt" |
| `auto:gmlsports.se mbappe lön` | true | gmlsports.se | "mbappe lön" |

## Förberedelse (intake)

**Mål:** Få fram sökord + kontext (sajt, målgrupp, ton, längd, interna länkar, output-mapp) med så få frågor som möjligt. Idealfallet = nollfrågor.

**Resolution-ordning (i denna ordning):**

1. **Sökord** — alltid från argumenten (efter `auto:` och eventuell domän-strippning).

2. **Domän auto-detektering** — om `$DOMAIN` är satt:

   **Steg-för-steg:**
   - Hämta `https://[domain]/` via `fetch.ps1`/`fetch.sh` (samma script som Steg 1). Spara till `./drafts/{slug}/_site_homepage.txt`.
   - Extrahera från homepage:
     - `<title>` → sajtnamn
     - `<meta name="description">` → positioneringstext
     - Senaste artikellänkar från `<a href>` med samma hostname → sampla 1–2 stycken
   - Hämta 1–2 sample-artiklar från samma domän, spara som `_site_sample_NN.txt`
   - Analysera samtliga filer och bygg en site-profil i `./drafts/{slug}/_site_profile.json`:

     ```json
     {
       "sajt": "teknikhajen.se",
       "namn": "Teknikhajen",
       "tema": "Teknik och konsumentguider",
       "malgrupp": "Privatpersoner med teknikintresse",
       "ton": "Saklig guide, vänlig",
       "typisk_langd": "1800-2500 ord",
       "interna_lankar": false,
       "output_mapp": "./articles/",
       "kalla": "auto-detekterad 2026-05-13"
     }
     ```

   **Viktig policy — interna länkar:** `interna_lankar` ska **alltid sättas till `false`** som default, även om domän-detekteringen visar att sajten faktiskt använder interna länkar. Skälet: skillen har inte tillgång till sajtens fullständiga artikelinventory och kan inte verifiera att gissade URL:er existerar. Att inkludera påhittade interna länkar är värre än att inte ha några. Användaren kan manuellt sätta `interna_lankar: true` i sin `.semantic-stack-preset.json` om hen har full översikt över sin sajt och vill att skillen ska föreslå platshållare för internlänkar (märkta som "verifiera URL").

   - **I step-by-step:** visa profilen som en rad ("Detekterad profil: teknikhajen.se / Privatpersoner / Saklig guide / 1800-2500 ord / inga interna länkar") och fråga "OK eller justera?" (Ja / Justera).
   - **I auto-mode:** visa profilen som statusrad och fortsätt direkt.

   **Default output_mapp** sätts till `./articles/` om inte annan information finns i sample-artiklar (då kanske `./posts/`, `./content/` eller liknande baserat på vad sajten verkar använda).

   **Om domän-fetch misslyckas** (404, timeout, tomt innehåll): logga felet, fall tillbaka till steg 3 (projektpreset).

3. **Projektpreset** — om ingen domän var given (eller domän-fetch misslyckades), kontrollera `./.semantic-stack-preset.json`. Format:

   ```json
   {
     "sajt": "teknikhajen.se",
     "malgrupp": "privatpersoner",
     "ton": "saklig guide",
     "langd": "2000+",
     "interna_lankar": false,
     "output_mapp": "./articles/"
   }
   ```

   Om filen finns, visa: *"Använder projektpreset: teknikhajen.se / privatpersoner / saklig guide / 2000+ ord / inga interna länkar / ./articles/"*. I step-by-step fråga "Använd dessa eller justera?". I auto-mode fortsätt direkt.

4. **Cross-project memory** — om ingen projektpreset finns, kontrollera `~/.claude/skills/semantic-stack/.last-context.json`. Om yngre än 30 dagar, visa sammanfattning och samma flöde som projektpreset.

5. **Fresh intake** — sista utvägen om varken domän, preset eller memory ger resultat. Kör en enda `AskUserQuestion` med 3–4 frågor i en batch:
   - Sajt/domän + målgrupp
   - Ton + längd
   - Output-mapp
   - "Vill du spara detta som projektpreset?" (Ja/Nej)

   **Standardprofiler** att erbjuda:
   - **Teknik/konsumentguide:** privatpersoner, saklig guide, 2 000+ ord, inga interna länkar
   - **Sport/fotboll:** sport/fotbollsintresserade, vänlig/neutral, 2 000+ ord, inga interna länkar
   - **Privatekonomi:** privatpersoner, saklig guide, 2 000+ ord, inga interna länkar
   - **Egen kontext:** fritext

6. **Spara state efter intake (alla vägar):**
   - Skriv alltid `~/.claude/skills/semantic-stack/.last-context.json` med aktuell timestamp.
   - Om domän var given → skriv även `./.semantic-stack-preset.json` automatiskt baserat på detekterad profil (gör nästa körning i samma projekt nollfrågor).
   - Om användaren valde att spara via fresh intake → skriv `./.semantic-stack-preset.json`.

**Slug-regler för sökordet:**
- Lowercase
- Svenska tecken: `å→a`, `ä→a`, `ö→o`
- Övriga icke-alfanumeriska tecken: ersätt med `-`
- Trimma ledande/avslutande `-` och kollapsa upprepade `-`

Skapa arbetskatalog: `./drafts/{slug}/`. Här sparas alla mellanresultat.

## Auto-mode beteende

När `$AUTO_MODE = true`:

- **Inga godkännande-pauser** mellan Steg 1→2→3→4→5
- **Slutrapport visas på en gång** efter Steg 5, inklusive sammanfattning av varje mellansteg
- **Kritiska stoppvillkor** som ändå avbryter flödet:
  - Färre än 3 framgångsrika WebFetch/Invoke-WebRequest i Steg 1
  - Termtäckning i Steg 5 är <60 % (flaggas men flödet fortsätter och rapporteras)
  - HTTP 5xx-fel på primärkällor och alla fallbacks
- **Statusuppdateringar** under flödets gång: en kort rad mellan stegen ("Steg 1 klar, 10/10 fetched. Startar Steg 2.")

När `$AUTO_MODE = false` följs normala godkännandepauser enligt varje steg.

## Steg 1 — Term-extraktion (NeuronWriter-stil)

**Mål:** Skapa en kvantitativ vokabulärguide (`terms.json`) baserad på vad konkurrenterna i topp 10 SERP faktiskt skriver.

**Gör så här:**

1. **WebSearch** med sökordet. Plocka ut **de 10 högst rankade organiska resultaten**.

2. **Kopiera rätt fetch-script** till `./drafts/{slug}/` baserat på plattform. Båda scripten är funktionellt likvärdiga och producerar samma fyra filer per URL: `title_NN.txt`, `h1_NN.txt`, `h2_NN.txt`, `raw_NN.txt`.

   **Plattformsval:** kontrollera Claude Codes systemprompt — den anger "Platform: win32" / "darwin" / "linux".

   **På Windows** (PowerShell tillgängligt som default):
   ```powershell
   Copy-Item "$env:USERPROFILE\.claude\skills\semantic-stack\scripts\fetch.ps1" ".\drafts\{slug}\fetch.ps1"
   ```
   Anrop per URL: `& .\drafts\{slug}\fetch.ps1 -Url "URL" -OutDir ".\drafts\{slug}" -Id "01"`

   **På macOS/Linux** (Bash + curl + perl, alla preinstallerade):
   ```bash
   cp ~/.claude/skills/semantic-stack/scripts/fetch.sh ./drafts/{slug}/fetch.sh
   chmod +x ./drafts/{slug}/fetch.sh
   ```
   Anrop per URL: `./drafts/{slug}/fetch.sh "URL" "./drafts/{slug}" "01"`

   Om varken PowerShell eller Bash+perl är tillgängligt, fall tillbaka direkt på Playwright MCP eller WebFetch för varje URL (kvalitet sjunker eftersom H1/H2-strukturen inte fångas).

3. **Kör fetch parallellt för alla 10 URLs.** För varje URL skapas fyra filer: `title_NN.txt`, `h1_NN.txt`, `h2_NN.txt`, `raw_NN.txt`.

   **Fallback per URL** vid HTTP-fel eller tunt innehåll (<200 ord): Playwright MCP → WebFetch som sista utväg.

   **Stoppregel:** >3 misslyckanden → i step-by-step pausa och fråga; i auto-mode flagga och försök slutföra med vad som finns.

4. **Läs in alla title_*, h1_*, h2_* och raw_*-filer** i din kontext.

5. **Bygg `./drafts/{slug}/terms.json`** i exakt NeuronWriter-format. Referensexempel ligger i `~/.claude/skills/semantic-stack/references/`:
   - `neuronwriter-example-1.json` — skatteämne (reavinstskatt)
   - `neuronwriter-example-2.json` — personbiografi (Andreas Ravelli)
   - `neuronwriter-example-3.json` — komplext samhällsämne (assisterat självmord Schweiz)

   Läs minst ett av dessa innan du bygger terms.json för att kalibrera mängd och format. Strukturen:

   ```json
   {
     "title_terms": ["term1", "term2", "..."],
     "h1_terms": ["term1", "term2", "..."],
     "h2_terms": ["term1", "term2", "..."],
     "basic_terms": [
       {"term1": {"min": 1, "max": 5}}
     ],
     "extended_terms": [
       {"längre fras 1": {"min": 1, "max": 2}}
     ]
   }
   ```

   **Regler för termurval:**

   | Sektion | Innehåll | Krav |
   | :--- | :--- | :--- |
   | `title_terms` | Termer från `<title>` på minst **2 av 10** sidor | Sorterat efter frekvens, gemener |
   | `h1_terms` | Termer från `<h1>` på minst **2 av 10** sidor | Sorterat efter frekvens, gemener |
   | `h2_terms` | Termer från `<h2>` på minst **2 av 10** sidor | Sorterat efter frekvens, gemener |
   | `basic_terms` | 1–2 ords-termer i minst **3 av 10** källor | `min` = lägsta antal förekomster i någon källa, `max` = högsta |
   | `extended_terms` | 2–7 ords-fraser i minst **2 av 10** källor | Samma min/max-logik |

   **Måluppfyllnad:** 5–15 title, 8–20 h1, 10–25 h2, 20–40 basic, 60–100 extended.

6. **BEHÅLL alla mellanfiler** (`title_*`, `h1_*`, `h2_*`, `raw_*`) — Steg 2 (Research) använder samma data.

7. **Pausa (step-by-step) eller fortsätt (auto-mode).** I båda fallen, visa en kort summering: antal URLs, antal termer per kategori, 5–10 mest centrala termer, 3–5 H2-rubriker konkurrenterna använder.

   I step-by-step: fråga "Godkänner du term-extraktionen och vill gå vidare till research?"
   I auto-mode: visa bara summeringen som statusrad och fortsätt direkt till Steg 2.

## Steg 2 — Research

**Mål:** Samla minst 5 relevanta källor i fulltext och syntetisera en omfattande researchsammanfattning.

**Gör så här:**

1. **Använd raw_*-filerna från Steg 1.** Ingen ny fetch behövs.

2. **Komplettera med 1–3 ytterligare primärkällor** om Steg 1 saknade myndighetskällor. Kör samma fetch-script med ny ID-numrering (raw_11, raw_12, …).

3. **Syntetisera `./drafts/{slug}/research.md` från fulltexterna.** Sikta på:
   - Konkreta paragrafhänvisningar (BrB 4 kap. 9a §, GDPR art. 6.1, etc.)
   - Direktcitat när slagkraftig formulering
   - Numerisk täthet (procent, datum, belopp, paragrafnummer)
   - Entitetsrik kartläggning

   Använd struktur:

   ```markdown
   # Research: {sökord}

   ## Källor
   - [Titel](url) — beskrivning + metod (Invoke-WebRequest/Playwright/WebFetch)

   ## Definitioner och huvudkoncept
   ## Statistik och siffror
   ## Entiteter
   ## Direktcitat (där relevant)
   ## Vanliga frågor (PAA-liknande)
   ## Vinklar och teman som konkurrenter täcker
   ## Luckor (vad konkurrenter missar)
   ## Vinkel för {sajt om angiven}
   ```

4. **Radera mellanfilerna** (`title_*`, `h1_*`, `h2_*`, `raw_*`, `fetch.ps1`) när research.md är klar. Behåll `terms.json` och `research.md`.

5. **Pausa (step-by-step) eller fortsätt (auto-mode).** Visa 3–5 punkter summering. I step-by-step fråga om godkännande.

## Steg 3 — Artikelplan (Rank2Bank)

**Mål:** Skapa en artikelplan som följer Korays semantiska SEO-principer och uppfyller minst 85 % av min-kraven i `terms.json`.

**Gör så här:**

1. Läs referensfilerna i `~/.claude/skills/semantic-stack/references/`:
   - `rank2bank-instructions.txt`, `rank2bank-35-points.md`, `rank2bank-course-notes.md`, `rank2bank-terms.md`

2. Läs `./drafts/{slug}/research.md` och `./drafts/{slug}/terms.json`.

3. Generera artikelplan och skriv till `./drafts/{slug}/plan.md`:

   ```markdown
   # Artikelplan: {sökord}

   ## Search Intent
   ## Contextual Vector
   ## Topical Map (entiteter och relationer)
   ## Föreslagen H1
   {ska innehålla sökordet + minst 2 termer från title_terms/h1_terms}

   ## SEO-description (150–160 tecken)
   {ska inkludera huvudsökordet + 1–2 termer från basic_terms}

   ## Rubrikhierarki (H2/H3)
   - ## H2 nr 1 — {rubrik}
     - ### H3 — ...
     - **Predikat/påstående:** ...
     - **Källor:** ...
     - **Termer från terms.json som täcks:** ...

   ## Frågor som måste besvaras

   ## Termtäckningsanalys (terms.json)
   - Title-termer planerade i H1: X av Y (Z %)
   - H1-termer planerade i H1: X av Y (Z %)
   - H2-termer planerade i H2:or: X av Y (Z %)
   - Basic-termer fördelade över sektioner: X av Y (Z %)
   - Extended-termer fördelade över sektioner: X av Y (Z %)
   - **Total min-täckning:** Z % (mål: ≥85 %)

   ## Interna länkar
   ## Längd och format
   ```

4. **Pausa (step-by-step) eller fortsätt (auto-mode).** I step-by-step visa plan och fråga om godkännande. Om termtäckning <85 %, justera planen innan du visar.

## Steg 4 — Skriv artikeln

**Mål:** Producera artikeln enligt Matyas svenska SEO-skrivriktlinjer och uppfylla minst 85 % av min-kraven i `terms.json`.

**Gör så här:**

1. Läs `~/.claude/skills/semantic-stack/references/matyas-seo-guidelines.md`.

2. Läs `./drafts/{slug}/research.md`, `./drafts/{slug}/plan.md` och `./drafts/{slug}/terms.json`.

3. Skriv artikeln till `./drafts/{slug}/draft.md`:
   - `# {H1 från planen}` — ingen frontmatter ännu
   - Följ rubrikhierarkin exakt
   - Tillämpa Matyas-principer (informationstäthet, direkta svar, faktabaserade satser, konkreta siffror, korta meningar, eliminera utfyllnad)
   - Inkludera basic_terms och extended_terms naturligt enligt min-kraven (mål ≥85 %)
   - Undvik stuffing
   - Inga AI-floskler ("Det är viktigt att notera", "Sammanfattningsvis", etc.)
   - **Inga interna länkar som default** (oavsett vad domän-detekteringen visar). Skapa aldrig påhittade URL:er till sajter du inte verifierat existerar. Undantag: om användarens projektpreset eller intake explicit har `interna_lankar: true` — då får du föreslå internlänkar men markera dem som platshållare (`<!-- TODO: verifiera URL -->`) som användaren manuellt verifierar.

4. **Pausa (step-by-step) eller fortsätt (auto-mode).** I step-by-step säg "Artikeln är skriven ({X} ord). Vill du läsa innan jag skapar slutfilen?"

## Steg 5 — Slutfil med frontmatter

**Mål:** Producera den slutgiltiga `.md`-filen och rapportera termtäckning.

**Gör så här:**

1. Generera frontmatter (title från H1, description 150–160 tecken, date i ISO-format).

2. Bygg slutfilen (frontmatter + draft.md).

3. Spara till `{output-mapp}/{slug}.md`.

4. **Verifiera termtäckning** mot `terms.json`. Räkna förekomster, beräkna:
   - Andel min-krav uppfyllda
   - Andel max-krav överskridna (stuffing-varning)
   - Andel title/h1/h2-termer i motsvarande rubriker

5. **Rapportera till användaren.** Slutrapporten innehåller:
   - Sökväg, ordlängd, H2/H3, description-längd
   - **Termtäckningsrapport**:
     - title_terms i H1: X / Y
     - h1_terms i H1: X / Y
     - h2_terms i H2:or: X / Y
     - basic_terms min-uppfyllda: X / Y (Z %)
     - extended_terms min-uppfyllda: X / Y (Z %)
     - **Total min-täckning:** Z %
   - Varningar (om <85 % täckning, om max överskrids, om rubriker saknas, om sökord ovanligt få/många)

   I **auto-mode** inkluderar slutrapporten även en kort sammanfattning av Steg 1, 2 och 3 (vad som producerades), eftersom användaren inte sett mellanresultaten.

6. **Cleanup-fråga:** i step-by-step fråga om `drafts/{slug}/` ska behållas eller raderas. I auto-mode rapportera bara att den är behållen och kan raderas med ett enkelt kommando.

## Batch-körning (N artiklar)

När användaren ber om flera artiklar i ett svep — t.ex. "skriv alla 22 F1-förare" — gäller dessa regler:

### Planering
1. Lista alla entiteter med slug. Visa listan och be om bekräftelse (step-by-step) eller visa som statusrad (auto-mode).
2. Estimera tidsåtgång: ~15-20 min per entitet med fullt flöde. Kommunicera detta tydligt.
3. Fråga om prioritering: vilka entiteter är viktigast? Börja med dem.

### Körning
- Kör Steg 1–5 **per entitet, sekventiellt**. Parallellisera ALDRIG artikelskrivandet utan research.
- Enda tillåtna parallellisering: HTTP-fetches inom Steg 1 för en enskild entitet (de 10 URL-fetcharna).
- Spara varje färdig slutfil innan du går vidare till nästa entitet.
- Rapportera progress: "Entitet 3/22 klar: carlos-sainz-jr.md (1847 ord, 84% termtäckning)."

### Om batch-storleken är för stor
- Om N > 10 och auto-mode: kör de första 5 entiteterna, pausa och visa sammanfattning. Fråga om fortsättning.
- Om N > 20: dela upp i sessioner. Kommunicera detta till användaren hellre än att ta genvägar.
- Det är aldrig tillåtet att kompromissa med Steg 1 för att hinna fler entiteter per session.

### Subagentdelegering vid batch
Om subagenter används för att parallellisera batch-körning:
- Varje subagent ansvarar för **ett fåtal entiteter** (1–3), inte 10+.
- Subagentens prompt MÅSTE innehålla: sökord, instructions att köra fullt Steg 1–5, output-mapp, frontmatter-schema.
- Subagenten FÅR INTE få en bullet-lista med fakta och ombeds "skriva en artikel". Det är inte semantic-stack — det är fri generering utan research.
- Moderagenten verifierar varje subagents output: kontrollera att `terms.json` skapades och att termtäckning är ≥85 % innan filen godkänns.

## Fel- och edge cases

- **WebSearch ger få resultat:** prova alternativa formuleringar. Berätta om källskörden är tunn.
- **Invoke-WebRequest HTTP 4xx/5xx eller tunn text:** fallback-kedja (Playwright → WebFetch).
- **JS-renderad sida** (Riksbanken etc.): hoppa direkt till Playwright. Notera att Playwright inte ger ren H1/H2-struktur.
- **>3 källor i rad misslyckas:** i step-by-step pausa, i auto-mode flagga men fortsätt.
- **Term-extraktion <7 framgångsrika källor:** kommunicera tunnare data.
- **Total min-täckning <85 % efter Steg 4:** flagga tydligt i Steg 5-rapporten med lista över missade termer. I step-by-step erbjud revidering, i auto-mode bara rapportera.
- **Termtäckning >max på flera termer:** stuffing-risk. Flagga, men notera att max ofta överskrids naturligt för längre artiklar (mätningen är frekvens-baserad, inte densitet-baserad).
- **Engelska/annat språk-sökord:** fråga om språk. Default svenska om sökordet är svenskt eller flerspråkigt.
- **Output-mappen saknas:** skapa den.
- **Fil i `drafts/{slug}/` finns:** fråga om överskrivning eller suffix (`_v2`, `_v3`).
- **Preset.json är korrupt JSON:** logga felet, fall tillbaka till memory eller fresh intake.
- **Kontextkostnad:** 100 000–300 000 tokens för 10 sidor + struktur. Inom 1M men håll dig medveten.

## Sammanfattning av flödet

| Steg | Output-fil | Pausa step-by-step? | Pausa auto-mode? |
|------|------------|--------|--------|
| Intake | (preset.json / .last-context.json) | Ja (1 fråga) | Ja (1 fråga) |
| 1. Term-extraktion | `drafts/{slug}/terms.json` (+ raw-filer för Steg 2) | Ja | Nej (statusrad) |
| 2. Research | `drafts/{slug}/research.md` | Ja | Nej (statusrad) |
| 3. Artikelplan | `drafts/{slug}/plan.md` | Ja | Nej (statusrad) |
| 4. Artikel (utan frontmatter) | `drafts/{slug}/draft.md` | Ja | Nej (statusrad) |
| 5. Slutfil + termtäckningsrapport | `{output-mapp}/{slug}.md` | Slutrapport | Slutrapport (utökad) |

## Anmärkning om term-extraktionens begränsning

Min term-extraktion är en **approximation** av NeuronWriter och liknande NLP-baserade verktyg:

- Riktig NLP-extraktion (spaCy, BERT) identifierar entiteter med högre precision
- Min frekvensanalys är manuell n-gram-räkning, inte morfologisk lemmatisering
- Min/max-frekvenserna är estimat, inte exakta percentiler

För produktion av kommersiella SEO-artiklar bör term-extraktionen verifieras med dedikerat NLP-verktyg.
