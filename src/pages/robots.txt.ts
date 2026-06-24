import type { APIRoute } from 'astro';
import { companyConfig } from '../config/company';

export const GET: APIRoute = ({ site }) => {
    const base = site?.href.replace(/\/$/, '') ?? `https://${companyConfig.domain}`;
    const body = `User-agent: *\nDisallow:\n\nSitemap: ${base}/sitemap-index.xml\n`;
    return new Response(body, {
        headers: { 'Content-Type': 'text/plain; charset=utf-8' },
    });
};
