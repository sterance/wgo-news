import { useState, type ReactNode } from "react";
import { Alert, Button, Dialog, DialogActions, DialogContent, DialogTitle } from "@mui/material";
import type { ButtonProps } from "@mui/material/Button";
import { ApiError } from "../api/client.ts";
import "./ConfirmationDialog.css";

interface ConfirmationDialogProps {
  open: boolean;
  title: string;
  message: ReactNode;
  confirmLabel: string;
  confirmingLabel: string;
  confirmColor?: ButtonProps["color"];
  onClose: () => void;
  onConfirm: () => Promise<void>;
}

export default function ConfirmationDialog({ open, title, message, confirmLabel, confirmingLabel, confirmColor = "primary", onClose, onConfirm }: ConfirmationDialogProps) {
  const [error, setError] = useState<ApiError>();
  const [confirming, setConfirming] = useState(false);

  const confirm = async () => {
    setConfirming(true);
    setError(undefined);
    try {
      await onConfirm();
      onClose();
    } catch (reason) {
      setError(reason instanceof ApiError ? reason : new ApiError(0, "Something went wrong."));
    } finally {
      setConfirming(false);
    }
  };

  return (
    <Dialog
      open={open}
      onClose={confirming ? undefined : onClose}
      className="confirmation-dialog"
    >
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>
        {error && (
          <Alert
            severity="error"
            sx={{ mb: 2 }}
          >
            {error.message}
          </Alert>
        )}
        {message}
      </DialogContent>
      <DialogActions>
        <Button
          onClick={onClose}
          disabled={confirming}
        >
          Cancel
        </Button>
        <Button
          onClick={confirm}
          color={confirmColor}
          variant="contained"
          disabled={confirming}
        >
          {confirming ? confirmingLabel : confirmLabel}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
