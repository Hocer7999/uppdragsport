import { defineCollection, z, reference } from 'astro:content';

const articlesCollection = defineCollection({
    schema: z.object({
        title: z.string(),
        metaTitle: z.string().optional(),
        description: z.string(),
        metaDescription: z.string().optional(),
        publishDate: z.string().transform((str) => new Date(str)),
        updatedDate: z.string().transform((str) => new Date(str)).optional(),
        // Reference to a categories entry. Optional — if omitted, the article
        // is "uncategorized" but still routes/renders correctly.
        category: reference('categories').optional(),
        // Multi-tag taxonomy (free-form strings — tag pages are generated from
        // the union of all tags across articles, no separate collection needed).
        tags: z.array(z.string()).default([]),
        // Reference to an authors entry. Optional — falls back to authorName below.
        author: reference('authors').optional(),
        // Legacy / fallback author display name (used when no author reference is set).
        authorName: z.string().default('Redaktionen'),
        image: z.string().optional(),
        imageAlt: z.string().optional(),
        // Synlig fotografkredit (CC-BY/SA-bilder från Wikimedia kräver det) +
        // länk till källfilen. Sätts av news-content/daily-content vid Wikimedia-foto.
        imageCredit: z.string().optional(),
        imageSource: z.string().optional(),
        relatedArticles: z.array(reference('articles')).optional(),
        faq: z.array(z.object({
            question: z.string(),
            answer: z.string(),
        })).optional(),
    }),
});

// Tidskänsliga sportnyheter (skilt från evergreen-artiklar). Genereras av
// news-content-skillet: händelsedrivet, faktagrundat, med original svensk text.
const newsCollection = defineCollection({
    schema: z.object({
        title: z.string(),
        metaTitle: z.string().optional(),
        description: z.string(),
        metaDescription: z.string().optional(),
        publishDate: z.string().transform((str) => new Date(str)),
        updatedDate: z.string().transform((str) => new Date(str)).optional(),
        // "fotboll" | "hockey" | "innebandy" | "friidrott" | "skidor" | ...
        sport: z.string().default('sport'),
        // Namngiven verklig person nyheten i grunden handlar om (för Wikimedia-bild).
        primaryEntity: z.string().optional(),
        // Styr bildkällan: person → Wikimedia-foto; annat → AI-bild.
        entityType: z.enum(['person', 'team', 'league', 'event', 'general']).default('general'),
        authorName: z.string().default('Uppdragsports redaktion'),
        tags: z.array(z.string()).default([]),
        image: z.string().optional(),
        imageAlt: z.string().optional(),
        imageCredit: z.string().optional(),
        imageSource: z.string().optional(),
        // Källhänvisning (E-E-A-T). Renderas som "Källor"-lista.
        sources: z.array(z.object({
            title: z.string(),
            url: z.string(),
        })).default([]),
        // Verkligt färska, tunga händelser får en "DIREKT"-markering.
        isBreaking: z.boolean().default(false),
    }),
});

const categoriesCollection = defineCollection({
    schema: z.object({
        title: z.string(),
        description: z.string().optional(),
        image: z.string().optional(),
        order: z.number().default(0),
    }),
});

const authorsCollection = defineCollection({
    schema: z.object({
        name: z.string(),
        bio: z.string(),
        avatar: z.string().optional(),
        role: z.string().optional(),
        socials: z.record(z.string()).optional(),
    }),
});

const servicesCollection = defineCollection({
    schema: z.object({
        title: z.string(),
        slug: z.string().optional(), // overrides filename; sällan behövs
        order: z.number().default(0), // sort order on hub page
        shortDescription: z.string(), // 1-mening, för kort på startsidan och hub
        description: z.string(), // meta description
        metaTitle: z.string().optional(),
        metaDescription: z.string().optional(),
        icon: z.string().optional(), // iconify-namn, t.ex. "heroicons:sparkles"
        image: z.string().optional(),
        imageAlt: z.string().optional(),
        // Schema.org-typ. Default Service. Lokala företag bör override:a:
        // tandvård → "MedicalProcedure", juridik → "LegalService",
        // hantverk → "Service", finans → "FinancialService", etc.
        schemaType: z.enum([
            'Service',
            'MedicalProcedure',
            'LegalService',
            'FinancialService',
            'HealthAndBeautyBusiness',
        ]).default('Service'),
        priceRange: z.string().optional(), // t.ex. "från 1 200 kr"
        duration: z.string().optional(), // t.ex. "30–45 min"
        faq: z.array(z.object({
            question: z.string(),
            answer: z.string(),
        })).optional(),
        relatedServices: z.array(z.string()).optional(), // slugs
    }),
});

export const collections = {
    'articles': articlesCollection,
    'news': newsCollection,
    'categories': categoriesCollection,
    'authors': authorsCollection,
    'services': servicesCollection,
};
