# WGO News: admin login, shared forms, and React served by Django

Instructions for Claude Code working in the `wgo-news` repo (Django REST backend in `backend/`, React + Vite front end in `src/`).

## Goal

1. **Two ways to run in development.** Both must work, because the in-class demo happens in dev.
   - **Mode A, Vite dev server.** `npm run dev` on `:5173`, which proxies backend paths to Django on `:8000`.
   - **Mode B, Django serves the built React app.** `npm run build:django`, then `python manage.py runserver`, then open `:8000`. The page is rendered through Django templates using template inheritance.
2. **Gate admin behind Django's login.** All writes through the API, and all access to the React `/admin` page, require a logged-in **superuser**. The login screen is Django's own admin login page. The person is sent to `/django-admin/login/?next=/admin` and comes back to `/admin` after signing in.
3. **Move the Django admin.** Django's built-in admin moves from `/admin/` to `/django-admin/`. The React page keeps `/admin`.
4. **Add Django forms.** `NewsForm` and `CategoryForm` (ModelForms) hold the validation, and both the Django admin and the API serializers use them. **Validation behaviour must stay identical**: same rules, same error messages.
5. **Rewrite the README** to describe the project as it is now.

Out of scope:
- Production deploys (Cloudflare Pages front end, Oracle-hosted backend). Leave the workflows, Dockerfile and production build exactly as they are. Production still builds with `npm run build`, base `/`, into `dist/`.
- Renaming the project package.
- The report and the zip.

## Before writing code, read these files

`src/config.ts`, `src/api/client.ts`, `src/api/useApi.ts`, `src/pages/Admin.tsx`, `src/components/NewsFormDialog.tsx`, `src/components/CategoryManageDialog.tsx`, `src/components/Navbar.tsx`, `index.html` (especially its inline theme script), `vite.config.ts`, `.env.example`, `backend/news/tests.py`, `backend/news/serializers.py`, `backend/config/settings.py`, `backend/Dockerfile`.

Pay particular attention to how the React dialogs display API validation errors. The error response shape must not change.

Work in the phases below. At the end of each phase, run the checks listed for it and commit before moving on. Do not push.

---

## Phase 1: Shared forms (backend only)

1. Create `backend/news/forms.py` with `CategoryForm` and `NewsForm` as `ModelForm`s.
   - `CategoryForm` (field `name`):
     - Strip whitespace and reject a blank name.
     - Reject case-insensitive duplicates with the existing message: "A category with this name already exists."
     - Django's `full_clean()` already runs `validate_constraints()`, so the model's `Lower("name")` `UniqueConstraint` may already produce this error. Test this first, and only add an explicit `clean_name` check if the test shows the constraint doesn't cover it.
   - `NewsForm` (fields `title`, `category`, `source`, `date_and_time`, `content`):
     - Keep the title minimum length of 3. This comes from the model validator.
     - Add `clean_date_and_time`, which rejects future values with the existing message: "The date and time cannot be in the future."
     - Strip whitespace from `title` and `source`.
   - Keep the model's `clean()` methods and DB constraints as they are. They protect the shell and seed command paths.
2. In `admin.py`, set `form = CategoryForm` on `CategoryAdmin` and `form = NewsForm` on `NewsAdmin`. Nothing else in the admin classes changes.
3. Make the serializers delegate validation to the forms.
   - In `validate(self, attrs)` on `NewsItemSerializer` and `CategorySerializer`:
     - Build the form data. For PATCH, start from `model_to_dict(self.instance)` and overlay the incoming `attrs`. Convert model instances (such as `category`) to their `pk`.
     - Instantiate the form with `instance=self.instance`.
     - If `form.is_valid()` fails, raise `serializers.ValidationError(form.errors)`. This keeps the field-keyed error dict the front end expects. Then return `attrs`.
   - Remove the now-duplicated `validate_date_and_time` from `NewsItemSerializer`.
   - Watch out for DRF's auto-generated `UniqueValidator` on `Category.name`. Make sure a duplicate name still returns exactly one clear error under `name`, not two.
4. Add tests:
   - The forms in isolation: blank title, short title, future date, duplicate category in different case, and whitespace stripping.
   - The admin uses the forms: `NewsAdmin.form is NewsForm`, and the same for categories.
   - The API returns the same error keys and messages as before.

**Check:** `python manage.py test` passes, `python manage.py check` is clean, `makemigrations --check` reports no changes.

---

## Phase 2: Auth and permissions (backend)

1. Move the Django admin: `path("django-admin/", admin.site.urls)` in `config/urls.py`. Update the docstring there and the comments in `settings.py`, which currently claim the API is read-only.
2. Settings:
   - `LOGIN_URL = "/django-admin/login/"`.
   - Restrict DRF to session auth: `"DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.SessionAuthentication"]`.
   - Set the default permission to a new `news.permissions.IsSuperuserOrReadOnly`. Safe methods are allowed for anyone. Unsafe methods require `request.user.is_authenticated and request.user.is_superuser`.
