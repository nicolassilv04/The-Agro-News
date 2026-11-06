export interface Source {
  name: string;
  url?: string;
  accessedAt?: string;
}

export interface NlpData {
  importance_score?: number;
  sentiment?: 'positive' | 'negative' | 'neutral';
  cluster_id?: string;
  topics?: string[];
  key_points?: string[];
  tan_summary?: string;
}

export interface Entities {
  pessoas?: string[];
  empresas?: string[];
  organizacoes?: string[];
  locais?: string[];
  produtos?: string[];
  commodities?: string[];
}

export interface NewsItem {
  id: string;
  slug: string;
  title: string;
  subtitle?: string;
  summary: string;
  content: string;
  category: string;
  subcategory?: string;
  published_at: string;
  updated_at?: string;
  edition_id: string;
  is_featured?: boolean;
  heroImage?: string;
  heroAlt?: string;
  source?: Source;
  sources_count?: number;
  sources_list?: Source[];
  tags: string[];
  entities?: Entities;
  regions?: string[];
  nlp?: NlpData;
  related_news?: string[];
}

export interface Edition {
  id: string;
  slug: string;
  date: string;
  formatted_date: string;
  title: string;
  summary: string;
  featured_news: string;
  news: string[];
}

export interface Category {
  id: string;
  slug: string;
  name: string;
  description: string;
  subcategories: string[];
  icon?: string;
}
