// @ts-check
import eslint from "@eslint/js";
import tseslint from "typescript-eslint";
import eslintConfigPrettier from "eslint-config-prettier/flat";
import pluginVue from 'eslint-plugin-vue';
import globals from 'globals';

export default tseslint.config(
  {
    files: ["**/*.{js,ts,vue}"],
    ignores: ["node_modules/", "dist/"],
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
        project: ['./tsconfig.json', './tsconfig.node.json'],
        extraFileExtensions: ['.vue'],
        parser: '@typescript-eslint/parser',
        tsconfigRootDir: '.',
        ecmaFeatures: {
          jsx: true
        }
      },
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.node,
        ...globals.es2021,
        global: true,
        require: true,
        process: true,
        __dirname: true,
        beforeEach: true,
        describe: true,
        it: true,
        expect: true,
        vi: true
      }
    },
    settings: {
      'import/resolver': {
        typescript: true,
        node: true
      }
    },
    processor: pluginVue.processors['.vue'],
    plugins: {
      vue: pluginVue,
      '@typescript-eslint': tseslint.plugin,
    },
    rules: {
      ...eslint.configs.recommended.rules,
      ...tseslint.configs.recommended[0].rules,
      ...pluginVue.configs['flat/recommended'][0].rules,
      ...eslintConfigPrettier.rules,
      'vue/valid-template-root': 'off',
      'vue/comment-directive': 'off',
      'no-unused-vars': 'off', // Disable base rule
      '@typescript-eslint/no-unused-vars': ['error', {
        'argsIgnorePattern': '^_',
        'varsIgnorePattern': '^_'
      }],
      'no-undef': 'off', // TypeScript handles this
      '@typescript-eslint/no-explicit-any': 'warn',
      'vue/html-indent': ['error', 2],
      'vue/script-indent': ['error', 2],
    }
  }
);
