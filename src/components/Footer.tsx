import { Link } from "react-router-dom";
import { Box } from "@mui/material";
import GitHubIcon from "@mui/icons-material/GitHub";
import "./Footer.css";

export function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="footer">
      <Box className="footer-content">
        <span>© Chris Smith {year}</span>
        <Link
          to="https://www.github.com/sterance/wgo-news"
          target="_blank"
          rel="noopener noreferrer"
        >
          <GitHubIcon />
        </Link>
      </Box>
    </footer>
  );
}
