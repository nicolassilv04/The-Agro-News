import { defineCollection, z } from 'astro:content';

const sourceSchema = z.object({
  name: z.string(),
  url: z.string().optional(),
  accessedAt: z.string().optional(),
});

const nlpSchema = z.object({
  importance_score: z.number().optional(),
  sentiment: z.enum(['positive', 'negative', 'neutral']).optional(),
  cluster_id: z.string().optional(),
  topics: z.array(z.string()).optional(),
  key_points: z.array(z.string()).optional(),
  tan_summary: z.string().optional(),
});

const entitiesSchema = z.object({
  pessoas: z.array(z.string()).optional(),
  empresas: z.array(z.string()).optional(),
  organizacoes: z.array(z.string()).optional(),
  locais: z.array(z.string()).optional(),
  produtos: z.array(z.string()).optional(),
  commodities: z.array(z.string()).optional(),
});

const newsCollection = defineCollection({
  type: 'data',
  schema: z.object({
    id: z.string(),
    slug: z.string(),
    title: z.string(),
    subtitle: z.string().optional(),
    summary: z.string(),
    content: z.string(),
    category: z.string(),
    subcategory: z.string().optional(),
    published_at: z.string(),
    updated_at: z.string().optional(),
    edition_id: z.string(),
    is_featured: z.boolean().default(false),
    heroImage: z.string().optional(),
    heroAlt: z.string().optional(),
    source: sourceSchema.optional(),
    sources_count: z.number().optional(),
    sources_list: z.array(sourceSchema).optional(),
    tags: z.array(z.string()).default([]),
    entities: entitiesSchema.optional(),
    regions: z.array(z.string()).optional(),
    nlp: nlpSchema.optional(),
    related_news: z.array(z.string()).optional(),
  }),
});

const editionsCollection = defineCollection({
  type: 'data',
  schema: z.object({
    id: z.string(),
    slug: z.string(),
    date: z.string(),
    formatted_date: z.string(),
    title: z.string(),
    summary: z.string(),
    featured_news: z.string(),
    news: z.array(z.string()),
  }),
});

const categoriesCollection = defineCollection({
  type: 'data',
  schema: z.object({
    id: z.string(),
    slug: z.string(),
    name: z.string(),
    description: z.string(),
    subcategories: z.array(z.string()),
    icon: z.string().optional(),
  }),
});

export const collections = {
  news: newsCollection,
  editions: editionsCollection,
  categories: categoriesCollection,
};
