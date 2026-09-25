import { Button, Link, Stack, Typography } from "@mui/material";
import { djangoAdminUrl } from "../config.ts";
import { endpoints } from "../api/client.ts";
import type { NewsItem } from "../api/types.ts";
import { useApi } from "../api/useApi.ts";
import QueryStatus from "../components/QueryStatus.tsx";
import { capitaliseWords } from "../utils/formatters.ts";

const newsAdmin = (path: string) => djangoAdminUrl(`news/news/${path}`);

export default function Admin() {
  const { data, loading, error } = useApi<NewsItem[]>(endpoints.news());

  return (
    <Stack className="base-stack">
      <Typography variant="h2" align="center">
        Admin
      </Typography>

      <Stack direction="row" useFlexGap spacing={1.5} sx={{ mt: 2, flexWrap: "wrap" }}>
        <Button variant="contained" href={newsAdmin("add/")} target="_blank" rel="noopener">
          Create News
        </Button>
        <Button variant="outlined" href={djangoAdminUrl("news/category/")} target="_blank" rel="noopener">
          Manage categories
        </Button>
        <Button variant="outlined" href={djangoAdminUrl()} target="_blank" rel="noopener">
          Open Django admin
        </Button>
      </Stack>

      <Typography variant="body2" sx={{ mt: 1, color: "var(--text-muted)" }}>
        Editing opens Django's admin site and needs a staff login. Changes appear here after a refresh.
      </Typography>

      <QueryStatus loading={loading} error={error} />

      {data?.map((item) => (
        <Stack key={item.id} direction="row" useFlexGap spacing={2} sx={{ mt: 2, alignItems: "baseline", justifyContent: "space-between", flexWrap: "wrap" }}>
          <Typography variant="h6" component="h3">
            {item.title}
            <Typography component="span" variant="body2" sx={{ ml: 1, color: "var(--text-muted)" }}>
              {capitaliseWords(item.category.name)}
            </Typography>
          </Typography>
          <Stack direction="row" spacing={1.5}>
            <Link href={newsAdmin(`${item.id}/change/`)} target="_blank" rel="noopener">
              Edit
            </Link>
            <Link href={newsAdmin(`${item.id}/delete/`)} target="_blank" rel="noopener">
              Delete
            </Link>
          </Stack>
        </Stack>
      ))}
      {data?.length === 0 && <Typography sx={{ mt: 2 }}>No news yet. Use "Create News" to add some.</Typography>}
    </Stack>
  );
}
