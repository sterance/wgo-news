"""Send the news app to the "news" database and everything else to "default"."""

NEWS_DB = "news"


class NewsRouter:
    def db_for_read(self, model, **hints):
        return NEWS_DB if model._meta.app_label == "news" else None

    db_for_write = db_for_read

    def allow_relation(self, obj1, obj2, **hints):
        # Only allow relations within the same database.
        return obj1._state.db == obj2._state.db

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # news tables only in news.db; all other apps only in auth.db.
        return (db == NEWS_DB) == (app_label == "news")
