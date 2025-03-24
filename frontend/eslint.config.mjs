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
      sourceType: 'module',
      globals: {
        ...globals.browser
      }
    },
    plugins: {
      vue: pluginVue
    },
    rules: {
      ...eslint.configs.recommended.rules,
      ...tseslint.configs.recommended[0].rules,
      ...pluginVue.configs['flat/recommended'][0].rules,
      ...eslintConfigPrettier.rules
    }
  }
);
