export const capitaliseWords = (str: string | null | undefined): string => {
  if (!str) return "";
  return str.replace(/\b\w/g, (char) => char.toUpperCase());
};
