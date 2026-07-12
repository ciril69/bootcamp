import { Link } from "@tanstack/react-router";
import { Plus } from "lucide-react";
import { useCart, formatPrice } from "@/lib/cart";
import type { Product } from "@/lib/products";
import { toast } from "sonner";

export function ProductCard({ product }: { product: Product }) {
  const { add, open } = useCart();

  const quickAdd = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    add({
      productId: product.id,
      name: product.name,
      price: product.price,
      size: product.sizes[Math.floor(product.sizes.length / 2)],
      image: product.images[0],
    });
    toast.success(`${product.name} added`, { description: "Choose size in cart if needed." });
    open();
  };

  return (
    <Link
      to="/product/$id"
      params={{ id: product.id }}
      className="group block hover-lift"
    >
      <div className="relative aspect-[4/5] overflow-hidden bg-surface-2">
        <img
          src={product.images[0]}
          alt={product.name}
          loading="lazy"
          width={1000}
          height={1200}
          className="size-full object-cover transition-transform duration-[900ms] ease-out group-hover:scale-[1.06]"
        />
        <img
          src={product.images[1] ?? product.images[0]}
          alt=""
          aria-hidden="true"
          loading="lazy"
          width={1000}
          height={1200}
          className="absolute inset-0 size-full object-cover opacity-0 transition-opacity duration-700 group-hover:opacity-100"
        />
        {product.featured && (
          <span className="absolute top-3 left-3 text-[10px] tracking-[0.25em] uppercase bg-background/70 backdrop-blur px-2 py-1 text-metal-bright">
            Featured
          </span>
        )}
        <button
          onClick={quickAdd}
          aria-label={`Quick add ${product.name}`}
          className="absolute bottom-3 right-3 size-11 grid place-items-center rounded-full bg-background/70 backdrop-blur border border-border text-foreground opacity-0 translate-y-2 group-hover:opacity-100 group-hover:translate-y-0 transition-all duration-500 hover:bg-metal-bright hover:text-background"
        >
          <Plus className="size-5" />
        </button>
      </div>
      <div className="pt-4 flex items-start justify-between gap-3">
        <div className="min-w-0">
          <div className="text-[10px] tracking-[0.25em] uppercase text-muted-foreground">{product.categoryLabel}</div>
          <div className="mt-1 truncate text-sm font-medium">{product.name}</div>
        </div>
        <div className="text-sm text-metal-bright shrink-0">{formatPrice(product.price)}</div>
      </div>
    </Link>
  );
}
