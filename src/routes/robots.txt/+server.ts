
import { config } from '../../../moire.config';

export const prerender = true;

export async function GET({ url }: { url: URL }) {
  const siteUrl = url.origin && url.origin !== 'http://sveltekit-prerender' ? url.origin : (config.url || 'https://example.com');
  const body = `
User-agent: *
Allow: /

Sitemap: ${ siteUrl }/sitemap.xml
`.trim();

  return new Response(body, {
    headers: {
      'Cache-Control': 'max-age=0, s-maxage=3600',
      'Content-Type': 'text/plain'
    }
  });
}
