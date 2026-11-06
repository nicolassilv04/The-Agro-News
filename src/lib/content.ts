import { getCollection } from 'astro:content';
import type { NewsItem, Edition, Category } from '../types/content';

export async function getAllNews(): Promise<NewsItem[]> {
  const newsEntries = await getCollection('news');
  return newsEntries
    .map((entry) => entry.data as NewsItem)
    .sort((a, b) => new Date(b.published_at).getTime() - new Date(a.published_at).getTime());
}

export async function getNewsBySlug(slug: string): Promise<NewsItem | undefined> {
  const allNews = await getAllNews();
  return allNews.find((item) => item.slug === slug);
}

export async function getNewsById(id: string): Promise<NewsItem | undefined> {
  const allNews = await getAllNews();
  return allNews.find((item) => item.id === id);
}

export async function getNewsByCategory(categorySlug: string): Promise<NewsItem[]> {
  const allNews = await getAllNews();
  return allNews.filter((item) => item.category.toLowerCase() === categorySlug.toLowerCase());
}

export async function getAllEditions(): Promise<Edition[]> {
  const editionEntries = await getCollection('editions');
  return editionEntries
    .map((entry) => entry.data as Edition)
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
}

export async function getEditionBySlug(slug: string): Promise<Edition | undefined> {
  const allEditions = await getAllEditions();
  return allEditions.find((item) => item.slug === slug);
}

export async function getLatestEdition(): Promise<Edition | undefined> {
  const editions = await getAllEditions();
  return editions[0];
}

export async function getAllCategories(): Promise<Category[]> {
  const categoryEntries = await getCollection('categories');
  return categoryEntries.map((entry) => entry.data as Category);
}

export async function getCategoryBySlug(slug: string): Promise<Category | undefined> {
  const categories = await getAllCategories();
  return categories.find((cat) => cat.slug.toLowerCase() === slug.toLowerCase());
}

export async function getRelatedNews(newsId: string, limit: number = 3): Promise<NewsItem[]> {
  const allNews = await getAllNews();
  const current = allNews.find((item) => item.id === newsId);
  if (!current) return [];

  if (current.related_news && current.related_news.length > 0) {
    const explicitRelated = allNews.filter((item) => current.related_news?.includes(item.id));
    if (explicitRelated.length > 0) return explicitRelated.slice(0, limit);
  }

  return allNews
    .filter((item) => item.id !== newsId && item.category === current.category)
    .slice(0, limit);
}
