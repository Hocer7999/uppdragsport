import type {
    Graph,
    Organization,
    WebSite,
    WebPage,
    Article,
    BlogPosting,
    Blog,
    CollectionPage,
    FAQPage,
    Person,
    DefinedTerm,
    Thing,
} from 'schema-dts';
import { companyConfig } from '../config/company';

export const siteUrl = `https://${companyConfig.domain}`;

/** Normalize a pathname to match trailingSlash: 'never'. Root "/" is preserved. */
export function normalizePath(pathname: string): string {
    return pathname.replace(/\/+$/, '') || '/';
}

/** Build a canonical URL string from a pathname (always trailing-slash-stripped). */
export function canonical(pathname: string): string {
    return new URL(normalizePath(pathname), siteUrl).href;
}

export function getOrganization(): Organization {
    return {
        '@type': 'Organization',
        '@id': `${siteUrl}/#organization`,
        name: companyConfig.name,
        url: siteUrl,
        logo: `${siteUrl}${companyConfig.logo}`,
        sameAs: Object.values(companyConfig.socialMedia || {}).filter((u): u is string => !!u),
    };
}

export function getWebSite(): WebSite {
    return {
        '@type': 'WebSite',
        '@id': `${siteUrl}/#website`,
        url: siteUrl,
        name: companyConfig.name,
        publisher: {
            '@id': `${siteUrl}/#organization`,
        },
    };
}

export function getWebPage(pathname: string, title: string, description?: string): WebPage {
    const url = canonical(pathname);
    return {
        '@type': 'WebPage',
        '@id': `${url}#webpage`,
        url,
        name: title,
        description: description,
        isPartOf: {
            '@id': `${siteUrl}/#website`,
        },
        inLanguage: 'sv-SE',
    };
}

/** Generic Article (schemaType: Article). Use getBlogPosting for blog posts. */
export function getArticle(
    pathname: string,
    title: string,
    publishDate: Date,
    authorName: string,
    image?: string,
    description?: string,
    updatedDate?: Date,
): Article {
    const url = canonical(pathname);
    return {
        '@type': 'Article',
        '@id': `${url}#article`,
        isPartOf: { '@id': `${url}#webpage` },
        headline: title,
        datePublished: publishDate.toISOString(),
        ...(updatedDate && { dateModified: updatedDate.toISOString() }),
        author: { '@type': 'Person', name: authorName },
        publisher: { '@id': `${siteUrl}/#organization` },
        image: image ? new URL(image, siteUrl).href : undefined,
        description,
    };
}

/** BlogPosting — use for editorial / blog posts on content sites. */
export function getBlogPosting(
    pathname: string,
    title: string,
    publishDate: Date,
    authorName: string,
    image?: string,
    description?: string,
    updatedDate?: Date,
): BlogPosting {
    const url = canonical(pathname);
    return {
        '@type': 'BlogPosting',
        '@id': `${url}#blogposting`,
        isPartOf: { '@id': `${url}#webpage` },
        mainEntityOfPage: { '@id': `${url}#webpage` },
        headline: title,
        datePublished: publishDate.toISOString(),
        ...(updatedDate && { dateModified: updatedDate.toISOString() }),
        author: { '@type': 'Person', name: authorName },
        publisher: { '@id': `${siteUrl}/#organization` },
        image: image ? new URL(image, siteUrl).href : undefined,
        description,
    };
}

/** Blog — primary entity for content sites. */
export function getBlog(name?: string, description?: string): Blog {
    return {
        '@type': 'Blog',
        '@id': `${siteUrl}/#blog`,
        url: siteUrl,
        name: name ?? companyConfig.name,
        description: description ?? companyConfig.description,
        publisher: { '@id': `${siteUrl}/#organization` },
        inLanguage: 'sv-SE',
    };
}

/** CollectionPage — for category/tag/author archive pages. */
export function getCollectionPage(
    pathname: string,
    name: string,
    description?: string,
    itemCount?: number,
): CollectionPage {
    const url = canonical(pathname);
    return {
        '@type': 'CollectionPage',
        '@id': `${url}#collectionpage`,
        url,
        name,
        description,
        isPartOf: { '@id': `${siteUrl}/#website` },
        inLanguage: 'sv-SE',
        ...(typeof itemCount === 'number' && {
            mainEntity: {
                '@type': 'ItemList',
                numberOfItems: itemCount,
            },
        }),
    };
}

/** Person — for author profile pages. */
export function getPerson(author: {
    name: string;
    bio?: string;
    avatar?: string;
    role?: string;
    socials?: Record<string, string>;
    pathname?: string;
}): Person {
    const url = author.pathname ? canonical(author.pathname) : undefined;
    return {
        '@type': 'Person',
        ...(url && { '@id': `${url}#person` }),
        name: author.name,
        ...(author.bio && { description: author.bio }),
        ...(author.avatar && { image: new URL(author.avatar, siteUrl).href }),
        ...(author.role && { jobTitle: author.role }),
        ...(url && { url }),
        ...(author.socials && {
            sameAs: Object.values(author.socials).filter((u): u is string => !!u),
        }),
        worksFor: { '@id': `${siteUrl}/#organization` },
    };
}

/** DefinedTerm — for glossary / encyclopedia / directory entries. */
export function getDefinedTerm(term: {
    name: string;
    description: string;
    pathname: string;
    inDefinedTermSet?: string;
    termCode?: string;
}): DefinedTerm {
    const url = canonical(term.pathname);
    return {
        '@type': 'DefinedTerm',
        '@id': `${url}#term`,
        name: term.name,
        description: term.description,
        url,
        ...(term.inDefinedTermSet && {
            inDefinedTermSet: term.inDefinedTermSet,
        }),
        ...(term.termCode && { termCode: term.termCode }),
    };
}

export function getFAQPage(faqs: { question: string; answer: string }[], pathname: string): FAQPage {
    const url = canonical(pathname);
    return {
        '@type': 'FAQPage',
        '@id': `${url}#faq`,
        isPartOf: { '@id': `${url}#webpage` },
        mainEntity: faqs.map((faq) => ({
            '@type': 'Question',
            name: faq.question,
            acceptedAnswer: { '@type': 'Answer', text: faq.answer },
        })),
    };
}

export function getService(
    pathname: string,
    data: {
        title: string;
        description: string;
        schemaType: 'Service' | 'MedicalProcedure' | 'LegalService' | 'FinancialService' | 'HealthAndBeautyBusiness';
        image?: string;
        priceRange?: string;
    },
): Thing {
    const url = canonical(pathname);
    return {
        '@type': data.schemaType,
        '@id': `${url}#service`,
        name: data.title,
        description: data.description,
        url,
        provider: { '@id': `${siteUrl}/#organization` },
        ...(data.image && { image: new URL(data.image, siteUrl).href }),
        ...(data.priceRange && {
            offers: {
                '@type': 'Offer',
                priceCurrency: 'SEK',
                description: data.priceRange,
            },
        }),
    } as Thing;
}

export function getBreadcrumbs(items: { name: string; pathname: string }[]): Thing {
    return {
        '@type': 'BreadcrumbList',
        itemListElement: items.map((item, index) => ({
            '@type': 'ListItem',
            position: index + 1,
            name: item.name,
            item: canonical(item.pathname),
        })),
    } as Thing;
}

export function generateGraph(schemaObjects: Thing[]): Graph {
    return {
        '@context': 'https://schema.org',
        '@graph': schemaObjects,
    };
}
