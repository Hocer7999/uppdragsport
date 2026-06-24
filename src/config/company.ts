// =====================================================================
// COMPANY CONFIG — single source of truth for Uppdragsport.
// All canonical/JSON-LD/sitemap/robots derive from this file.
// =====================================================================

export const companyConfig = {
    // --- Identity -----------------------------------------------------
    name: "Uppdragsport",
    domain: "uppdragsport.se", // no protocol, no trailing slash
    logo: "/logo.png",
    email: "info@uppdragsport.se",
    description: "Uppdragsport — svensk sport på djupet. Nyheter, analyser och reportage om fotboll, hockey och allt däremellan, dygnet runt.",

    // --- Address & legal ---------------------------------------------
    // Content-sajt: ingen fysisk adress / org.nr / telefon.
    address: "",
    postalCode: "",
    city: "",
    country: "Sverige",
    phone: "",
    orgNumber: "",

    // --- Analytics ----------------------------------------------------
    googleAnalyticsId: "", // empty disables GA

    // --- Social (leave URL empty to omit from JSON-LD sameAs) --------
    socialMedia: {
        twitter: "",
        linkedin: "",
        facebook: "",
        instagram: "",
    },

    // --- Service areas (ej relevant för content-sajt; behålls tomt) --
    serviceAreas: [],

    // --- Stats (ej använt på content-startsidan) ---------------------
    stats: [],

    // --- Navigation ---------------------------------------------------
    headerLinks: [
        { text: "Nyheter", href: "/nyheter" },
        { text: "Artiklar", href: "/artiklar" },
        { text: "Fotboll", href: "/kategori/fotboll" },
        { text: "Hockey", href: "/kategori/hockey" },
        { text: "Om oss", href: "/om-oss" },
    ],
    footerLinks: [
        {
            title: "Innehåll",
            links: [
                { text: "Sportnyheter", href: "/nyheter" },
                { text: "Alla artiklar", href: "/artiklar" },
                { text: "Fotboll", href: "/kategori/fotboll" },
                { text: "Hockey", href: "/kategori/hockey" },
                { text: "Innebandy", href: "/kategori/innebandy" },
                { text: "Friidrott & skidor", href: "/kategori/friidrott-och-skidor" },
            ],
        },
        {
            title: "Om oss",
            links: [
                { text: "Om Uppdragsport", href: "/om-oss" },
                { text: "Nyhetsbrev", href: "/#nyhetsbrev" },
                { text: "RSS-feed", href: "/rss.xml" },
            ],
        },
        {
            title: "Juridik",
            links: [
                { text: "Integritetspolicy", href: "/integritetspolicy" },
                { text: "Cookiepolicy", href: "/cookiepolicy" },
            ],
        },
    ],

    lastUpdated: new Date().toLocaleDateString('sv-SE', { year: 'numeric', month: 'long', day: 'numeric' }),
};
