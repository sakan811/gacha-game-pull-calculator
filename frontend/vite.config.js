import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  ssr: {
    noExternal: ['chart.js', 'chartjs-plugin-annotation']
  },
  optimizeDeps: {
    include: ['chart.js', 'chartjs-plugin-annotation']
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path
      }
    }
  }
}) 