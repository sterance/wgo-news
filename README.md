# "What's Going On?" News

A small news site. Anyone can browse the latest articles, filter them by category and read
them in full. A superuser can sign in and create, edit and delete articles and categories,
either from the site's own **Admin** page or from Django's built-in admin.

- **Front end:** React 19 + TypeScript, built with Vite, MUI components, React Router
- **Back end:** Django 6 + Django REST Framework, SQLite

## Architecture

```
src/                  React app (pages: Home, News, Article, Admin)
  api/                fetch helpers (client.ts), useApi, useAuth
  config.ts           backend URL, nav links, login URL helper
public/theme-init.js  sets the light/dark theme before first paint
backend/
  config/             settings, URLs, database router
  news/
    models.py         Category, News
    forms.py          CategoryForm, NewsForm: the validation rules
    serializers.py    API serializers (validate by running the forms)
    admin.py          Django admin (uses the forms directly)
    permissions.py    IsSuperuserOrReadOnly
    views.py          JSON API
    views_auth.py     /api/auth/me/ and /api/auth/logout/
    views_spa.py      serves the built React app through templates
    templatetags/vite.py  {% vite_assets %}: asset tags from Vite's manifest
  templates/          base.html → spa.html, message.html → 403.html / build_missing.html
```

**One set of validation rules.** `NewsForm` and `CategoryForm` are Django `ModelForm`s. The
Django admin uses them as its forms. The API serializers run the same form from `validate()`
and return its errors under the same field names. Both paths therefore enforce the same rules:
- A title of at least 3 characters.
- No future dates ("The date and time cannot be in the future.").
- No duplicate category names, ignoring case ("A category with this name already exists.").
- Surrounding whitespace is stripped.

The model `clean()` methods and database constraints stay in place as a last line of defence
for code that skips the forms (the shell, `seed_news`).

**Two SQLite databases.** `config/db_router.py` sends the `news` app to `news.db` and
everything else (users, sessions, admin log) to `auth.db`. Each one is migrated separately.

**Templates.** In Mode B (below), every page is rendered by Django. `spa.html` extends
`base.html` (head, favicons, theme script) and adds the React root plus the hashed JS/CSS
from Vite's manifest. The plain message pages (`403.html`, `build_missing.html`) extend
`message.html`, which itself extends `base.html`.

## Setup

Requires Python 3.12+ and Node `^20.19` or `>=22.12` (`.nvmrc` pins 22).

```sh
# Back end
cd backend
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate                    # auth.db: users, sessions, admin
python manage.py migrate --database news    # news.db: categories, articles
python manage.py createsuperuser
python manage.py seed_news                  # optional demo content
cd ..

# Front end
npm install
```

## Running

There are two ways to run it in development. Both use one origin for the app, the API and the
login page, so the Django session cookie and CSRF protection work the same in each.

### Mode A: Vite dev server (hot reload)

```sh
# terminal 1
cd backend && python manage.py runserver      # http://localhost:8000

# terminal 2
npm run dev                                   # http://localhost:5173
```

Open **http://localhost:5173**. Vite serves the React app and proxies `/api`, `/django-admin`
and `/static` to Django on `:8000` (see `vite.config.ts`). Leave `VITE_BACKEND_URL` unset.

### Mode B: Django serves the built app

```sh
npm run build:django                          # builds into backend/frontend_build/
cd backend && python manage.py runserver
```

Open **http://localhost:8000**. Django renders each page from its templates and serves the
build as static files. Run `npm run build:django` again after front-end changes. Restart
`runserver` after the *first* build so Django picks up the new directory. If the build is
missing, every page shows instructions (HTTP 503) instead.

## Signing in (admin)

1. Open `/admin`.
2. If you aren't signed in, you are sent to Django's admin login page,
   `/django-admin/login/?next=/admin`.
   - In Mode A, the React page does this after asking `/api/auth/me/`.
   - In Mode B, Django redirects before the page loads.
3. Sign in with a **superuser** account. Django sends you back to `/admin`.
4. Use **Log out** on the Admin page to end the session and return home.

Only superusers can manage content. A signed-in user who isn't a superuser sees a "not a
superuser" message (Mode A) or a 403 page (Mode B), and every write they attempt is refused.

