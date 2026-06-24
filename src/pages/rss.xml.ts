import rss from "@astrojs/rss";
import { getCollection } from "astro:content";
import type { APIContext } from "astro";
import { companyConfig } from "../config/company";

/**
 * RSS-feed for /artiklar.
 *
 * - Always emits a valid feed, even when the articles-collection is empty.
 * - Items are ordered newest-first by `publishDate`.
 * - All links are absolute (resolved against `context.site`).
 * - Language is set to sv-SE via customData.
 */
export async function GET(context: APIContext) {
    const articles = await getCollection("articles");

    return rss({
        title: companyConfig.name,
        description: companyConfig.description,
        site: context.site ?? `https://${companyConfig.domain}`,
        items: articles
            .sort(
                (a, b) =>
                    b.data.publishDate.valueOf() - a.data.publishDate.valueOf(),
            )
            .map((article) => {
                // Build link without trailing slash to match canonicals
                // (astro.config has trailingSlash: 'never').
                const siteBase =
                    context.site?.toString().replace(/\/$/, "") ??
                    `https://${companyConfig.domain}`;
                return {
                    title: article.data.title,
                    pubDate: article.data.publishDate,
                    description: article.data.description,
                    link: `${siteBase}/artiklar/${article.slug}`,
                };
            }),
        customData: `<language>sv-SE</language>`,
    });
}
