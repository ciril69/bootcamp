import { createFileRoute, Link, notFound } from "@tanstack/react-router";
import { useState } from "react";
import { Mail, Minus, Phone, Plus, ShoppingBag } from "lucide-react";
import { getProduct, related } from "@/lib/products";
import { useCart, formatPrice } from "@/lib/cart";
import { ProductCard } from "@/components/site/ProductCard";
import { Reveal } from "@/components/site/Reveal";
import { toast } from "sonner";

export const Route = createFileRoute("/product/$id")({
  loader: ({ params }) => {
    const product = getProduct(params.id);
    if (!product) throw notFound();
    return { product };
  },
  head: ({ loaderData }) => ({
    meta: loaderData ? [
      { title: `${loaderData.product.name} — MONOLITH` },
      { name: "description", content: loaderData.product.description },
      { property: "og:title", content: `${loaderData.product.name} — MONOLITH` },
      { property: "og:description", content: loaderData.product.description },
      { property: "og:image", content: loaderData.product.images[0] },
    ] : [{ title: "Not found" }, { name: "robots", content: "noindex" }],
  }),
  component: ProductDetail,
  notFoundComponent: NotFound,
});

function NotFound() {
  return (
    <div className="container-x mx-auto py-32 text-center">
      <div className="font-display text-5xl tracking-[0.15em]">Piece not found</div>
      <Link to="/shop" className="mt-6 inline-block text-sm tracking-[0.25em] uppercase text-metal-bright hover:text-foreground">Back to shop</Link>
    </div>
  );
}

