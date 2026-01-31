import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [
    react(),
  ],
  // Explicitly tell Vite to look for postcss config if needed, 
  // though it auto-detects postcss.config.js by default.
  css: {
    postcss: './postcss.config.js',
  },
});