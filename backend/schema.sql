BEGIN;
--
-- Create model Category
--
CREATE TABLE "category" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL UNIQUE);
--
-- Create model News
--
CREATE TABLE "article" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(200) NOT NULL, "source" varchar(100) NOT NULL, "date_and_time" datetime NOT NULL, "content" text NOT NULL, "category_id" bigint NOT NULL REFERENCES "category" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "category_name_unique_ci" ON "category" ((LOWER("name")));
CREATE INDEX "article_category_id_99127861" ON "article" ("category_id");
CREATE INDEX "news_date_time_idx" ON "article" ("date_and_time" DESC);
COMMIT;
