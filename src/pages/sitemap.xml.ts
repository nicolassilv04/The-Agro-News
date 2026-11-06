import { getAllNews, getAllEditions, getAllCategories } from '../lib/content';
import { SITE_URL, getNewsUrl, getEditionUrl, getCategoryUrl } from '../lib/urls';

export async function GET() {
  const news = await getAllNews();
  const editions = await getAllEditions();
  const categories = await getAllCategories();

  const staticPages = [
    '/',
    '/noticias/',
    '/categorias/',
    '/busca/',
    '/sobre/',
    '/metodologia/',
    '/fontes/',
  ];

  const newsPages = news.map((item) => getNewsUrl(item.slug));
  const editionPages = editions.map((item) => getEditionUrl(item.slug));
  const categoryPages = categories.map((item) => getCategoryUrl(item.slug));

  const allUrls = [...staticPages, ...newsPages, ...editionPages, ...categoryPages];

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${allUrls
  .map(
    (url) => `  <url>
    <loc>${SITE_URL}${url}</loc>
    <changefreq>daily</changefreq>
    <priority>${url === '/' ? '1.0' : url.startsWith('/noticia/') ? '0.8' : '0.6'}</priority>
  </url>`
  )
  .join('\n')}
</urlset>`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml',
    },
  });
}
