# Vite + React + TypeScript starter

A baseline for new projects: Vite, React, TypeScript, a top navbar, light/dark
theming, and GitHub Actions that deploy to Cloudflare Pages on every push to `main`.

## What's included

- **Vite + React + TypeScript**, unmodified from `create-vite` apart from the placeholder content being removed
- **Navbar** (`src/components/Navbar.tsx`), sticky, with a skip-to-content link. Add links in `src/config.ts`
- **Light/dark theme.** Follows the OS until the person picks one, then remembers the choice.
  An inline script in `index.html` applies the theme before first paint, so there is no flash
- **Design tokens** in `src/index.css`. Colors come from CSS variables; dark values live under `:root[data-theme='dark']`
- **CI/CD** (`.github/workflows/deploy.yml`): lint + build on every push and PR, deploy to Cloudflare Pages on pushes to `main`

```
src/
  components/   Navbar, ThemeToggle
  theme/        ThemeProvider, useTheme, storage helpers
  config.ts     App name and nav links
  index.css     Tokens + base styles
```

## Starting a new project

Make this repo a **template repository** once (GitHub → Settings → tick *Template repository*).
After that:

```sh
gh repo create my-app --template <you>/vite-react-template --clone --private
cd my-app
npm install
npm run dev
```

Then rename the placeholders:

1. `package.json` → `name`
2. `index.html` → `<title>`
3. `src/config.ts` → `APP_NAME`
4. `public/favicon.svg`

## Deploying to Cloudflare Pages

The first push to `main` triggers a deploy, and it will fail until the steps below are done.
Do them before your first push, or just re-run the workflow afterwards.

**1. Create the Pages project (once per project).** `wrangler pages deploy` does not create
the project for you.

```sh
npx wrangler pages project create my-app --production-branch=main
```

By default the workflow deploys to a Pages project named after the **GitHub repository**.
Names must be lowercase letters, digits and hyphens. If yours differs, set a variable:

```sh
gh variable set CLOUDFLARE_PROJECT_NAME --body my-pages-project-name
```

**2. Create an API token.** Cloudflare dashboard → *My Profile → API Tokens → Create Token →
Custom token* with permission **Account → Cloudflare Pages → Edit**. Your account ID is on the
dashboard overview page.

**3. Add them as repository secrets.**

```sh
gh secret set CLOUDFLARE_API_TOKEN
gh secret set CLOUDFLARE_ACCOUNT_ID
```

**4. Push to `main`.** The site is live at `https://<project-name>.pages.dev`.

Pull requests run lint and build only. They never deploy and don't need the secrets.

## Theming

Change colors in `src/index.css`. There is one set of tokens for light (`:root`) and one for dark
(`:root[data-theme='dark']`). To add a token, add it to both blocks, then use `var(--your-token)`.

Use the theme from code with `useTheme()`:

```tsx
const { theme, setTheme, toggleTheme } = useTheme()
```

If you change the localStorage key, update it in both `src/theme/storage.ts` and the inline
script in `index.html`.

## Scripts

| Command           | What it does                          |
| ----------------- | ------------------------------------- |
| `npm run dev`     | Start the dev server                  |
| `npm run build`   | Typecheck, then build to `dist/`      |
| `npm run preview` | Serve the production build locally    |
| `npm run lint`    | Lint with oxlint                      |

Requires Node `^20.19` or `>=22.12` (`.nvmrc` pins 22).

## Notes

- **Routing:** none included. If you add a client-side router, Cloudflare Pages serves
  `index.html` for unknown paths automatically as long as there is no `404.html`.
- **Pages vs. Workers:** Cloudflare now steers new projects toward Workers with static assets.
  Pages remains supported and is what this template uses.
