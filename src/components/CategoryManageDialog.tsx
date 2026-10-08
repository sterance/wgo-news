import { useState } from "react";
import { Alert, Button, Dialog, DialogActions, DialogContent, DialogTitle, IconButton, Stack, TextField, Typography } from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import CheckIcon from "@mui/icons-material/Check";
import CloseIcon from "@mui/icons-material/Close";
import { ApiError, endpoints } from "../api/client.ts";
import type { Category, NewsItem } from "../api/types.ts";
import { useApi } from "../api/useApi.ts";
import ConfirmationDialog from "./ConfirmationDialog.tsx";
import { capitaliseWords } from "../utils/formatters.ts";
import "./CategoryManageDialog.css";

interface CategoryManageDialogProps {
  open: boolean;
  categories: Category[];
  onClose: () => void;
  onSave: (name: string, id?: number) => Promise<void>;
  onDelete: (category: Category) => Promise<void>;
}

export default function CategoryManageDialog({ open, categories, onClose, onSave, onDelete }: CategoryManageDialogProps) {
  const [editingCategory, setEditingCategory] = useState<Category>();
  const [name, setName] = useState("");
  const [editingName, setEditingName] = useState("");
  const [error, setError] = useState<ApiError>();
  const [submitting, setSubmitting] = useState(false);
  const [deleteCategory, setDeleteCategory] = useState<Category>();
  const pendingDeletion = useApi<NewsItem[]>(deleteCategory === undefined ? null : endpoints.news({ category: deleteCategory.id }));

  const startCreate = () => {
    setEditingCategory(undefined);
    setName("");
    setError(undefined);
  };

  const startEdit = (category: Category) => {
    setEditingCategory(category);
    setEditingName(category.name);
    setError(undefined);
  };

  const saveNewCategory = async () => {
    setSubmitting(true);
    setError(undefined);
    try {
      await onSave(name.trim());
      setName("");
    } catch (reason) {
      setError(reason instanceof ApiError ? reason : new ApiError(0, "Something went wrong."));
    } finally {
      setSubmitting(false);
    }
  };

  const saveRename = async () => {
    if (editingCategory === undefined) return;
    setSubmitting(true);
    setError(undefined);
    try {
      await onSave(editingName.trim(), editingCategory.id);
      startCreate();
    } catch (reason) {
      setError(reason instanceof ApiError ? reason : new ApiError(0, "Something went wrong."));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <>
      <Dialog
        open={open}
        onClose={submitting ? undefined : onClose}
        fullWidth
        maxWidth="sm"
        className="category-manage-dialog"
      >
        <DialogTitle>Manage categories</DialogTitle>
        <DialogContent>
          <Stack
            spacing={2}
            sx={{ pt: 1 }}
          >
            {error && <Alert severity="error">{error.message}</Alert>}
            <Stack
              direction="row"
              spacing={1}
            >
              <TextField
                label="New category"
                value={name}
                onChange={(event) => {
                  setName(event.target.value);
                  setError(undefined);
                }}
                slotProps={{
                  input: { required: true },
                }}
                fullWidth
                autoFocus
                disabled={submitting || editingCategory !== undefined}
              />
              <Button
                variant="contained"
                onClick={saveNewCategory}
                disabled={submitting || name.trim() === ""}
              >
                {submitting ? "Saving..." : "Add"}
              </Button>
            </Stack>
            <Stack spacing={0.5}>
              {categories.map((category) => (
                <Stack
                  key={category.id}
                  direction="row"
                  sx={{ alignItems: "center", justifyContent: "space-between" }}
                >
                  {editingCategory?.id === category.id ? (
                    <TextField
                      value={editingName}
                      onChange={(event) => {
                        setEditingName(event.target.value);
                        setError(undefined);
                      }}
                      size="small"
                      autoFocus
                      fullWidth
                      disabled={submitting}
                      slotProps={{ htmlInput: { "aria-label": `Rename ${category.name}` } }}
                    />
                  ) : (
                    <Typography>{capitaliseWords(category.name)}</Typography>
                  )}
                  <Stack direction="row">
                    {editingCategory?.id === category.id ? (
                      <>
                        <IconButton
                          aria-label={`Save rename for ${category.name}`}
                          onClick={saveRename}
                          disabled={submitting || editingName.trim() === ""}
                        >
                          <CheckIcon fontSize="small" />
                        </IconButton>
                        <IconButton
                          aria-label="Cancel rename"
                          onClick={startCreate}
                          disabled={submitting}
                        >
                          <CloseIcon fontSize="small" />
                        </IconButton>
                      </>
                    ) : (
                      <IconButton
                        aria-label={`Rename ${category.name}`}
                        onClick={() => startEdit(category)}
                        disabled={submitting || editingCategory !== undefined}
                      >
                        <EditIcon fontSize="small" />
                      </IconButton>
                    )}
                    <IconButton
                      aria-label={`Delete ${category.name}`}
                      onClick={() => setDeleteCategory(category)}
                      disabled={submitting}
                    >
                      <DeleteIcon fontSize="small" />
                    </IconButton>
                  </Stack>
                </Stack>
              ))}
            </Stack>
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button
            onClick={onClose}
            disabled={submitting}
          >
            Close
          </Button>
        </DialogActions>
      </Dialog>
      <ConfirmationDialog
        open={deleteCategory !== undefined}
        title="Delete category?"
        message={
          <>
            <Typography>
              This will permanently delete "{deleteCategory?.name}"{pendingDeletion.data?.length === 0 ? "." : " and the following articles:"}
            </Typography>
            {pendingDeletion.data !== undefined && pendingDeletion.data.length > 0 && (
              <ul>
                {pendingDeletion.data.map((item) => (
                  <li key={item.id}>{item.title}</li>
                ))}
              </ul>
            )}
          </>
        }
        confirmLabel="Delete"
        confirmingLabel="Deleting..."
        confirmColor="error"
        onClose={() => setDeleteCategory(undefined)}
        onConfirm={async () => {
          if (deleteCategory !== undefined) await onDelete(deleteCategory);
          setDeleteCategory(undefined);
        }}
      />
    </>
  );
}
