import fs from 'fs';

// Verify SEO elements in a noticia page
const noticiaHtml = fs.readFileSync(
  'dist/noticia/soja-registra-nova-movimentacao-no-mercado-internacional/index.html',
  'utf-8'
);

const checks = [
  ['<title>', noticiaHtml.includes('<title>')],
  ['meta description', noticiaHtml.includes('name="description"')],
  ['canonical', noticiaHtml.includes('rel="canonical"')],
  ['og:title', noticiaHtml.includes('og:title')],
  ['og:type', noticiaHtml.includes('og:type')],
  ['og:image', noticiaHtml.includes('og:image')],
  ['twitter:card', noticiaHtml.includes('twitter:card')],
  ['JSON-LD NewsArticle', noticiaHtml.includes('NewsArticle')],
  ['datePublished', noticiaHtml.includes('datePublished')],
  ['article:published_time', noticiaHtml.includes('article:published_time')],
  ['article body text in HTML', noticiaHtml.includes('Os mercados internacionais')],
  ['breadcrumb', noticiaHtml.includes('breadcrumb')],
  ['data-pagefind-body', noticiaHtml.includes('data-pagefind-body')],
  ['skip link #main-content', noticiaHtml.includes('#main-content')],
  ['aria-expanded (menu)', noticiaHtml.includes('aria-expanded')],
  ['aria-controls (menu)', noticiaHtml.includes('aria-controls')],
  ['article element', noticiaHtml.includes('<article')],
];

console.log('=== SEO & Content Verification: /noticia/soja-... ===');
checks.forEach(([label, result]) => {
  console.log(result ? '[OK]  ' : '[FAIL]', label);
});

// Verify sitemap entries
const sitemap = fs.readFileSync('dist/sitemap.xml', 'utf-8');
const sitemapChecks = [
  ['sitemap has homepage', sitemap.includes('https://tan.agro.br/')],
  ['sitemap has noticia url', sitemap.includes('/noticia/')],
  ['sitemap has noticias url', sitemap.includes('/noticias/')],
  ['sitemap has categorias url', sitemap.includes('/categorias/')],
  ['sitemap has priority 1.0 for home', sitemap.includes('<priority>1.0</priority>')],
];
console.log();
console.log('=== Sitemap Verification ===');
sitemapChecks.forEach(([label, result]) => {
  console.log(result ? '[OK]  ' : '[FAIL]', label);
});

// Verify RSS
const rss = fs.readFileSync('dist/rss.xml', 'utf-8');
const rssChecks = [
  ['RSS has channel title TAN', rss.includes('TAN')],
  ['RSS has item element', rss.includes('<item>')],
  ['RSS has pubDate', rss.includes('<pubDate>')],
  ['RSS lang pt-BR', rss.includes('pt-BR')],
];
console.log();
console.log('=== RSS Verification ===');
rssChecks.forEach(([label, result]) => {
  console.log(result ? '[OK]  ' : '[FAIL]', label);
});

// Summary
const allChecks = [...checks, ...sitemapChecks, ...rssChecks];
const passed = allChecks.filter(([, r]) => r).length;
console.log();
console.log(`TOTAL PASS: ${passed} / ${allChecks.length}`);
