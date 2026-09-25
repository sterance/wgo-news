import { Stack, Typography, Link } from "@mui/material";
import { Link as RouterLink } from "react-router-dom";
import type { NewsItem } from "../api/types.ts";
import "../components/NewsItemPreview.css";

interface Props {
  item: NewsItem;
}

export default function NewsItemPreview({ item }: Props) {
  const to = `/news/${item.id}`;
  return (
    <Stack>
      <Typography variant="h4">
        <Link component={RouterLink} to={to}>
          {item.title}
        </Link>
      </Typography>
      <div className="news-preview-body">
        <Typography variant="body1" className="truncated-body">
          {item.content}
        </Typography>
        <Link component={RouterLink} to={to} className="read-more-link">
          Read More...
        </Link>
      </div>
    </Stack>
  );
}
