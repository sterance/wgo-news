import { useEffect, useState } from "react";
import { Alert, Button, Stack, Typography } from "@mui/material";
import { djangoAdminUrl, loginUrl } from "../config.ts";
import { apiMutation, endpoints, logout } from "../api/client.ts";
import type { Category, NewsInput, NewsItem } from "../api/types.ts";
import { useApi } from "../api/useApi.ts";
import { useAuth } from "../api/useAuth.ts";
import CategoryManageDialog from "../components/CategoryManageDialog.tsx";
import ConfirmationDialog from "../components/ConfirmationDialog.tsx";
import NewsFormDialog from "../components/NewsFormDialog.tsx";
import QueryStatus from "../components/QueryStatus.tsx";
import { capitaliseWords } from "../utils/formatters.ts";
import "../pages/Admin.css";

/** Superusers only. Anyone else is sent to the Django admin login, which brings them back here. */
export default function Admin() {
  const { user, loading, error } = useAuth();
  const needsLogin = user !== undefined && !user.authenticated;

  useEffect(() => {
    // Full page load: the login page is Django's, not a React route.
    if (needsLogin) window.location.assign(loginUrl("/admin"));
  }, [needsLogin]);

  if (loading || needsLogin || user === undefined) {
    return (
      <Stack className="base-stack">
        <QueryStatus
          loading={loading || needsLogin}
          error={error}
        />
      </Stack>
    );
  }

  if (!user.is_superuser) {
    return (
      <Stack className="base-stack">
        <Typography
          variant="h2"
          align="center"
        >
          Admin
        </Typography>
        <Alert
          severity="warning"
          action={
            <Button
              color="inherit"
              size="small"
              onClick={logout}
            >
              Log out
            </Button>
          }
        >
          You are signed in as {user.username}, which is not a superuser account. Log in with a superuser to manage the news.
        </Alert>
      </Stack>
    );
  }

  return <AdminDashboard username={user.username ?? ""} />;
}

function AdminDashboard({ username }: { username: string }) {
  const news = useApi<NewsItem[]>(endpoints.news());
  const categories = useApi<Category[]>(endpoints.categories());
  const [formItem, setFormItem] = useState<NewsItem>();
  const [formOpen, setFormOpen] = useState(false);
  const [deleteItem, setDeleteItem] = useState<NewsItem>();
  const [categoriesOpen, setCategoriesOpen] = useState(false);

  const saveNews = async (input: NewsInput, id?: number) => {
    await apiMutation<NewsItem>(id === undefined ? endpoints.createNews() : endpoints.updateNews(id), id === undefined ? "POST" : "PATCH", input);
    news.refetch();
  };

  const deleteNews = async () => {
    if (deleteItem === undefined) return;
    await apiMutation<void>(endpoints.deleteNews(deleteItem.id), "DELETE");
    setDeleteItem(undefined);
    news.refetch();
  };

  const saveCategory = async (name: string, id?: number) => {
    await apiMutation<Category>(id === undefined ? endpoints.createCategory() : endpoints.updateCategory(id), id === undefined ? "POST" : "PATCH", { name });
    categories.refetch();
    news.refetch();
  };

  const deleteCategory = async (category: Category) => {
    await apiMutation<void>(endpoints.deleteCategory(category.id), "DELETE");
    categories.refetch();
    news.refetch();
  };

  return (
    <Stack className="base-stack">
      <Typography
        variant="h2"
        align="center"
      >
        Admin
      </Typography>

      <Typography
        variant="body2"
        align="center"
        className="admin-signed-in"
      >
        Signed in as {username} ·{" "}
        <Button
          size="small"
          onClick={logout}
        >
          Log out
        </Button>
      </Typography>

      <Stack
        direction="row"
        useFlexGap
        spacing={1.5}
        className="admin-actions"
      >
        <Button
          variant="contained"
          onClick={() => {
            setFormItem(undefined);
            setFormOpen(true);
          }}
        >
          Create Article
        </Button>
        <Button
          variant="outlined"
          onClick={() => setCategoriesOpen(true)}
        >
          Manage categories
        </Button>
        <Button
          variant="outlined"
          href={djangoAdminUrl()}
          target="_blank"
          rel="noopener"
        >
          Open Django admin
        </Button>
      </Stack>

      <QueryStatus
        loading={news.loading || categories.loading}
        error={news.error ?? categories.error}
      />

      <Stack
        direction="row"
        useFlexGap
        spacing={2}
        className="admin-item admin-header"
      >
        <Typography
          variant="body2"
          className="admin-column-label"
        >
          Article
        </Typography>
        <Typography
          variant="body2"
          className="admin-column-label"
        >
          Category
        </Typography>
        <Typography
          variant="body2"
          className="admin-column-label admin-actions-label"
        >
          Actions
        </Typography>
      </Stack>

      {news.data?.map((item) => (
        <Stack
          key={item.id}
          direction="row"
          useFlexGap
          spacing={2}
          className="admin-item"
        >
          <Typography
            variant="h6"
            component="h3"
          >
            {item.title}
          </Typography>
          <Typography
            component="span"
            variant="body2"
            className="admin-category"
          >
            {capitaliseWords(item.category.name)}
          </Typography>
          <Stack
            direction="row"
            spacing={1.5}
            className="admin-item-actions"
          >
            <Button
              size="small"
              onClick={() => {
                setFormItem(item);
                setFormOpen(true);
              }}
            >
              Edit
            </Button>
            <Button
              size="small"
              color="error"
              onClick={() => setDeleteItem(item)}
            >
              Delete
            </Button>
          </Stack>
        </Stack>
      ))}
      {news.data?.length === 0 && <Typography className="admin-empty">No news yet. Use "Create News" to add some.</Typography>}

      <NewsFormDialog
        key={`${formOpen}-${formItem?.id ?? "new"}`}
        open={formOpen}
        item={formItem}
        categories={categories.data ?? []}
        onClose={() => setFormOpen(false)}
        onSubmit={saveNews}
      />
      <CategoryManageDialog
        open={categoriesOpen}
        categories={categories.data ?? []}
        onClose={() => setCategoriesOpen(false)}
        onSave={saveCategory}
        onDelete={deleteCategory}
      />
      <ConfirmationDialog
        open={deleteItem !== undefined}
        title="Delete news?"
        message={`This will permanently delete "${deleteItem?.title}".`}
        confirmLabel="Delete"
        confirmingLabel="Deleting..."
        confirmColor="error"
        onClose={() => setDeleteItem(undefined)}
        onConfirm={deleteNews}
      />
    </Stack>
  );
}
