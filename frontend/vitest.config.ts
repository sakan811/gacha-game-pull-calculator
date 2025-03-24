import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/tests/utils/setup.ts'],
    include: [
      'src/tests/**/*.{test,spec}.{js,ts,jsx,tsx}', 
      'src/tests/**/**/*.{test,spec}.{js,ts,jsx,tsx}'
    ]
  }
});