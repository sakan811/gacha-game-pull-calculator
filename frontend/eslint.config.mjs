// @ts-check
import eslint from "@eslint/js";
import tseslint from "typescript-eslint";
import eslintConfigPrettier from "eslint-config-prettier/flat";
import pluginVue from 'eslint-plugin-vue';
import * as espreeParser from 'espree';
import globals from 'globals';

export default tseslint.config(
  {
    files: ["**/*.{js,ts,vue}"],
    ignores: ["node_modules/", "dist/"],
    languageOptions: {
      parser: espreeParser,
      parserOptions: {
        parser: tseslint.parser,
        extraFileExtensions: ['.vue'],
        ecmaVersion: 'latest',
        sourceType: 'module'
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
    plugins: {
      vue: pluginVue
    },
    rules: {
      ...eslint.configs.recommended.rules,
      ...tseslint.configs.recommended[0].rules,
      ...pluginVue.configs['flat/recommended'][0].rules,
      ...eslintConfigPrettier.rules,
      'vue/valid-template-root': 'off',
      'no-unused-vars': ['error', { 
        'argsIgnorePattern': '^_',
        'varsIgnorePattern': '^_'
      }],
      'no-undef': 'error'
    }
  }
);
