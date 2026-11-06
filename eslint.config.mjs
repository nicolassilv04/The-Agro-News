import eslintPluginAstro from 'eslint-plugin-astro';
import tsParser from '@typescript-eslint/parser';

export default [
  // Lint .astro files with the Astro-specific parser
  ...eslintPluginAstro.configs.recommended,
  // Override parser for .ts / .tsx files
  {
    files: ['**/*.ts'],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        project: './tsconfig.json',
      },
    },
  },
  {
    // Ignore generated directories
    ignores: ['dist/**', 'node_modules/**', '.astro/**'],
  },
];
