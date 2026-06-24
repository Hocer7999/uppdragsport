export interface Feature {
    text: string;
    included: boolean;
}

export interface ComparisonRow {
    feature: string;
    keys: {
        [key: string]: string | boolean;
    };
}

export interface Package {
    id: string; // unique identifier for mapping
    name: string;
    subtitle: string;
    price: string;
    originalPrice?: string;
    badge?: string;
    features: Feature[];
    ctaText: string;
    isFeatured?: boolean;
}

export const defaultPackages: Package[] = [
    {
        id: "free",
        name: "Gratis",
        subtitle: "För dig som vill testa",
        price: "0 kr",
        originalPrice: "",
        features: [
            { text: "1 användare", included: true },
            { text: "1GB lagring", included: true },
            { text: "Community-support", included: true },
            { text: "Daglig backup", included: false },
            { text: "API-tillgång", included: false },
        ],
        ctaText: "Kom igång gratis",
        isFeatured: false,
    },
    {
        id: "plus",
        name: "Plus",
        subtitle: "För professionella användare",
        price: "299 kr",
        originalPrice: "399 kr",
        badge: "Populärast",
        features: [
            { text: "Upp till 5 användare", included: true },
            { text: "50GB lagring", included: true },
            { text: "Prioriterad support", included: true },
            { text: "Daglig backup", included: true },
            { text: "API-tillgång", included: true },
        ],
        ctaText: "Uppgradera till Plus",
        isFeatured: true,
    },
    {
        id: "standard",
        name: "Standard",
        subtitle: "För växande team",
        price: "499 kr",
        originalPrice: "",
        features: [
            { text: "Upp till 10 användare", included: true },
            { text: "100GB lagring", included: true },
            { text: "Prioriterad support", included: true },
            { text: "Daglig backup", included: true },
            { text: "API-tillgång", included: true },
        ],
        ctaText: "Uppgradera till Standard",
        isFeatured: false,
    }
];

export const pricingComparisonRows: ComparisonRow[] = [
    {
        feature: "Grundläggande funktioner",
        keys: { free: true, plus: true, standard: true, premium: true }
    },
    {
        feature: "Support",
        keys: { free: "Community", plus: "Prioriterad", standard: "Prioriterad", premium: "Dedikerad" }
    },
    {
        feature: "Lagring",
        keys: { free: "1 GB", plus: "50 GB", standard: "100 GB", premium: "Obegränsat" }
    },
    {
        feature: "Säkerhetskopiering",
        keys: { free: false, plus: true, standard: true, premium: true }
    },
    {
        feature: "API-tillgång",
        keys: { free: false, plus: true, standard: true, premium: true }
    },
];
