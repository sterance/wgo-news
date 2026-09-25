/** "2023-08-06" -> "06 August 2023" (parsed as a local date, so no timezone shift). */
export function formatDate(iso: string): string {
  const [year, month, day] = iso.split("-").map(Number);
  return new Date(year, month - 1, day).toLocaleDateString("en-AU", {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });
}
