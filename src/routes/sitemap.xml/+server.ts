
import { config } from '../../../moire.config';
import { getMemos } from '$lib/server/memos';

export const prerender = true;

export async function GET({ url }: { url: URL }) {
  const memos = await getMemos();
  // Falling back to config.url because url.origin is not available during prerendering
  const siteUrl = url.origin && url.origin !== 'http://sveltekit-prerender' ? url.origin : (config.url || 'https://example.com');

  const body = `<?xml version="1.0" encoding="UTF-8" ?>
<urlset
  xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"
  xmlns:xhtml="http://www.w3.org/1999/xhtml"
  xmlns:mobile="http://www.google.com/schemas/sitemap-mobile/1.0"
  xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
  xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"
>
  <url>
    <loc>${ siteUrl }</loc>
    <changefreq>daily</changefreq>
    <priority>0.7</priority>
  </url>
  ${ memos
    .map(
      (memo) => `
  <url>
    <loc>${ siteUrl }/#${ memo.slug }</loc>
    <changefreq>daily</changefreq>
    <priority>0.7</priority>
    <lastmod>${ memo.date.toISOString() }</lastmod>
  </url>
  `
    )
    .join('') }
</urlset>`;

  return new Response(body, {
    headers: {
      'Cache-Control': 'max-age=0, s-maxage=3600',
      'Content-Type': 'application/xml'
    }
  });
}
