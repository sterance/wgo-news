import Chip from "@mui/material/Chip";

interface Props {
  label: string;
  selected?: boolean;
  onClick?: () => void;
}

export default function CategoryChip({ label, selected = false, onClick }: Props) {
  return (
    <Chip
      label={label}
      variant="outlined"
      onClick={onClick}
      className={selected ? "category-chip--selected" : undefined}
      aria-pressed={selected}
    />
  );
}
