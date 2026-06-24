---
name: new-site
description: "Initiera mallen för en ny sajt: byter ut företagsdata, domän, branschspecifikt innehåll, nollställer artiklar och säkerställer SEO-grunder (canonical, trailing slash, robots, sitemap). Använd när användaren startar ett nytt bygge i Bombus Astro-mallen (säger 'ny sajt', 'starta projekt', 'sätt upp X för Y', 'byt företag till X')."
risk: safe
---

# new-site

Initierar Bombus Astro-mallen för en ny kund/nisch. Mallen är byggd för att återanvändas — det här är den deterministiska checklistan som säkerställer att ingen rest från föregående bygge följer med.

## När den ska användas

Använd när användaren:
- vill starta ett nytt sajt-bygge i denna mall
- nämner ett nytt företag, en ny domän eller en ny nisch som mallen ska anpassas för
- ber dig "rensa mallen" eller "byta företag"

## Resurser i projektet

- **`.env` i projektroten** — innehåller `FAL_KEY` för bildgenerering via fal.ai. Säkerhetskopiera ALDRIG denna fil till git (redan i `.gitignore`). Om filen saknas i ett nytt bygge, fråga användaren innan du fortsätter med bildsteg.
- **`fal-generate`-skillet** — använd för att generera hero-bilder, artikelbilder, sektionsbilder och OG-bilder. Anropa det när du behöver en bild istället för Unsplash-placeholders. Skickas API-nyckeln från `.env` (skillet läser `FAL_KEY` från miljön).
  - **Modell: ALLTID `openai/gpt-image-2` på `quality: "low"`** (endpoint: `https://fal.ai/models/openai/gpt-image-2`). Använd INTE Flux — det är en äldre och dyrare modell som `fal-generate` annars tenderar att default:a till. Sätt modellen explicit i varje anrop.
- **`ui-ux-pro-max`-skillet** — använd för designval (tema, paletter, typsnitt, sektion-layouts) innan du börjar skriva komponentkod för en ny nisch.

## Steg

### 0. Rensa byggartefakter (om kloning skedde manuellt)

```bash
rm -rf dist .astro node_modules
npm install
```

Klonas via git är detta inte nödvändigt — `.gitignore` exkluderar dem.

### 1. Samla in en brief
Fråga användaren (i en omgång — använd AskUserQuestion om tillgängligt) efter:
- **Företagsnamn** (`name`)
- **Domän** (utan `https://`, ingen trailing slash — t.ex. `mittforetag.se`)
- **Bransch/nisch** (en mening — används för att forma copy och artiklar)
- **Kort beskrivning** (~150 tecken, blir default meta description)
- **E-post**, **telefon**, **adress**, **postnr**, **stad**, **org.nr**
- **DaisyUI-tema** (default: `corporate`. Alternativ: `emerald`, `cupcake`, `dark`, `light`, `bumblebee`, m.fl. — se daisyui.com/docs/themes)
- **Typsnitt** (`inter`, `dm-sans` eller `manrope`)
- **Sociala konton** (URLs eller blank — blanka filtreras bort från JSON-LD)
- **Service-områden** (lista städer — kan behållas som default Sverige-städer)
- **Google Analytics ID** (valfritt)

Om något är okänt: lämna fältet som tom sträng — gå INTE vidare med påhittade värden.

### 2. Skriv `src/config/company.ts`
Använd briefen. Sätt `domain` exakt som angiven (utan protokoll, utan trailing slash). Allt annat (canonical, JSON-LD, sitemap, robots.txt) deriveras automatiskt från denna fil.

### 3. Skriv `src/config/site.ts`
Sätt `theme` och `font` enligt briefen.

### 4. Anpassa branschspecifikt innehåll
Dessa filer innehåller TODO-markerade platshållare som måste skrivas om per nisch:
- `src/pages/index.astro` — saknar ContentBlock-sektioner; lägg in 2–3 nya per nisch
- `src/pages/om-oss.astro` — historia/mission/vision TODO
- `src/components/sections/Hero.astro` — default-props (title, subtitle, badge) bör överrides från `index.astro`
- `src/config/faq.ts` — generiska FAQ; byt mot nisch-FAQ
- `src/config/pricing.ts` — generiska SaaS-paket; anpassa eller ersätt
- `src/components/sections/Services.astro`, `Features.astro`, `InfoCards.astro`, `Steps.astro`, `CTA.astro`, `Stats.astro`, `StatsAlt.astro` — granska och uppdatera hårdkodad copy

### 5. Generera artiklar (valfritt)
`src/content/articles/` ska vara tom från start. Lägg till 3–5 nisch-relevanta artiklar i Markdown med korrekt frontmatter (se `src/content/config.ts` för schemat). Datum måste vara ISO-strängar.

