import { createFileRoute, Link } from "@tanstack/react-router";
import { Minus, Plus, ShoppingBag, Trash2 } from "lucide-react";
import { useCart, formatPrice } from "@/lib/cart";

export const Route = createFileRoute("/cart")({
  head: () => ({ meta: [{ title: "Your Bag — MONOLITH" }, { name: "robots", content: "noindex" }] }),
  component: CartPage,
});

function CartPage() {
  const { items, updateQty, remove, subtotal } = useCart();

  return (
    <section className="container-x mx-auto py-12 md:py-20">
      <div className="text-xs tracking-[0.4em] uppercase text-muted-foreground">Checkout Step 01</div>
      <h1 className="mt-3 font-display text-5xl md:text-7xl tracking-[0.02em]">Your Bag</h1>

      {items.length === 0 ? (
        <div className="mt-16 max-w-md mx-auto text-center border border-border p-12 bg-surface">
          <div className="mx-auto size-20 rounded-full grid place-items-center border border-border">
            <ShoppingBag className="size-8 text-muted-foreground" />
          </div>
          <div className="mt-6 font-display text-3xl tracking-[0.15em]">Empty</div>
          <p className="mt-2 text-sm text-muted-foreground">Nothing here yet. The collection is ready when you are.</p>
          <Link to="/shop" className="btn-shine mt-6 inline-flex px-6 py-3 text-xs tracking-[0.3em] uppercase bg-metal-bright text-background hover:bg-foreground transition-colors">
            Shop the drop
          </Link>
        </div>
      ) : (
        <div className="mt-10 grid lg:grid-cols-[1fr_360px] gap-10">
          <ul className="divide-y divide-border border-y border-border">
            {items.map((it) => (
              <li key={`${it.productId}-${it.size}`} className="py-6 flex gap-4 md:gap-6 animate-fade-in">
                <Link to="/product/$id" params={{ id: it.productId }} className="w-24 h-32 md:w-32 md:h-40 shrink-0 overflow-hidden bg-surface-2">
                  <img src={it.image} alt={it.name} className="size-full object-cover" loading="lazy" />
                </Link>
                <div className="flex-1 min-w-0 flex flex-col justify-between">
                  <div className="flex justify-between gap-4">
                    <div>
                      <Link to="/product/$id" params={{ id: it.productId }} className="font-medium hover:text-metal-bright transition-colors">
                        {it.name}
                      </Link>
                      <div className="text-xs text-muted-foreground mt-1">Size {it.size}</div>
                    </div>
                    <button onClick={() => remove(it.productId, it.size)} className="text-muted-foreground hover:text-destructive p-1" aria-label={`Remove ${it.name}`}>
                      <Trash2 className="size-4" />
                    </button>
                  </div>
                  <div className="flex items-end justify-between mt-4">
                    <div className="inline-flex items-center border border-border">
                      <button className="size-9 grid place-items-center hover:bg-surface-2" onClick={() => updateQty(it.productId, it.size, it.quantity - 1)} aria-label="Decrease">
                        <Minus className="size-3.5" />
                      </button>
                      <span className="w-9 text-center text-sm">{it.quantity}</span>
                      <button className="size-9 grid place-items-center hover:bg-surface-2" onClick={() => updateQty(it.productId, it.size, it.quantity + 1)} aria-label="Increase">
                        <Plus className="size-3.5" />
                      </button>
                    </div>
                    <div className="text-metal-bright">{formatPrice(it.price * it.quantity)}</div>
                  </div>
                </div>
              </li>
            ))}
          </ul>
          <aside className="lg:sticky lg:top-24 self-start border border-border p-6 md:p-8 bg-surface">
            <div className="text-xs tracking-[0.3em] uppercase text-muted-foreground">Summary</div>
            <div className="mt-4 space-y-2 text-sm">
              <div className="flex justify-between"><span className="text-muted-foreground">Subtotal</span><span>{formatPrice(subtotal)}</span></div>
              <div className="flex justify-between"><span className="text-muted-foreground">Shipping</span><span>Calc at checkout</span></div>
            </div>
            <div className="mt-6 pt-4 border-t border-border flex justify-between">
              <span className="text-xs tracking-[0.3em] uppercase text-muted-foreground pt-2">Total</span>
              <span className="font-display text-3xl">{formatPrice(subtotal)}</span>
            </div>
            <Link to="/checkout" className="btn-shine mt-8 flex justify-center px-6 py-4 text-xs tracking-[0.3em] uppercase bg-metal-bright text-background hover:bg-foreground transition-colors">
              Checkout
            </Link>
            <Link to="/shop" className="mt-3 flex justify-center py-2 text-xs tracking-[0.25em] uppercase text-muted-foreground hover:text-foreground">
              Continue shopping
            </Link>
          </aside>
        </div>
      )}
    </section>
  );
}
