export const SITE_URL = 'https://tan.agro.br';

export function getNewsUrl(slug: string): string {
  return `/noticia/${slug}/`;
}

export function getEditionUrl(slug: string): string {
  return `/noticias/${slug}/`;
}

export function getCategoryUrl(slug: string): string {
  return `/categorias/${slug}/`;
}

export function getCanonicalUrl(path: string): string {
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${SITE_URL}${cleanPath}`;
}
