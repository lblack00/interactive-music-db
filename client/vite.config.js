import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '~@mdi/font': fileURLToPath(new URL('./node_modules/@mdi/font', import.meta.url))
    }
  },
  server: {
    fs: {
      // Allow serving files from node_modules
      allow: ['..', './node_modules']
    }
  }
})
