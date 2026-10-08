export const APP_NAME = `"What's Going On?" News`;

export interface NavLink {
  label: string;
  href: string;
}

// Django backend. Empty means same origin: the Vite dev server proxies to
// Django, or Django serves the built app itself. Production sets VITE_BACKEND_URL.
const BACKEND_URL = ((import.meta.env.VITE_BACKEND_URL as string | undefined) || "").replace(/\/+$/, "");

// link into Django admin site
export const djangoAdminUrl = (path = "") => `${BACKEND_URL}/django-admin/${path}`;

// Django admin login page; sends the person back to `next` afterwards
export const loginUrl = (next: string) => `${BACKEND_URL}/django-admin/login/?next=${encodeURIComponent(next)}`;

export const NAV_LINKS: NavLink[] = [
  { label: "Home", href: "/" },
  { label: "News", href: "/news" },
  { label: "Admin", href: "/admin" },
];

export const API_BASE_URL = `${BACKEND_URL}/api`;