3. Add auth endpoints in `news/urls.py` under `/api/auth/`:
   - `GET /api/auth/me/` returns `{"authenticated": bool, "username": str | null, "is_superuser": bool}`. Decorate it with `ensure_csrf_cookie` so the React app always has a `csrftoken` cookie.
   - `POST /api/auth/logout/` calls `django.contrib.auth.logout` and returns 204. It is CSRF-protected.
   - Login itself is not an API endpoint. It is Django's admin login page.
4. Sessions and users live in the `default` DB (`auth.db`) and news lives in `news.db`. Make sure tests that touch both declare `databases = {"default", "news"}`.
5. Tests:
   - Anonymous POST/PATCH/DELETE on news and categories returns 403.
   - A logged-in staff user who is not a superuser also gets 403.
   - A logged-in superuser succeeds.
   - Anonymous GETs still succeed.
   - `/api/auth/me/` returns the right payload in each state and sets the `csrftoken` cookie.
   - Logout works, and logout without a CSRF token is rejected. Use `Client(enforce_csrf_checks=True)` for the CSRF cases.
   - `/django-admin/` responds and `/admin/` no longer reaches the Django admin.
   - Update the existing write tests to log in as a superuser first.

**Check:** all tests pass.

---

## Phase 3: Front-end auth (Mode A)

1. **Use a same-origin API in dev.** The API base currently defaults to `http://localhost:8000`, which is a different origin. Change it to default to `""`, so requests use relative URLs. `VITE_BACKEND_URL`, when set, is still used, and production CI sets it, so production stays unchanged. Update `.env.example` to match.
2. **Vite proxy.** In `vite.config.ts`, add a `server.proxy` and an identical `preview.proxy` that send `/api`, `/django-admin` and `/static` to `http://localhost:8000`.
   - Leave `changeOrigin` false (the default). The browser's `Origin` (`http://localhost:5173`) must match the forwarded `Host` header, or Django's CSRF origin check will reject the login form and API writes.
3. **`djangoAdminUrl`** in `src/config.ts` becomes `${API_BASE_URL}/django-admin/`. Add a helper `loginUrl(next: string)` that returns `${API_BASE_URL}/django-admin/login/?next=${encodeURIComponent(next)}`.
4. **CSRF on writes.** `apiMutation` reads the `csrftoken` cookie and sends it as the `X-CSRFToken` header.
   - If a mutation returns 401 or 403, redirect to `loginUrl("/admin")` (session expired or not authorised) instead of showing a generic error.
   - 400 validation errors must render exactly as they do now.
5. **Auth state.** Add a small `useAuth` hook (or a context, if the navbar needs it) that calls `/api/auth/me/` on mount.
6. **Gate `Admin.tsx`.**
   - While loading: show the existing `QueryStatus` loading state.
   - Not authenticated: `window.location.assign(loginUrl("/admin"))`. Use a full page navigation, because the login page is Django's, not a React route.
   - Authenticated but not a superuser: show a short message saying the account isn't a superuser, with a "Log out" button.
   - Superuser: show the existing page unchanged, plus a "Signed in as {username} · Log out" control.
   - Logging out POSTs to `/api/auth/logout/` with the CSRF header, then navigates to `/`.
7. **Navbar.** The Admin link stays visible to everyone. The gate is on the page itself.

**Check:** `npm run lint` and `npm run build` pass (the production build must still work). Then walk through this manually: run Django on `:8000` and `npm run dev`.
1. Visit `localhost:5173/admin` and confirm it redirects to the Django login.
2. Sign in as a superuser and confirm you land back on `/admin`.
3. Create, edit and delete a news item and a category.
4. Log out, and confirm a direct `fetch` POST to `/api/news/` returns 403.

---

## Phase 4: Django serves the React app (Mode B)

1. **Add a Vite build mode.** Add the npm script `"build:django": "tsc -b && vite build --mode django"`. In `vite.config.ts`, when `mode === "django"`, set:
   - `base: "/static/"`
   - `build.outDir: "backend/frontend_build"`
   - `build.emptyOutDir: true`
   - `build.manifest: true`

   The default mode must be untouched. Add `backend/frontend_build/` to `.gitignore`.
2. **Static files and templates.** In `settings.py`:
   - Add `BASE_DIR / "frontend_build"` to `STATICFILES_DIRS`, but only if that directory exists, to avoid the `staticfiles.W004` warning and so the Docker build doesn't break.
   - Add `BASE_DIR / "templates"` to `TEMPLATES["DIRS"]`.
3. **Template tag.** Create `news/templatetags/vite.py` with a `{% vite_assets "index.html" %}` tag.
   - It reads `frontend_build/.vite/manifest.json`, cached when `DEBUG` is off.
   - It outputs the entry's `<link rel="stylesheet">` tags and its `<script type="module">` tag, with URLs built via `static()`.
