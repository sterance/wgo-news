import { Stack, Typography, Link } from "@mui/material";
import { Link as RouterLink } from "react-router-dom";
import type { NewsItem } from "../api/types.ts";
import dayjs from "dayjs";
import "../components/NewsItemPreview.css";

interface Props {
  item: NewsItem;
}

export default function NewsItemPreview({ item }: Props) {
  const to = `/news/${item.id}`;
  return (
    <Stack className="news-preview">
      <Stack direction="row" spacing={2} className="news-preview-header">
        <Typography variant="h4">
          <Link component={RouterLink} to={to}>
            {item.title}
          </Link>
        </Typography>
        <Typography variant="caption">
          {dayjs(item.date_and_time).format("DD MMMM YYYY")}, {dayjs(item.date_and_time).format("hh:mm a")}
        </Typography>
      </Stack>

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