function ProductDetail() {
  const { product } = Route.useLoaderData();
  const [size, setSize] = useState(product.sizes[2]);
  const [qty, setQty] = useState(1);
  const [activeImg, setActiveImg] = useState(0);
  const { add, open } = useCart();

  const rel = related(product.id, product.category);

  const addToCart = () => {
    if (!size) { toast.error("Choose a size"); return; }
    add({
      productId: product.id,
      name: product.name,
      price: product.price,
      size,
      image: product.images[0],
      quantity: qty,
    });
    toast.success(`${product.name} added`);
    open();
  };

  return (
    <>
      <section className="container-x mx-auto py-8 md:py-16">
        <div className="text-xs tracking-[0.25em] uppercase text-muted-foreground mb-6">
          <Link to="/" className="hover:text-foreground">Home</Link>
          <span className="mx-2 text-border">/</span>
          <Link to="/shop" className="hover:text-foreground">Shop</Link>
          <span className="mx-2 text-border">/</span>
          <span className="text-foreground">{product.categoryLabel}</span>
        </div>

        <div className="grid lg:grid-cols-[1.2fr_1fr] gap-8 lg:gap-16">
          {/* Gallery */}
          <div className="flex flex-col-reverse md:flex-row gap-3">
            <div className="flex md:flex-col gap-2 md:gap-3 overflow-x-auto md:overflow-visible">
              {product.images.map((img: string, i: number) => (
                <button
                  key={i}
                  onClick={() => setActiveImg(i)}
                  className={`shrink-0 size-16 md:size-20 overflow-hidden border transition-colors ${activeImg === i ? "border-metal-bright" : "border-border hover:border-muted-foreground"}`}
                  aria-label={`View image ${i + 1}`}
                >
                  <img src={img} alt="" className="size-full object-cover" loading="lazy" />
                </button>
              ))}
            </div>
            <div className="flex-1 relative aspect-[4/5] overflow-hidden bg-surface-2 group">
              <img
                key={activeImg}
                src={product.images[activeImg]}
                alt={product.name}
                className="size-full object-cover transition-transform duration-[900ms] group-hover:scale-[1.04] animate-fade-in"
                width={1000}
                height={1200}
              />
            </div>
          </div>

          {/* Info */}
          <div className="lg:sticky lg:top-24 self-start">
            <div className="text-xs tracking-[0.3em] uppercase text-muted-foreground">{product.categoryLabel}</div>
            <h1 className="mt-3 font-display text-4xl md:text-6xl tracking-[0.02em]">{product.name}</h1>
            <div className="mt-4 text-2xl text-metal-bright">{formatPrice(product.price)}</div>
            <p className="mt-6 text-sm md:text-base text-secondary-foreground/80 leading-relaxed">
              {product.description}
            </p>

            <div className="mt-8">
              <div className="text-xs tracking-[0.3em] uppercase text-muted-foreground mb-3">Size</div>
              <div className="flex flex-wrap gap-2">
                {product.sizes.map((s: string) => (
                  <button
                    key={s}
                    onClick={() => setSize(s)}
                    className={`min-w-[52px] h-11 px-3 text-sm border transition-colors ${size === s ? "border-metal-bright text-metal-bright" : "border-border hover:border-muted-foreground"}`}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>

            <div className="mt-8 flex items-center gap-4">
              <div className="inline-flex items-center border border-border">
                <button className="size-11 grid place-items-center hover:bg-surface-2" onClick={() => setQty((q) => Math.max(1, q - 1))} aria-label="Decrease quantity">
                  <Minus className="size-4" />
                </button>
                <span className="w-10 text-center">{qty}</span>
                <button className="size-11 grid place-items-center hover:bg-surface-2" onClick={() => setQty((q) => Math.min(10, q + 1))} aria-label="Increase quantity">
                  <Plus className="size-4" />
                </button>
              </div>
              <button
                onClick={addToCart}
                className="btn-shine flex-1 inline-flex items-center justify-center gap-2 px-6 py-4 text-xs tracking-[0.3em] uppercase bg-metal-bright text-background hover:bg-foreground transition-colors"
              >
                <ShoppingBag className="size-4" /> Add to Cart
              </button>
            </div>

            {product.customizable && (
              <div className="mt-10 p-6 border border-border bg-surface">
                <div className="text-xs tracking-[0.3em] uppercase text-metal-bright">Custom Apparel</div>
                <p className="mt-3 text-sm text-secondary-foreground/80 leading-relaxed">
                  This piece can be printed, embroidered, or tailored for a team. Reach out and the studio handles the rest.
                </p>
                <div className="mt-4 flex flex-wrap gap-2">
                  <a href={`mailto:custom@monolith.studio?subject=Custom%20request%20—%20${encodeURIComponent(product.name)}`} className="inline-flex items-center gap-2 px-4 py-2 text-[10px] tracking-[0.25em] uppercase border border-border hover:border-metal-bright hover:text-metal-bright transition-colors">
                    <Mail className="size-3.5" /> Email
                  </a>
                  <a href="tel:+14155550134" className="inline-flex items-center gap-2 px-4 py-2 text-[10px] tracking-[0.25em] uppercase border border-border hover:border-metal-bright hover:text-metal-bright transition-colors">
                    <Phone className="size-3.5" /> Call
                  </a>
                </div>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Mobile sticky add-to-cart */}
      <div className="fixed bottom-0 inset-x-0 z-30 md:hidden bg-background/90 backdrop-blur border-t border-border p-3 flex items-center gap-3">
        <div>
          <div className="text-[10px] uppercase tracking-[0.25em] text-muted-foreground">{size ? `Size ${size}` : "Pick size"}</div>
          <div className="text-sm text-metal-bright">{formatPrice(product.price * qty)}</div>
        </div>
        <button
          onClick={addToCart}
          className="flex-1 btn-shine text-xs tracking-[0.25em] uppercase bg-metal-bright text-background py-3"
        >
          Add to Cart
        </button>
      </div>

      {rel.length > 0 && (
        <section className="container-x mx-auto py-20 md:py-32 pb-32 md:pb-32">
          <Reveal>
            <div className="text-xs tracking-[0.4em] uppercase text-muted-foreground">You might also like</div>
            <h2 className="mt-3 font-display text-4xl md:text-6xl tracking-[0.02em]">Related</h2>
          </Reveal>
          <div className="mt-12 grid grid-cols-2 lg:grid-cols-4 gap-x-4 gap-y-10 md:gap-x-6">
            {rel.map((p) => <ProductCard key={p.id} product={p} />)}
          </div>
        </section>
      )}
    </>
  );
}