**Artikelbilder via fal.ai:** för varje artikel, generera en hero-bild med `fal-generate`-skillet.
- API-nyckel: `FAL_KEY` i `.env` i projektroten.
- **Modell: ALLTID `openai/gpt-image-2` med `quality: "low"`** (https://fal.ai/models/openai/gpt-image-2). Använd inte Flux — det är dyrare och äldre.
- Spara bilderna i `public/images/articles/<slug>.webp`.
- Referera från artikelns frontmatter: `image: "/images/articles/<slug>.webp"` och sätt `imageAlt` med en beskrivande svensk text.
- Prompt-tips: skriv prompten på engelska, beskriv stilen (t.ex. "clean editorial illustration, soft pastel palette, no text"), undvik bokstäver/logotyper i bilden. Matcha visuell stil mellan artiklar för konsistens.

Frontmatter-checklista per artikel:
- `title`, `description`, `publishDate` (ISO), `author`, `category` — obligatoriska
- `metaTitle`, `metaDescription` — sätt om de ska skilja från `title`/`description`
- `image`, `imageAlt` — använd fal-genererad bild
- `faq` — array med 3–5 nisch-frågor → renderas som FAQPage JSON-LD automatiskt

### 6. Logotyp och bilder
- Byt ut `public/dummy-logo.svg` mot riktig logo (behåll filnamn ELLER uppdatera `companyConfig.logo`).
- Byt ut favicon-filerna i `public/` (`favicon.svg`, `favicon-16x16.png`, `favicon-32x32.png`, `apple-touch-icon.png`, `android-chrome-*`).
- Uppdatera `public/site.webmanifest` med korrekt namn och färger.
- **Bildgenerering**: anropa `fal-generate`-skillet för hero-, artikel- och sektionsbilder. API-nyckeln (`FAL_KEY`) finns i `.env` i projektroten. **Använd alltid modell `openai/gpt-image-2` med `quality: "low"`** — inte Flux. Spara genererade bilder i `public/images/` och referera med absoluta paths (`/images/hero.webp`). Använd inte Unsplash-länkar i produktion — byt ut de som finns kvar i komponenterna.

### 7. SEO-säkring (redan inbyggt — verifiera bara)
Följande är redan strukturellt löst i mallen — kontrollera bara att de fungerar:
- ✅ `trailingSlash: 'never'` i `astro.config.mjs`
- ✅ `build.format: 'file'` (genererar `/om-oss.html` istället för `/om-oss/index.html`)
- ✅ Canonical i `src/layouts/Layout.astro` strippar trailing slash via regex
- ✅ JSON-LD `@id`/`url` byggs via `canonical()`-helper i `src/utils/jsonLD.ts`
- ✅ `astro.config.mjs site:` importeras från `companyConfig.domain` — bara en sanning för domänen
- ✅ `/robots.txt` genereras dynamiskt från samma källa (`src/pages/robots.txt.ts`)
- ✅ Sitemap genereras automatiskt via `@astrojs/sitemap`
- ✅ **Taggsidor (`/tag/[slug]`) är `noindex, follow` OCH uteslutna ur sitemapen.** Taggsidor är tunna/dubblerade (ofta 1 artikel styck) och ska aldrig indexeras. Mallen löser detta på två ställen; verifiera att båda finns kvar om du rört `astro.config.mjs` eller tag-routen:
  - `astro.config.mjs`: `sitemap({ filter: (page) => !/\/tag\//.test(page) })`
  - `src/pages/tag/[slug].astro`: `<Layout ... robots="noindex, follow">`

### 8. Slutverifiering — KÖR ALLTID

```bash
npm install   # om dependencies inte är installerade
npm run build
```

Granska build-outputen:
- Inga TypeScript-fel
- Sitemap genererad i `dist/sitemap-index.xml` med rätt domän
- `dist/robots.txt` pekar på rätt sitemap-URL
- Stickprov: öppna `dist/index.html` och verifiera `<link rel="canonical">` utan trailing slash, `og:url` matchar, JSON-LD `@id` matchar canonical

### 9. Grep efter rester
Kör en sista koll på vanliga leftover-mönster:

```
grep -ri "corpia\|logoipsum\|TODO" src/
```

Alla träffar måste antingen vara medvetna TODOs eller åtgärdas.

## Vanliga fallgropar att undvika

1. **Hardkodad copy i sektioner** — flera komponenter (Hero, Services, FAQ:s sidebar tidigare) hade nisch-specifik svensk text. Gå alltid igenom alla `src/components/sections/*.astro`.
2. **Två källor för domän** — sätt ALDRIG site-URL direkt i `astro.config.mjs`. Den läses från `companyConfig.domain`.
3. **Trailing slash i interna länkar** — använd alltid `/om-oss`, aldrig `/om-oss/`. `trailingSlash: 'never'` gör att andra varianten ger 404.
4. **Glömda exempel-artiklar** — `src/content/articles/` ska vara tom efter rensning; gamla artiklar dyker upp i sitemap.
5. **Dummy-logo i OG-image** — `Layout.astro` har `image = "/dummy-logo.svg"` som default. Byt logo-filen eller props per sida.

## Output

När alla steg är klara, rapportera:
- Domän, företagsnamn, tema
- Antal sidor i sitemap (från `dist/sitemap-0.xml`)
- Antal artiklar
- Kvarvarande TODOs i koden (grep-resultat)
- Build-status (passed/failed)
