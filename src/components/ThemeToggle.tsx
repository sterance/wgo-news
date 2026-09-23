import { useTheme } from "../theme/useTheme.ts";
import "./ThemeToggle.css";
import { Brightness4, Brightness7 } from "@mui/icons-material";

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();
  const label = `Switch to ${theme === "dark" ? "light" : "dark"} theme`;

  return (
    <button type="button" className="theme-toggle" onClick={toggleTheme} aria-label={label} title={label}>
      {theme === "dark" ? <Brightness4 /> : <Brightness7 />}
    </button>
  );
}
