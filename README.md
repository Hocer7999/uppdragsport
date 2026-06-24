# Bombus Astro Boilerplate 🚀

Välkommen till **Bombus Astro Boilerplate** – en modern, blixtsnabb och skalbar grund för att bygga webbplatser med [Astro](https://astro.build).

Detta projekt är designat för att vara **extremt konfigurerbart** och **återanvändbart**. Med en centraliserad konfiguration kan du snabbt anpassa design, innehåll och funktionalitet för nya projekt utan att behöva gräva djupt i koden.

## 📦 Innehåll

- [Funktioner](#funktioner)
- [Kom igång](#kom-igång)
- [Projektstruktur](#projektstruktur)
- [Konfiguration](#konfiguration-viktigt)
- [Design & Tema](#design--tema)
- [Komponenter](#komponenter)
- [Artiklar & Blogg](#artiklar--blogg)
- [SEO & Meta](#seo--meta)

![Exampelsida](https://github.com/aliasnille/bombus-boilplate/blob/main/example-page.png)

---

## Funktioner

*   ⚡ **Astro v5**: Blixtsnabb prestanda med Islands Architecture.
*   🎨 **Tailwind CSS v4 & DaisyUI v5**: Mordern styling och enkla teman.
*   ⚙️ **Centraliserad Konfiguration**: Styr allt från `src/config/`.
*   🧩 **Färdiga Sektioner**: Hero, Features, Pricing, FAQ, Kontaktformulär m.m.
*   📝 **Blogg/Artiklar**: Inbyggt stöd med Astro Content Collections.
*   ⚖️ **Juridiska Sidor**: Automatiska GDPR-anpassade integritets- och cookiepolicy-sidor.
*   🔍 **SEO-optimerad**: Inbyggt stöd för meta-taggar, Open Graph, Sitemap och Schema mark-up.

---

## Kom igång

### Förutsättningar
Du behöver ha **Node.js** installerat på din dator.

### Installation

1.  Klonan projektet eller ladda ner ZIP-filen.
2.  Installera enligt nedan:

```bash
npm install
```

### Kör utvecklingsservern

Starta den lokala servern och se projektet live på `http://localhost:4321`:

```bash
npm run dev
```

### Bygg för produktion

Skapa en optimerad version av webbplatsen redo för uppladdning:

```bash
npm run build
```

---

## Projektstruktur

Här är en överblick över de viktigaste mapparna:

```text
src/
├── components/     # Alla UI-komponenter
│   ├── layout/     # Header, Footer, CookieConsent
│   ├── sections/   # Färdiga sektioner (Hero, Pricing, etc.)
│   └── seo/        # SEO-relaterade komponenter
├── config/         # ⚡ ALL KONFIGURATION HÄR (Se nedan)
├── content/        # Markdown-filer för artiklar/blogg
├── layouts/        # Huvudlayouten (Layout.astro)
├── pages/          # Webbplatsens sidor (.astro-filer)
└── styles/         # Global CSS
```

---

## Konfiguration (VIKTIGT) ⚙️

Styrkan i detta boilerplate ligger i mappen `src/config/`. Här kan du ändra det mesta utan att röra komponentkoden.

### 1. Företagsinfo (`src/config/company.ts`)
Här ställer du in all information om företaget. Detta används automatiskt i footern, kontaktsidor och de juridiska policysidorna.
*   **Namn, domän, e-post, telefon**
*   **Adressuppgifter**
*   **Sociala medier-länkar**
*   **Serviceområden** (lista på städer)
*   **Länkar i header och footer**

### 2. Webbplatsinställningar (`src/config/site.ts`)
Styr det visuella uttrycket.
*   **theme**: Välj tema (t.ex. `emerald`, `light`, `dark`, `corporate`). Baserat på DaisyUI ([https://daisyui.com/docs/themes/](https://daisyui.com/docs/themes/)).
*   **font**: Välj typsnitt (`inter`, `dm-sans`, `manrope`).

### 3. Priser (`src/config/pricing.ts`)
Konfigurera dina prispaket och jämförelsetabeller.
*   Lägg till/ta bort paket (Gratis, Plus, Premium, etc.).
*   Justera priser och funktioner.
*   Paketen renderas automatiskt i `Pricing.astro` och `PricingCards.astro`.

### 4. Frågor & Svar (`src/config/faq.ts`)
Lägg till dina vanliga frågor här så dyker de upp i FAQ-komponenterna.

---

## Design & Tema

Projektet använder **Tailwind CSS v4** och **DaisyUI v5**.

### Byta färger
Öppna `src/config/site.ts` och ändra `theme` till något av DaisyUI:s teman (eller skapa ett eget i CSS).
Exempel: `theme: "corporate"`, `theme: "cupcake"`, `theme: "dark"`.

### Byta typsnitt
Öppna `src/config/site.ts` och ändra `font` till:
*   `inter`
*   `dm-sans`
*   `manrope`

Dessa laddas automatiskt via @fontsource i `global.css`.

---

## Komponenter

I `src/components/sections/` hittar du alla byggstenar. Du importerar och använder dem i dina sidor (t.ex. `index.astro`) så här:

```astro
---
import Hero from '../components/sections/Hero.astro';
import Features from '../components/sections/Features.astro';
---

<Layout title="Min Hemsida">
  <Hero />
  <Features />
</Layout>
```

**Tillgängliga sektioner:**
*   `Hero`, `HeroCentered`, `HeroSubpage`
*   `Features`
*   `Pricing`, `PricingCards`
*   `FAQ`, `FAQWithSidebar`
*   `Contact`, `MultiStepForm`
*   `Stats`, `GraphSection`
*   `ContentBlock` (för allmän text)
*   ...och fler under `src/components/sections/`

![Sektioner](https://github.com/aliasnille/bombus-boilplate/blob/main/components.png)

---

## Artiklar & Blogg 📝

Bloggen drivs av **Astro Content Collections**.

1.  Lägg till dina artiklar som `.md`-filer i mappen: `src/content/articles/`
2.  Varje fil måste ha "frontmatter" (metadata) högst upp:

```markdown
---
title: "Min första artikel"
description: "En kort sammanfattning..."
publishDate: 2024-03-20
author: "Ditt Namn"
image: "/images/artikel-bild.jpg"
category: "Nyheter"
featured: true
---

Här skriver du din artikel med vanlig Markdown...
```

Dina artiklar dyker automatiskt upp på `/artiklar` och får en egen sida.

---

## SEO & Meta 🔍

Projektet har inbyggt stöd för SEO.

I `src/layouts/Layout.astro` hanteras:
*   **Canonical URL** (automatiskt)
*   **Open Graph** (för Facebook/LinkedIn delning)
*   **Twitter Cards**
*   **Schema.org** (JSON-LD)

För att anpassa SEO för en specifik sida, skicka med props till Layouten:

```astro
<Layout 
  title="Specifik Sidtitel" 
  description="En unik beskrivning för denna sida för Google."
  image="/bild-för-delning.jpg"
>
  ...
</Layout>
```

---

## Juridik ⚖️

Sidorna `/cookiepolicy` och `/integritetspolicy` genereras automatiskt baserat på informationen i `src/config/company.ts`. Se till att fylla i korrekt företagsnamn och kontaktuppgifter där för att dessa sidor ska bli giltiga.
