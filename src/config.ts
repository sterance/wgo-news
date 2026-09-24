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
