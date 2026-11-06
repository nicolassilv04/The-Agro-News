import { SITE_URL, getCanonicalUrl } from './urls';
import type { NewsItem } from '../types/content';

export interface SeoProps {
  title?: string;
  description?: string;
  canonicalPath?: string;
  image?: string;
  type?: 'website' | 'article';
  publishedTime?: string;
  modifiedTime?: string;
  category?: string;
  keywords?: string[];
}

export function getSeoMetadata(props: SeoProps) {
  const defaultTitle = 'TAN — The Agro News | Inteligência Editorial do Agronegócio';
  const defaultDescription =
    'Portal editorial especializado em notícias, mercado, clima, tecnologia e regulação do agronegócio brasileiro.';
  const defaultImage = `${SITE_URL}/images/og-tan-default.png`;

  const title = props.title ? `${props.title} — TAN` : defaultTitle;
  const description = props.description || defaultDescription;
  const canonicalUrl = getCanonicalUrl(props.canonicalPath || '/');
  const image = props.image
    ? props.image.startsWith('http')
      ? props.image
      : `${SITE_URL}${props.image}`
    : defaultImage;
  const type = props.type || 'website';

  return {
    title,
    description,
    canonicalUrl,
    image,
    type,
    publishedTime: props.publishedTime,
    modifiedTime: props.modifiedTime,
    category: props.category,
    keywords: props.keywords?.join(', '),
  };
}

export function getNewsArticleJsonLd(item: NewsItem, canonicalUrl: string) {
  return JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'NewsArticle',
    headline: item.title,
    description: item.subtitle || item.summary,
    url: canonicalUrl,
    datePublished: item.published_at,
    dateModified: item.updated_at || item.published_at,
    articleSection: item.category,
    keywords: item.tags ? item.tags.join(', ') : item.category,
    author: {
      '@type': 'Organization',
      name: item.source ? item.source.name : 'TAN — The Agro News',
    },
    publisher: {
      '@type': 'Organization',
      name: 'TAN — The Agro News',
      url: SITE_URL,
      logo: {
        '@type': 'ImageObject',
        url: `${SITE_URL}/favicon.svg`,
      },
    },
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': canonicalUrl,
    },
  });
}
