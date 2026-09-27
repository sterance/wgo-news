import { Alert, Box, CircularProgress } from "@mui/material";
import "./QueryStatus.css";

interface Props {
  loading: boolean;
  error?: { message: string };
}

/** Shows a spinner or an error message; renders nothing once data is ready. */
export default function QueryStatus({ loading, error }: Props) {
  if (loading) {
    return (
      <Box className="query-status-container">
        <CircularProgress aria-label="Loading" />
      </Box>
    );
  }
  if (error) return <Alert severity="error">{error.message}</Alert>;
  return null;
}