4. **Templates** in `backend/templates/` (project-level), using template inheritance:
   - `base.html`: the `<head>` (charset, viewport, `{% block title %}`, favicons via `{% static %}`), a `{% block head %}` and a `{% block content %}`.
     - The inline theme-init script must be the same as the one in `index.html`.
     - Avoid copying the script by hand: move it into `public/theme-init.js` and load it as a blocking `<script>` in the `<head>` of both `index.html` and `base.html`. Check that there is still no theme flash in either mode.
   - `spa.html` extends `base.html`. It renders `<div id="root"></div>` plus `{% vite_assets "index.html" %}`. It also outputs the current user with `{{ user_context|json_script:"django-context" }}`. React's `useAuth` seeds its initial state from this when present, then still revalidates via `/api/auth/me/`.
   - `403.html` extends `base.html`. It shows a friendly "superuser required" page with a link to log out and a link home.
   - `build_missing.html` extends `base.html`. It explains that you need to run `npm run build:django`.
5. **Views** in `news/views_spa.py`, or a separate `frontend` app if that is cleaner:
   - `SpaView(TemplateView)` renders `spa.html` with `user_context`. If the manifest is missing, it renders `build_missing.html` with status 503 instead of crashing.
   - `AdminSpaView(LoginRequiredMixin, UserPassesTestMixin, SpaView)` checks `is_superuser`. Anonymous users are redirected to `LOGIN_URL?next=/admin`. A logged-in non-superuser gets `403.html`, via `handle_no_permission` or a project `403.html` handler.
6. **URLs** in `config/urls.py`. Put these after the `api/` and `django-admin/` routes:
   - `re_path(r"^admin/?$", AdminSpaView.as_view())`
   - then a catch-all `re_path(r"^(?!api/|django-admin/|static/).*$", SpaView.as_view())`

   The catch-all lets React Router handle `/`, `/news`, `/news/<id>` and unknown paths.
7. **Tests:**
   - Use `override_settings` to point the build dir at a temp dir containing a fake manifest and fake asset files.
   - Override `STORAGES["staticfiles"]` to plain `StaticFilesStorage` in these tests. The manifest storage raises "Missing staticfiles manifest entry" when `DEBUG` is off, as it is in tests.
   - Cover these cases:
     - `/`, `/news` and `/news/5` return 200 with the `#root` div and the script tag.
     - `/admin` redirects anonymous users to the login page with `next=/admin`.
     - `/admin` returns 403 for a non-superuser and 200 for a superuser.
     - The build-missing page returns 503.
     - `/api/...` and `/django-admin/` are not swallowed by the catch-all.

**Check:** all tests, lint and both builds pass. Then walk through this manually in Mode B: run `npm run build:django`, then `runserver`, and use `localhost:8000`.
1. Open the home page, a category filter and an article.
2. Refresh on `/news/<id>` and confirm the page still loads.
3. Open `/admin` while logged out and confirm it redirects to the login, and that signing in brings you back to `/admin`.
4. Create, edit and delete news and categories.
5. Log out.
6. Open `/django-admin/` and confirm the Django admin still works.

Then repeat the Phase 3 walkthrough in Mode A to confirm nothing regressed.

---

## Phase 5: README

Replace the starter-template README completely. Remove the stale link to `backend/README.md`. Cover:

- **What the app is**: public news site plus a superuser-only admin.
- **Architecture**: React/Vite front end, Django REST API, Django admin, two SQLite DBs with the router, and how the forms are shared by the admin and the API.
- **Setup**: venv, `pip install -r backend/requirements.txt`, migrations for both DBs (`migrate` and `migrate --database news`), `createsuperuser`, `seed_news`, `npm install`.
- **Running**: Mode A and Mode B, with exact commands and URLs.
- **The login flow**: React `/admin`, then Django login, then back to `/admin`. Superuser only. CSRF handling.
- **URL table**: every route, what it does and who can access it. This covers React routes, `/admin`, the `/api/...` endpoints with their methods and permissions, `/api/auth/...` and `/django-admin/`.
- **Tests**: how to run them.
- **Production note**: Cloudflare Pages and the Oracle backend are unchanged. Admin writes from the Cloudflare-hosted front end won't authenticate, because the session cookie would be cross-site. Mode B is the supported way to use the admin.

Keep the existing Cloudflare deployment section, shortened, under a "Deployment (optional)" heading.

## Done when

- [ ] All backend tests pass, including the new ones. `check` is clean and there are no pending migrations.
- [ ] `npm run lint`, `npm run build` and `npm run build:django` all succeed.
- [ ] The Mode A and Mode B manual walkthroughs both pass.
- [ ] Anonymous and non-superuser API writes return 403.
- [ ] Validation errors look identical to before in both the React dialogs and the Django admin.
- [ ] The production workflows, Dockerfile and default build output are unchanged.
- [ ] The README is rewritten.
