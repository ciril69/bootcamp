import { Link } from "@tanstack/react-router";
import { Minus, Plus, ShoppingBag, Trash2, X } from "lucide-react";
import { useCart, formatPrice } from "@/lib/cart";
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";

export function CartSheet() {
  const { items, isOpen, setOpen, updateQty, remove, subtotal, close } = useCart();

  return (
    <Sheet open={isOpen} onOpenChange={setOpen}>
      <SheetContent side="right" className="w-full sm:max-w-md bg-background border-border p-0 flex flex-col">
        <SheetHeader className="p-6 border-b border-border">
          <SheetTitle className="font-display tracking-[0.25em] text-left">
            Your Bag · {items.reduce((s, i) => s + i.quantity, 0)}
          </SheetTitle>
        </SheetHeader>

        {items.length === 0 ? (
          <div className="flex-1 grid place-items-center p-8 text-center">
            <div>
              <div className="mx-auto size-20 rounded-full grid place-items-center border border-border">
                <ShoppingBag className="size-8 text-muted-foreground" />
              </div>
              <div className="mt-6 font-display text-2xl tracking-[0.15em]">Bag is empty</div>
              <p className="mt-2 text-sm text-muted-foreground">Curated pieces are waiting.</p>
              <Link
                to="/shop"
                onClick={close}
                className="btn-shine mt-6 inline-flex items-center justify-center px-6 py-3 text-xs tracking-[0.25em] uppercase bg-metal-bright text-background hover:bg-foreground transition-colors"
              >
                Shop the drop
              </Link>
            </div>
          </div>
        ) : (
          <>
            <ul className="flex-1 overflow-y-auto divide-y divide-border">
              {items.map((it) => (
                <li key={`${it.productId}-${it.size}`} className="p-4 flex gap-4 animate-fade-in">
                  <div className="w-20 h-24 shrink-0 overflow-hidden bg-surface-2">
                    <img src={it.image} alt={it.name} className="size-full object-cover" loading="lazy" />
                  </div>
                  <div className="flex-1 min-w-0 flex flex-col justify-between">
                    <div className="flex justify-between gap-2">
                      <div className="min-w-0">
                        <div className="truncate text-sm font-medium">{it.name}</div>
                        <div className="text-xs text-muted-foreground mt-0.5">Size {it.size}</div>
                      </div>
                      <button
                        onClick={() => remove(it.productId, it.size)}
                        className="text-muted-foreground hover:text-destructive transition-colors p-1"
                        aria-label={`Remove ${it.name}`}
                      >
                        <Trash2 className="size-4" />
                      </button>
                    </div>
                    <div className="flex items-center justify-between mt-2">
                      <div className="inline-flex items-center border border-border">
                        <button
                          className="size-8 grid place-items-center hover:bg-surface-2 transition-colors"
                          onClick={() => updateQty(it.productId, it.size, it.quantity - 1)}
                          aria-label="Decrease quantity"
                        >
                          <Minus className="size-3.5" />
                        </button>
                        <span className="w-8 text-center text-sm">{it.quantity}</span>
                        <button
                          className="size-8 grid place-items-center hover:bg-surface-2 transition-colors"
                          onClick={() => updateQty(it.productId, it.size, it.quantity + 1)}
                          aria-label="Increase quantity"
                        >
                          <Plus className="size-3.5" />
                        </button>
                      </div>
                      <div className="text-sm text-metal-bright">{formatPrice(it.price * it.quantity)}</div>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
            <div className="border-t border-border p-6 space-y-4">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground tracking-[0.2em] uppercase text-xs">Subtotal</span>
                <span className="font-display text-xl">{formatPrice(subtotal)}</span>
              </div>
              <p className="text-xs text-muted-foreground">Shipping & taxes calculated at checkout.</p>
              <Link
                to="/checkout"
                onClick={close}
                className="btn-shine block w-full text-center px-6 py-4 text-xs tracking-[0.3em] uppercase bg-metal-bright text-background hover:bg-foreground transition-colors"
              >
                Checkout
              </Link>
              <button
                onClick={close}
                className="w-full text-center py-2 text-xs tracking-[0.25em] uppercase text-muted-foreground hover:text-foreground transition-colors"
              >
                Continue shopping
              </button>
            </div>
          </>
        )}
      </SheetContent>
    </Sheet>
  );
}
