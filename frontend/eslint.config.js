import eslint from '@eslint/js';
import tseslint from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import sveltePlugin from 'eslint-plugin-svelte';
import svelteParser from 'svelte-eslint-parser';
import prettier from 'eslint-config-prettier';

export default [
  eslint.configs.recommended,
  {
    ignores: ['dist/*', 'node_modules/*', '*.config.js', '*.config.ts', 'scripts/*']
  },
  {
    files: ['**/*.{js,ts}'],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: 2020,
        sourceType: 'module'
      },
      globals: {
        // Add browser globals
        window: 'readonly',
        document: 'readonly',
        console: 'readonly',
        fetch: 'readonly',
        HTMLElement: 'readonly',
        HTMLInputElement: 'readonly',
        HTMLSelectElement: 'readonly',
        HTMLCanvasElement: 'readonly',
        Event: 'readonly'
      }
    },
    plugins: {
      '@typescript-eslint': tseslint
    },
    rules: {
      '@typescript-eslint/no-explicit-any': 'warn',
      'no-inner-declarations': 'off' // Allow function declarations in blocks
    }
  },
  {
    files: ['**/*.svelte'],
    languageOptions: {
      parser: svelteParser,
      parserOptions: {
        parser: tsParser,
        sourceType: 'module'
      },
      globals: {
        // Add browser globals for Svelte files
        window: 'readonly',
        document: 'readonly',
        console: 'readonly',
        fetch: 'readonly',
        HTMLElement: 'readonly',
        HTMLInputElement: 'readonly',
        HTMLSelectElement: 'readonly',
        HTMLCanvasElement: 'readonly',
        Event: 'readonly'
      }
    },
    plugins: {
      svelte: sveltePlugin
    },
    rules: {
      'svelte/valid-compile': 'warn',
      'svelte/no-dom-manipulating': 'off',
      'svelte/experimental-require-strict-events': 'off',
      'svelte/experimental-require-slot-types': 'off',
      'svelte/system': 'warn',
      'no-inner-declarations': 'off' // Allow function declarations in Svelte script blocks
    }
  },
  {
    // Test file specific config
    files: ['**/*.test.ts', '**/setup.ts'],
    languageOptions: {
      globals: {
        // Add test globals
        describe: 'readonly',
        it: 'readonly',
        expect: 'readonly',
        beforeEach: 'readonly',
        afterEach: 'readonly',
        vi: 'readonly',
        global: 'readonly',
        document: 'readonly',
        HTMLElement: 'readonly',
        HTMLInputElement: 'readonly',
        HTMLSelectElement: 'readonly',
        fetch: 'readonly'
      }
    }
  },
  prettier
]; 