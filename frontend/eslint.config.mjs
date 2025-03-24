// @ts-check
import eslint from "@eslint/js";
import tseslint from "typescript-eslint";
import eslintConfigPrettier from "eslint-config-prettier/flat";
import vueParser from "vue-eslint-parser";

export default tseslint.config(
  eslint.configs.recommended,
  tseslint.configs.recommended,
  eslintConfigPrettier,
  {
    files: ["**/*.{js,ts,vue}"],
    ignores: ["node_modules/", "dist/"],
    languageOptions: {
      parser: vueParser,
      parserOptions: {
        parser: "@typescript-eslint/parser",
        extraFileExtensions: [".vue"],
        ecmaVersion: 2020,
        sourceType: "module",
      },
    },
  },
);
