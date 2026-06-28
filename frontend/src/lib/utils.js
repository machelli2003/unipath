import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Merges Tailwind class names safely, resolving conflicts (e.g. p-2 vs p-4)
 * the way shadcn/ui components expect. Used throughout components/ui/.
 */
export function cn(...inputs) {
  return twMerge(clsx(inputs));
}
