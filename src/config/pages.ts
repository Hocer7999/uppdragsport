// =====================================================================
// PAGES CONFIG — declarative section composition per siteType.
// ---------------------------------------------------------------------
// Edit these arrays (or override at the page level) to change what
// appears on the homepage / about page. The active export depends on
// siteConfig.siteType (set in src/config/site.ts).
//
// To add a new section: import it via the registry (src/lib/sectionRegistry.ts)
// then reference it here by name (the registry key).
// =====================================================================

import type { SectionConfig } from "../lib/sectionRegistry";
import { siteConfig } from "./site";

// --- Service homepage (lokala företag, tjänstesajter) -----------------
// Default-flödet är medvetet trimmat. Två sektioner är AVSIKTLIGT borttagna:
//   - Stats: "20+ år / 5000+ kunder / 4,9 betyg" är ett generiskt anti-pattern
//     som signalerar "klinikkedja/mallsajt" snarare än premium-varumärke.
//     Lägg in manuellt (`{ type: "Stats", ... }`) bara om klienten har
//     specifika, verifierbara siffror som faktiskt differentierar dem.
//   - Kommun: chip-grid med stadsdelar/kommuner ser ut som tag-cloud från
//     2012 och skadar premium-positionering. Lägg in manuellt om sajten
//     verkligen behöver lokal SEO via flera service-områden.
// Båda komponenterna finns kvar i sectionRegistry — bara default-listan
// utelämnar dem så nybygges inte ärver "billigt"-känslan.
export const serviceHomepageSections: SectionConfig[] = [
    { type: "Hero" },
    { type: "Features" },
    { type: "Services" },
    { type: "ContentBlock", props: {
        title: "Om oss",
        text: [
            "Beskriv kort vad ni gör och varför kunder väljer er.",
            "Lägg till en andra paragraf med konkret nytta för kunden.",
        ],
        image: "/images/om-oss.webp",
        imageAlt: "Sektionsbild",
    } },
    { type: "Steps" },
    { type: "CTA" },
    { type: "FAQ" },
    { type: "Contact" },
];

// --- Content homepage (Uppdragsport — Stadium Noir sportmagasin) -------
// Bespoke högenergi-flöde: helbleed-hero → live score-ticker → senaste
// nyheterna (auto-genererade) → sporterna → magasinsartiklar → bildreportage
// → editorial → nyhetsbrev → redaktion.
export const contentHomepageSections: SectionConfig[] = [
    { type: "HeroStadium" },
    { type: "ScoreTicker" },
    { type: "AdBanner", props: {
        image: "/images/ads/unibet.webp", brand: "Unibet", accent: "#15a34a",
        tagline: "Spela på Allsvenskan – oddsboost varje helg.", cta: "Spela nu",
    } },
    { type: "NewsPortal", props: { title: "Allt just nu" } },
    { type: "CategoryGrid", props: {
        title: "Sporterna",
        description: "Välj din arena. Vi täcker bollsport, is och bana — från elitserien till friidrottens VM-finaler.",
    } },
    { type: "AdBanner", props: {
        image: "/images/ads/betsson.webp", brand: "Betsson", accent: "#ff7a00",
        tagline: "Live-odds på alla matcher, direkt i mobilen.", cta: "Hämta erbjudande",
    } },
    { type: "MomentsFilmstrip" },
    { type: "EditorialQuote" },
    { type: "Newsletter", props: {
        title: "Missa inget avspark",
        description: "Veckans bästa analyser och reportage, samlade i ett mejl. Ingen reklam — bara sport.",
        buttonText: "Prenumerera",
    } },
    { type: "AuthorList", props: {
        title: "Redaktionen",
        description: "Skribenterna som följer matcherna så att du slipper.",
    } },
];

// --- Directory homepage (faktasajter, encyclopedia, programmatic SEO) -
export const directoryHomepageSections: SectionConfig[] = [
    { type: "HeroSearch", props: {
        title: "Sök i kunskapsbasen",
        subtitle: "Faktasidor, definitioner och guider — sökbart innehåll i ett.",
    } },
    { type: "CategoryGrid" },
    { type: "ContentBlock", props: {
        title: "Vad är detta?",
        text: [
            "Beskriv vad sajten innehåller och vem den är till för.",
            "Beskriv hur datat samlats in och hur det uppdateras.",
        ],
        image: "/images/om-oss.webp",
        imageAlt: "Sektionsbild",
    } },
    { type: "Stats" },
];

// --- Default homepage selection ---------------------------------------
export const homepageSections: SectionConfig[] =
    siteConfig.siteType === "content"
        ? contentHomepageSections
        : siteConfig.siteType === "directory"
            ? directoryHomepageSections
            : serviceHomepageSections;

// --- About page (gemensam — fungerar för alla siteTypes) --------------
// Stats avsiktligt utelämnat — se kommentar vid serviceHomepageSections.
export const aboutPageSections: SectionConfig[] = [
    { type: "ContentBlock", props: {
        title: "Om Uppdragsport",
        text: [
            "Uppdragsport är en svensk sportblogg byggd för dig som vill ha mer än siffrorna i tabellen. Vi bevakar fotboll, hockey, innebandy, friidrott och längdskidor — med analyser, reportage och nyheter som uppdateras dygnet runt.",
            "Vi tror att en match aldrig bara är resultatet. Det är historien runt omkring: formkurvan, taktiken, känslan på läktaren. Vårt uppdrag är att fånga det, oavsett om det handlar om en Allsvensk derbykväll eller en VM-final på skidor.",
        ],
        image: "/images/om-oss.webp",
        imageAlt: "Mörk arena upplyst av strålkastare inför avspark",
    } },
    { type: "EditorialQuote", props: {
        eyebrow: "Vårt löfte",
        quote: "Vi skriver om sport som om den betyder något. För den gör det.",
        attribution: "Redaktionen, Uppdragsport",
    } },
    { type: "CTA" },
];
