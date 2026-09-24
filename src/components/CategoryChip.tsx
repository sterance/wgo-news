import { Stack } from "@mui/material";
import Chip from "@mui/material/Chip";

export default function CategoryChip() {
  return (
    <Stack direction="row" spacing={2} sx={{ marginTop: "1rem !important" }}>
      <Chip label="Category 1" variant="outlined" />
      <Chip label="Category 2" variant="outlined" />
      <Chip label="Category 3" variant="outlined" />
      <Chip label="Category 4" variant="outlined" />
      <Chip label="Category 5" variant="outlined" />
    </Stack>
  );
}
