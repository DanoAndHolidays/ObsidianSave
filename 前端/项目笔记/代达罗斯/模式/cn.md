# cn
将classname中存在的表达式转换为字符串，而不是使用：
``` 
`px-2 ${ ClassName }` 
```
的形式去拼接

```ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export const cn = function(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
};

```

```ts
import type { HTMLAttributes } from "react";
import { cn } from "@/lib/utils";

export const Card = function({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("rounded-[10px] border border-[#ececef] dark:border-border bg-card text-card-foreground", className)} {...props} />;
};

export const CardHeader = function({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("flex items-center justify-between px-[17px] py-4 border-b border-[#f4f4f5] dark:border-border", className)} {...props} />;
};

export const CardContent = function({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("px-[17px] py-4", className)} {...props} />;
};

```