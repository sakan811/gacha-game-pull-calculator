// @ts-check
import eslint from "@eslint/js";
import tseslint from "typescript-eslint";
import eslintConfigPrettier from "eslint-config-prettier/flat";
import pluginVue from 'eslint-plugin-vue';
import globals from 'globals';
import * as vueParser from 'vue-eslint-parser';

export default tseslint.config(
  {
    files: ["**/*.{js,ts,vue}"],
    ignores: ["**/dist/**", "**/node_modules/**"],
    languageOptions: {
      sourceType: 'module',
      parser: vueParser,
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
        project: ['./tsconfig.app.json', './tsconfig.node.json'],
        extraFileExtensions: ['.vue'],
        parser: tseslint.parser,
        tsconfigRootDir: '.',
        ecmaFeatures: {
          jsx: true
        }
      },
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
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': ['error', {
        'argsIgnorePattern': '^_',
        'varsIgnorePattern': '^_'
      }],
      'no-undef': 'off',
      '@typescript-eslint/no-explicit-any': 'warn',
      'vue/html-indent': ['error', 2],
      'vue/script-indent': ['error', 2]
    }
  }
);
