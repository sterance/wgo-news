import { useState } from "react";
import dayjs from "dayjs";
import { Alert, Button, Dialog, DialogActions, DialogContent, DialogTitle, MenuItem, Stack, TextField } from "@mui/material";
import { ApiError } from "../api/client.ts";
import type { Category, NewsInput, NewsItem } from "../api/types.ts";
import { capitaliseWords } from "../utils/formatters.ts";
import "./NewsFormDialog.css";

interface NewsFormDialogProps {
  open: boolean;
  item?: NewsItem;
  categories: Category[];
  onClose: () => void;
  onSubmit: (input: NewsInput, id?: number) => Promise<void>;
}

const emptyForm = (): NewsInput => ({
  title: "",
  category: 0,
  source: "",
  date_and_time: dayjs().format("YYYY-MM-DDTHH:mm"),
  content: "",
});

const formFromItem = (item: NewsItem): NewsInput => ({
  title: item.title,
  category: item.category.id,
  source: item.source,
  date_and_time: dayjs(item.date_and_time).format("YYYY-MM-DDTHH:mm"),
  content: item.content,
});

export default function NewsFormDialog({ open, item, categories, onClose, onSubmit }: NewsFormDialogProps) {
  const [form, setForm] = useState<NewsInput>(() => (item ? formFromItem(item) : emptyForm()));
  const [error, setError] = useState<ApiError>();
  const [submitting, setSubmitting] = useState(false);
  const editing = item !== undefined;

  const updateField = (field: keyof NewsInput, value: string | number) => {
    setForm((current) => ({ ...current, [field]: value }));
    setError(undefined);
  };

  const fieldError = (field: keyof NewsInput) => error?.details?.[field]?.[0];

  const submit = async () => {
    setSubmitting(true);
    setError(undefined);
    try {
      await onSubmit({ ...form, date_and_time: dayjs(form.date_and_time).toISOString() }, item?.id);
      onClose();
    } catch (reason) {
      setError(reason instanceof ApiError ? reason : new ApiError(0, "Something went wrong."));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Dialog
      open={open}
      onClose={submitting ? undefined : onClose}
      fullWidth
      maxWidth="md"
      className="dialog"
    >
      <DialogTitle className="dialog__title" sx={{ p: 2 }}>{editing ? "Edit Article" : "Create Article"}</DialogTitle>
      <DialogContent className="dialog__body">
        <Stack
          spacing={2}
          sx={{ pt: 1 }}
        >
          {error && <Alert severity="error">{error.message}</Alert>}
          <TextField
            label="Title"
            value={form.title}
            onChange={(event) => updateField("title", event.target.value)}
            error={Boolean(fieldError("title"))}
            helperText={fieldError("title")}
            required
            autoFocus
            fullWidth
            className="form-field"
          />
          <TextField
            select
            label="Category"
            value={form.category || ""}
            onChange={(event) => updateField("category", Number(event.target.value))}
            error={Boolean(fieldError("category"))}
            helperText={fieldError("category")}
            required
            fullWidth
            className="form-field"
          >
            {categories.map((category) => (
              <MenuItem
                key={category.id}
                value={category.id}
              >
                {capitaliseWords(category.name)}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            label="Source"
            value={form.source}
            onChange={(event) => updateField("source", event.target.value)}
            error={Boolean(fieldError("source"))}
            helperText={fieldError("source")}
            required
            fullWidth
            className="form-field"
          />
          <TextField
            label="Date and time"
            type="datetime-local"
            value={form.date_and_time}
            onChange={(event) => updateField("date_and_time", event.target.value)}
            error={Boolean(fieldError("date_and_time"))}
            helperText={fieldError("date_and_time")}
            slotProps={{ inputLabel: { shrink: true } }}
            required
            fullWidth
            className="form-field"
          />
          <TextField
            label="Content"
            value={form.content}
            onChange={(event) => updateField("content", event.target.value)}
            error={Boolean(fieldError("content"))}
            helperText={fieldError("content")}
            multiline
            minRows={5}
            required
            fullWidth
            className="form-field"
          />
        </Stack>
      </DialogContent>
      <DialogActions className="dialog__actions">
        <Button
          onClick={onClose}
          disabled={submitting}
        >
          Cancel
        </Button>
        <Button
          onClick={submit}
          variant="contained"
          disabled={submitting || form.category === 0}
          className="submit-btn"
        >
          {submitting ? "Saving..." : editing ? "Save changes" : "Create article"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