**CSRF.** The API uses Django session authentication. `GET /api/auth/me/` (called on load)
and the Django-rendered pages set the `csrftoken` cookie. Every API write and the logout
request send it back in an `X-CSRFToken` header. If a write gets 401 or 403 (the session has
expired, or the account isn't a superuser), the app sends you to the login page.

## URLs

| Path | Method | What it does | Who |
| --- | --- | --- | --- |
| `/` | GET | Home: latest articles | Anyone |
| `/news`, `/news?category=<id>` | GET | All articles, optional category filter | Anyone |
| `/news/<id>` | GET | One article | Anyone |
| `/admin` | GET | React admin page: manage articles and categories | Superuser (others → login or 403) |
| `/api/news/` | GET | Articles, newest first. `?category=<id>`, `?limit=<n>` (max 100) | Anyone |
| `/api/news/` | POST | Create an article | Superuser |
| `/api/news/<id>/` | GET | One article | Anyone |
| `/api/news/<id>/` | PATCH, PUT, DELETE | Update or delete an article | Superuser |
| `/api/categories/` | GET | Categories A–Z with article counts | Anyone |
| `/api/categories/` | POST | Create a category | Superuser |
| `/api/categories/<id>/` | GET | One category | Anyone |
| `/api/categories/<id>/` | PATCH, PUT, DELETE | Rename or delete a category (deleting removes its articles) | Superuser |
| `/api/auth/me/` | GET | `{authenticated, username, is_superuser}`; sets the `csrftoken` cookie | Anyone |
| `/api/auth/logout/` | POST | End the session (needs `X-CSRFToken`), returns 204 | Anyone with a session |
| `/django-admin/` | GET, POST | Django's built-in admin | Staff (login page for everyone) |
| `/django-admin/login/` | GET, POST | Login page used by `/admin` | Anyone |

The React routes (`/`, `/news`, `/news/<id>`, `/admin`) are served by Vite in Mode A and by
Django in Mode B. In Mode B, any other path outside `/api/`, `/django-admin/` and `/static/`
also loads the React app, which handles unknown routes itself.

Validation errors come back as HTTP 400 with a JSON object keyed by field, e.g.
`{"title": ["Ensure this field has at least 3 characters."]}`. Writes without permission get
403.

## Tests

```sh
cd backend && python manage.py test     # Django: models, forms, API, permissions, auth, admin, templates
npm run lint                            # oxlint
npm run build                           # typecheck + production build
```

## Scripts

| Command | What it does |
| --- | --- |
| `npm run dev` | Vite dev server on `:5173`, proxying the backend paths to `:8000` |
| `npm run build` | Typecheck, then the production build into `dist/` (base `/`) |
| `npm run build:django` | Typecheck, then a build for Django into `backend/frontend_build/` (base `/static/`) |
| `npm run preview` | Serve `dist/` locally (same proxy as `dev`) |
| `npm run lint` | Lint with oxlint |

## Theming

Colours are CSS variables in `src/index.css`: light values under `:root`, dark under
`:root[data-theme='dark']`. `public/theme-init.js` applies the saved or system theme before
first paint. It is loaded by both `index.html` and `backend/templates/base.html`. If you change
the localStorage key, update it there and in `src/theme/storage.ts`.

## Production note

The production setup is unchanged:
- The front end is built with `npm run build` and deployed to Cloudflare Pages.
- The Django back end runs in Docker on an Oracle host (`backend/Dockerfile`,
  `.github/workflows/deploy-backend.yml`).
- The production build sets `VITE_BACKEND_URL` to the back end's public URL.

Because the Pages site and the API are on different sites, the browser won't send the Django
session cookie with API requests from the Cloudflare-hosted front end. Admin writes from there
won't authenticate. Reading works as before. **Mode B, where Django serves the app, is the
supported way to use the admin.** The Django admin at `<backend>/django-admin/` also works.

## Deployment (optional)

`.github/workflows/deploy.yml` lints and builds on every push and PR. When the repository
variable `ENABLE_DEPLOY` is `true`, it also deploys `dist/` to Cloudflare Pages on pushes to
`main`. One-time setup:

1. Create the Pages project:
   `npx wrangler pages project create <name> --production-branch=main`.
   The workflow deploys to a project named after the repository; override it with the
   `CLOUDFLARE_PROJECT_NAME` variable.
2. Create a Cloudflare API token with **Account → Cloudflare Pages → Edit**. Add it and your
   account ID as repository secrets:
   ```sh
   gh secret set CLOUDFLARE_API_TOKEN
   gh secret set CLOUDFLARE_ACCOUNT_ID
   ```
3. Set the repository variables `VITE_BACKEND_URL` (the back end's public URL) and
   `ENABLE_DEPLOY=true`.
4. Add the Pages origin to the back end's `DJANGO_CORS_ORIGINS`.
