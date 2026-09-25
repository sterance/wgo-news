// Shapes returned by the Django API (backend/news/serializers.py)
import dayjs from "dayjs";

export interface Category {
  id: number;
  name: string;
  article_count: number;
}

export interface NewsItem {
  id: number;
  title: string;
  category: Category;
  source: string;
  date_and_time: dayjs.Dayjs;
  content: string;
}
