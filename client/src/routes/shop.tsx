import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { Search, SlidersHorizontal, X } from "lucide-react";
import { z } from "zod";
import { PRODUCTS, CATEGORIES, type Category } from "@/lib/products";
import { ProductCard } from "@/components/site/ProductCard";
import { Reveal } from "@/components/site/Reveal";

const searchSchema = z.object({
  c: z.enum(["tshirts", "hoodies", "tanks", "jackets"]).optional().catch(undefined),
  q: z.string().optional().catch(undefined),
});

export const Route = createFileRoute("/shop")({
  validateSearch: (s) => searchSchema.parse(s),
  head: () => ({
    meta: [
      { title: "Shop — MONOLITH" },
      { name: "description", content: "Browse the current MONOLITH collection. Oversized tees, hoodies, tank tops, and jackets." },
    ],
  }),
  component: Shop,
});

type Sort = "featured" | "price-asc" | "price-desc" | "name";

function Shop() {
  const { c, q } = Route.useSearch();
  const navigate = Route.useNavigate();
  const [query, setQuery] = useState(q ?? "");
  const [price, setPrice] = useState<number>(400);
  const [sort, setSort] = useState<Sort>("featured");
  const [mobileFiltersOpen, setMobileFiltersOpen] = useState(false);

  const filtered = useMemo(() => {
    const term = query.trim().toLowerCase();
    const items = PRODUCTS.filter((p) => {
      if (c && p.category !== c) return false;
      if (p.price > price) return false;
      if (term && !(`${p.name} ${p.description} ${p.categoryLabel}`.toLowerCase().includes(term))) return false;
      return true;
    });
    const sorted = items.slice();
    if (sort === "price-asc") sorted.sort((a, b) => a.price - b.price);
    else if (sort === "price-desc") sorted.sort((a, b) => b.price - a.price);
    else if (sort === "name") sorted.sort((a, b) => a.name.localeCompare(b.name));
    else sorted.sort((a, b) => Number(b.featured) - Number(a.featured));
    return sorted;
  }, [c, query, price, sort]);

  const setCategory = (cat: Category | undefined) => {
    navigate({ search: (prev: { c?: Category; q?: string }) => ({ ...prev, c: cat }) });
  };

  const Filters = (
    <div className="space-y-8">
      <div>
        <div className="text-xs tracking-[0.3em] uppercase text-muted-foreground mb-3">Category</div>
        <div className="flex flex-col gap-1">
          <button
            onClick={() => setCategory(undefined)}
            className={`text-left py-2 text-sm transition-colors ${!c ? "text-metal-bright" : "text-foreground/70 hover:text-foreground"}`}
          >
            All
          </button>
          {CATEGORIES.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setCategory(cat.id)}
              className={`text-left py-2 text-sm transition-colors ${c === cat.id ? "text-metal-bright" : "text-foreground/70 hover:text-foreground"}`}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </div>
      <div>
        <div className="text-xs tracking-[0.3em] uppercase text-muted-foreground mb-3">Max price · ${price}</div>
        <input
          type="range" min={40} max={400} step={10}
          value={price} onChange={(e) => setPrice(Number(e.target.value))}
          className="w-full accent-[color:var(--metal-bright)]"
          aria-label="Maximum price"
        />
      </div>
    </div>
  );

  return (
    <section className="container-x mx-auto py-12 md:py-20">
      <Reveal>
        <div className="mb-10 md:mb-16">
          <div className="text-xs tracking-[0.4em] uppercase text-muted-foreground">The Collection</div>
          <h1 className="mt-3 font-display text-5xl md:text-8xl tracking-[0.02em] text-metal-gradient">Shop</h1>
        </div>
      </Reveal>

      <div className="flex flex-col md:flex-row gap-3 md:items-center md:justify-between mb-8">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 size-4 text-muted-foreground" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search the drop…"
            className="w-full pl-10 pr-3 py-3 bg-surface border border-border focus:border-metal-bright outline-none text-sm placeholder:text-muted-foreground"
            aria-label="Search products"
          />
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setMobileFiltersOpen(true)}
            className="md:hidden inline-flex items-center gap-2 px-4 py-3 border border-border text-xs tracking-[0.25em] uppercase"
          >
            <SlidersHorizontal className="size-4" /> Filters
          </button>
          <select
            value={sort}
            onChange={(e) => setSort(e.target.value as Sort)}
            className="px-4 py-3 bg-surface border border-border text-xs tracking-[0.25em] uppercase outline-none focus:border-metal-bright"
            aria-label="Sort products"
          >
            <option value="featured">Featured</option>
            <option value="price-asc">Price: Low</option>
            <option value="price-desc">Price: High</option>
            <option value="name">Name A–Z</option>
          </select>
        </div>
      </div>

      <div className="grid md:grid-cols-[220px_1fr] gap-10 md:gap-14">
        <aside className="hidden md:block sticky top-24 self-start">
          {Filters}
        </aside>

        <div>
          <div className="mb-6 text-xs tracking-[0.25em] uppercase text-muted-foreground">
            {filtered.length} piece{filtered.length === 1 ? "" : "s"}
          </div>
          {filtered.length === 0 ? (
            <div className="border border-border p-16 text-center bg-surface">
              <div className="font-display text-3xl tracking-[0.15em]">Nothing found</div>
              <p className="mt-2 text-sm text-muted-foreground">Try widening your filters.</p>
            </div>
          ) : (
            <div className="grid grid-cols-2 lg:grid-cols-3 gap-x-4 gap-y-10 md:gap-x-6 md:gap-y-14 animate-fade-in">
              {filtered.map((p) => (
                <ProductCard key={p.id} product={p} />
              ))}
            </div>
          )}
        </div>
      </div>

      {mobileFiltersOpen && (
        <div className="fixed inset-0 z-50 md:hidden">
          <div className="absolute inset-0 bg-background/80 backdrop-blur" onClick={() => setMobileFiltersOpen(false)} />
          <div className="absolute inset-y-0 left-0 w-[85%] max-w-sm bg-background border-r border-border p-6 animate-fade-in overflow-y-auto">
            <div className="flex justify-between items-center mb-8">
              <div className="font-display text-2xl tracking-[0.15em]">Filters</div>
              <button onClick={() => setMobileFiltersOpen(false)} aria-label="Close filters">
                <X className="size-5" />
              </button>
            </div>
            {Filters}
          </div>
        </div>
      )}
    </section>
  );
}
