export const APP_NAME = `"What's Going On?" News`;

export interface NavLink {
  label: string;
  href: string;
}

export const NAV_LINKS: NavLink[] = [
  { label: "Home", href: "/" },
  { label: "News", href: "/news" },
  { label: "Admin", href: "/admin" },
];

// link to django backend
const BACKEND_URL = ((import.meta.env.VITE_BACKEND_URL as string | undefined) || "http://localhost:8000").replace(/\/+$/, "");

export const API_BASE_URL = `${BACKEND_URL}/api`;

// link into Django admin site
export const djangoAdminUrl = (path = "") => `${BACKEND_URL}/admin/${path}`;
