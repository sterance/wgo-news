import { Chip, Link, Stack, Typography } from "@mui/material";
import { Link as RouterLink, useParams } from "react-router-dom";
import { endpoints } from "../api/client.ts";
import type { NewsItem } from "../api/types.ts";
import { useApi } from "../api/useApi.ts";
import QueryStatus from "../components/QueryStatus.tsx";
import { capitaliseWords } from "../utils/formatters.ts";
import dayjs from "dayjs";

export default function Article() {
  const { id } = useParams();
  const validId = id !== undefined && /^\d+$/.test(id);

  const { data: article, loading, error } = useApi<NewsItem>(validId ? endpoints.article(id) : null);

  return (
    <Stack className="base-stack" spacing={1.5} sx={{ pt: 2 }}>
      <Link component={RouterLink} to="/news" underline="hover" sx={{ alignSelf: "flex-start" }}>
        ← Back to news
      </Link>

      {!validId && <Typography>Article not found.</Typography>}
      <QueryStatus loading={loading} error={error} />

      {article && (
        <>
          <Typography variant="h3" component="h1" sx={{ fontWeight: 700 }}>
            {article.title}
          </Typography>
          <Stack direction="row" spacing={1} sx={{ alignItems: "center" }}>
            <Typography>Category:</Typography>
            <Chip component={RouterLink} to={`/news?category=${article.category.id}`} label={capitaliseWords(article.category.name)} variant="outlined" size="small" clickable />
          </Stack>
          <Typography>Source: {article.source}</Typography>
          <Typography>
            Published: {dayjs(article.date_and_time).format("DD MMMM YYYY")}, {dayjs(article.date_and_time).format("hh:mm a")}
          </Typography>
          <Typography sx={{ whiteSpace: "pre-line", pt: 2 }}>{article.content}</Typography>
        </>
      )}
    </Stack>
  );
}
