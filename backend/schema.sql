BEGIN;
--
-- Create model Category
--
CREATE TABLE "news_category" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL UNIQUE);
--
-- Create model News
--
CREATE TABLE "news_news" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(200) NOT NULL, "source" varchar(100) NOT NULL, "date_and_time" datetime NOT NULL, "content" text NOT NULL, "category_id" bigint NOT NULL REFERENCES "news_category" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "category_name_unique_ci" ON "news_category" ((LOWER("name")));
CREATE INDEX "news_news_category_id_f060a768" ON "news_news" ("category_id");
CREATE INDEX "news_date_time_idx" ON "news_news" ("date_and_time" DESC);
COMMIT;
