import { cva, type VariantProps } from "class-variance-authority";
import { Link } from "@tanstack/react-router";
import type { ComponentProps, ReactNode } from "react";
import { cn } from "@/lib/utils";

const btn = cva(
  "btn-shine inline-flex items-center justify-center gap-2 whitespace-nowrap text-xs tracking-[0.25em] uppercase transition-colors disabled:opacity-40 disabled:pointer-events-none",
  {
    variants: {
      variant: {
        solid: "bg-metal-bright text-background hover:bg-foreground",
        outline: "border border-border text-foreground hover:border-metal-bright hover:text-metal-bright bg-transparent",
        ghost: "text-foreground/80 hover:text-metal-bright",
      },
      size: {
        md: "px-6 py-3",
        lg: "px-8 py-4",
        sm: "px-4 py-2",
      },
    },
    defaultVariants: { variant: "solid", size: "md" },
  },
);

type BtnProps = { children: ReactNode; className?: string } & VariantProps<typeof btn>;

export function Btn({
  children, className, variant, size, ...rest
}: BtnProps & ComponentProps<"button">) {
  return (
    <button className={cn(btn({ variant, size }), className)} {...rest}>
      {children}
    </button>
  );
}

export function BtnLink({
  children, className, variant, size, ...rest
}: BtnProps & ComponentProps<typeof Link>) {
  return (
    <Link className={cn(btn({ variant, size }), className)} {...rest}>
      {children}
    </Link>
  );
}
