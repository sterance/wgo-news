import { Typography, Stack } from "@mui/material";
import CategoryChip from "../components/CategoryChip";
import "../pages/News.css";

export default function News() {
  return (
    <Stack className="base-stack">
      <Typography variant="h2" align="center">
        Categories
      </Typography>
      <Stack direction="row" spacing={2} className="category-chips">
        <CategoryChip></CategoryChip>
      </Stack>
    </Stack>
  );
}
