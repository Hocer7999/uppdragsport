// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from "@tailwindcss/vite";
import icon from 'astro-icon';
import sitemap from '@astrojs/sitemap';

import { companyConfig } from './src/config/company.ts';

// Single source of truth for the domain: companyConfig.domain
// Update src/config/company.ts when starting a new site.
export default defineConfig({
  site: `https://${companyConfig.domain}`,
  trailingSlash: 'never',
  // build.format defaults to 'directory' — pairs with trailingSlash: 'never' on
  // static hosts (Vercel/Netlify/Cloudflare Pages) so /om-oss/index.html is
  // served as /om-oss with no .html extension and no trailing slash.
  vite: {
    plugins: [tailwindcss()],
  },
  // Tunna taggsidor (en artikel styck) ska varken indexeras eller ligga i
  // sitemapen. De finns kvar för intern navigation men markeras noindex i
  // tag/[slug].astro och filtreras bort här.
  integrations: [icon(), sitemap({ filter: (page) => !/\/tag\//.test(page) })],
});
