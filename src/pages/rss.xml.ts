import rss from '@astrojs/rss';
import { getAllNews } from '../lib/content';
import { SITE_URL, getNewsUrl } from '../lib/urls';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const allNews = await getAllNews();

  return rss({
    title: 'TAN — The Agro News',
    description: 'Feed oficial de notícias e inteligência do agronegócio brasileiro.',
    site: context.site?.toString() || SITE_URL,
    items: allNews.map((item) => ({
      title: item.title,
      pubDate: new Date(item.published_at),
      description: item.summary,
      link: getNewsUrl(item.slug),
      categories: [item.category],
    })),
    customData: `<language>pt-BR</language>`,
  });
}
