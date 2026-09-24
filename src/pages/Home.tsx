import { Stack, Typography } from "@mui/material";
import NewsItemPreview from "../components/NewsItemPreview";

export default function Home() {
  return (
    <Stack className="base-stack">
      <Typography variant="h2" align="center">
        Recent News
      </Typography>
      <NewsItemPreview></NewsItemPreview>
      <NewsItemPreview></NewsItemPreview>
      <NewsItemPreview></NewsItemPreview>
      <NewsItemPreview></NewsItemPreview>
    </Stack>
  );
}
