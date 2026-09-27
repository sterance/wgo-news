import { Stack, Typography } from "@mui/material";
import { endpoints } from "../api/client.ts";
import type { NewsItem } from "../api/types.ts";
import { useApi } from "../api/useApi.ts";
import NewsItemPreview from "../components/NewsItemPreview";
import QueryStatus from "../components/QueryStatus.tsx";
import "../pages/Home.css";

const RECENT_COUNT = 4;

export default function Home() {
  const { data, loading, error } = useApi<NewsItem[]>(endpoints.news({ limit: RECENT_COUNT }));

  return (
    <Stack className="base-stack home-stack">
      <Typography variant="h2" align="center">
        Recent News
      </Typography>
      <QueryStatus loading={loading} error={error} />
      {data?.map((item) => (
        <NewsItemPreview key={item.id} item={item} />
      ))}
      {data?.length === 0 && <Typography className="home-empty">No news has been published yet.</Typography>}
    </Stack>
  );
}
