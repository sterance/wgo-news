import { Alert, Box, CircularProgress } from "@mui/material";

interface Props {
  loading: boolean;
  error?: { message: string };
}

/** Shows a spinner or an error message; renders nothing once data is ready. */
export default function QueryStatus({ loading, error }: Props) {
  if (loading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", py: 4 }}>
        <CircularProgress aria-label="Loading" />
      </Box>
    );
  }
  if (error) return <Alert severity="error">{error.message}</Alert>;
  return null;
}
