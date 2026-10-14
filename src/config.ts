export const APP_NAME = `"What's Going On?" News`;

export interface NavLink {
  label: string;
  href: string;
}

const BACKEND_URL = ((import.meta.env.VITE_BACKEND_URL as string | undefined) || "").replace(/\/+$/, "");

export const djangoAdminUrl = (path = "") => `${BACKEND_URL}/django-admin/${path}`;

export const loginUrl = (next: string) => `${BACKEND_URL}/django-admin/login/?next=${encodeURIComponent(next)}`;

export const NAV_LINKS: NavLink[] = [
  { label: "Home", href: "/" },
  { label: "News", href: "/news" },
  { label: "Admin", href: "/admin" },
];

export const API_BASE_URL = `${BACKEND_URL}/api`;
