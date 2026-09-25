import { Typography, Stack } from "@mui/material";
import { useSearchParams } from "react-router-dom";
import { endpoints } from "../api/client.ts";
import type { Category, NewsItem } from "../api/types.ts";
import { useApi } from "../api/useApi.ts";
import CategoryChip from "../components/CategoryChip";
import NewsItemPreview from "../components/NewsItemPreview";
import QueryStatus from "../components/QueryStatus.tsx";
import { capitaliseWords } from "../utils/formatters.ts";
import "../pages/News.css";

export default function News() {
  // The selected category lives in the URL (/news?category=3) so it can be shared.
  const [searchParams, setSearchParams] = useSearchParams();
  const rawCategory = Number(searchParams.get("category"));
  const selectedId = Number.isInteger(rawCategory) && rawCategory > 0 ? rawCategory : undefined;

  const categories = useApi<Category[]>(endpoints.categories());
  const news = useApi<NewsItem[]>(endpoints.news({ category: selectedId }));

  const selectCategory = (id?: number) => setSearchParams(id === undefined ? {} : { category: String(id) });

  const groups = (categories.data ?? [])
    .filter((category) => (selectedId === undefined ? true : category.id === selectedId))
    .map((category) => ({
      category,
      items: (news.data ?? []).filter((item) => item.category.id === category.id),
    }))
    .filter((group) => selectedId !== undefined || group.items.length > 0);

  return (
    <Stack className="base-stack">
      <Typography variant="h2" align="center">
        Categories
      </Typography>

      <Stack direction="row" useFlexGap spacing={1.5} className="category-chips" sx={{ marginTop: "1rem !important", flexWrap: "wrap" }}>
        <CategoryChip label="All" selected={selectedId === undefined} onClick={() => selectCategory()} />
        {categories.data?.map((category) => (
          <CategoryChip key={category.id} label={category.name.replace(/\b\w/g, (char) => char.toUpperCase())} selected={category.id === selectedId} onClick={() => selectCategory(category.id)} />
        ))}
      </Stack>

      <QueryStatus loading={categories.loading || news.loading} error={categories.error ?? news.error} />

      {groups.map(({ category, items }) => (
        <Stack key={category.id}>
          <Typography variant="h5" component="h3">
            {capitaliseWords(category?.name)}
          </Typography>
          {items.map((item) => (
            <NewsItemPreview key={item.id} item={item} />
          ))}
          {items.length === 0 && <Typography sx={{ mt: 1 }}>No articles in this category yet.</Typography>}
        </Stack>
      ))}
    </Stack>
  );
}
