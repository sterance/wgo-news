import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// Backend paths forwarded to Django in dev, so the app, API and Django login
// share one origin (session cookie + CSRF). changeOrigin stays false: Django's
// CSRF check needs the forwarded Host to match the browser's Origin.
const proxy = Object.fromEntries(
  ['/api', '/django-admin', '/static'].map((path) => [path, { target: 'http://localhost:8000' }]),
)

// https://vite.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [react()],
  server: { proxy },
  preview: { proxy },
  // `npm run build:django`: a build for Django to serve as static files
  // (see backend/templates/spa.html). The default build is unchanged.
  ...(mode === 'django' && {
    base: '/static/',
    build: {
      outDir: 'backend/frontend_build',
      emptyOutDir: true,
      manifest: true,
    },
  }),
}))
