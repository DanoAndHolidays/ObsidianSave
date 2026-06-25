# Button
```ts
import { type ButtonHTMLAttributes, forwardRef } from "react";
import { cn } from "@/lib/utils";

const variants = {
  default: "bg-gray-900 text-white hover:bg-gray-800",
  outline: "border border-gray-200 bg-white hover:bg-gray-50",
  ghost: "hover:bg-gray-100",
  destructive: "bg-red-600 text-white hover:bg-red-700",
};

const sizes = {
  sm: "h-8 px-3 text-xs",
  default: "h-9 px-4 text-sm",
  lg: "h-10 px-6 text-base",
};

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: keyof typeof variants;
  size?: keyof typeof sizes;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "default", ...props }, ref) => (
    <button
      ref={ref}
      className={cn(
        "inline-flex items-center justify-center rounded-md font-semibold transition-colors focus:outline-none focus:ring-1 focus:ring-offset-1 disabled:pointer-events-none disabled:opacity-50",
        variants[variant],
        sizes[size],
        className,
      )}
      {...props}
    />
  ),
);
Button.displayName = "Button";

```

cd "g:\Save\Grogramming\CodeForge\daedalus" && git commit -m "feat: add Crate entity — full-stack CRUD with list, detail, and dialog pages" -m "- DB: crates table with migration 0006 (id, name, type, responsibility, metadata, timestamps)" -m "- DAO/Service: crates-dao + crates-service with list/getById/create/update/delete" -m "- API: tRCR crates router (list, getById, create, update, delete) + Refine dataProvider" -m "- UI: CratesPage (table + create/edit dialog), CrateDetailPage, sidebar & nav entries"