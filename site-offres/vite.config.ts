import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'https://api-offres-145837535580.us-central1.run.app',
        changeOrigin: true,
        rewrite: (path)  => path.replace(/^\/api/, ''),
      },
    },
  },
  build: {
    outDir: 'build', // Génère le dossier "build" au lieu de "dist"
    emptyOutDir: true, // Vide le dossier de sortie avant la génération
  },
});
