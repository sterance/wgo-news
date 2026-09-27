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
  const [searchParams, setSearchParams] = useSearchParams();
  const rawCategories = searchParams.getAll("category");
  const selectedIds = rawCategories.map((val) => Number(val)).filter((num) => !isNaN(num) && num > 0);
  const showAll = selectedIds.length === 0;

  const categories = useApi<Category[]>(endpoints.categories());
  const news = useApi<NewsItem[]>(endpoints.news());

  const selectCategory = (id?: number) => {
    if (id === undefined) {
      setSearchParams({});
      return;
    }
    if (showAll) {
      setSearchParams({ category: String(id) });
    } else {
      const current = searchParams.getAll("category").map(Number);
      const index = current.indexOf(id);
      const updated = (index >= 0 ? current.filter((_, i) => i !== index) : [...current, id]).map(String);
      if (updated.length === 0) {
        setSearchParams({});
      } else {
        const params = new URLSearchParams();
        updated.forEach((catId) => params.append("category", catId));
        setSearchParams(params);
      }
    }
  };

  const groups = (categories.data ?? [])
    .filter((category) => (showAll ? true : selectedIds.includes(category.id)))
    .map((category) => ({
      category,
      items: (news.data ?? []).filter((item) => item.category.id === category.id),
    }))
    .filter((group) => (showAll ? group.items.length > 0 : true));

  return (
    <Stack className="base-stack">
      <Typography variant="h2" align="center">
        Categories
      </Typography>

      <Stack direction="row" useFlexGap spacing={1.5} className="category-chips news-chips">
        <CategoryChip label="All" selected={showAll} onClick={() => selectCategory()} />
        {categories.data?.map((category) => (
          <CategoryChip key={category.id} label={capitaliseWords(category.name)} selected={selectedIds.includes(category.id)} onClick={() => selectCategory(category.id)} />
        ))}
      </Stack>

      <QueryStatus loading={categories.loading || news.loading} error={categories.error ?? news.error} />

      {groups.map(({ category, items }) => (
        <Stack key={category.id} className="news-category-stack">
          <Typography variant="h4" component="h3">
            {capitaliseWords(category?.name)}
          </Typography>
          {items.map((item) => (
            <NewsItemPreview key={item.id} item={item} />
          ))}
          {items.length === 0 && <Typography className="news-no-articles">No articles in this category yet.</Typography>}
        </Stack>
      ))}
    </Stack>
  );
}
