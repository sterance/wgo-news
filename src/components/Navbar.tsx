import { APP_NAME, NAV_LINKS } from "../config.ts";
import { ThemeToggle } from "./ThemeToggle.tsx";
import "./Navbar.css";

export function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar__inner">
        <a className="navbar__brand" href="/">
          {APP_NAME}
        </a>

        {NAV_LINKS.length > 0 && (
          <nav className="navbar__nav" aria-label="Main">
            <ul>
              {NAV_LINKS.map((link) => (
                <li key={link.href}>
                  <a href={link.href}>{link.label}</a>
                </li>
              ))}
            </ul>
          </nav>
        )}

        <div className="navbar__actions">
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
