import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";

export type CartItem = {
  productId: string;
  name: string;
  price: number;
  size: string;
  image: string;
  quantity: number;
};

type CartCtx = {
  items: CartItem[];
  count: number;
  subtotal: number;
  add: (item: Omit<CartItem, "quantity"> & { quantity?: number }) => void;
  remove: (productId: string, size: string) => void;
  updateQty: (productId: string, size: string, qty: number) => void;
  clear: () => void;
  isOpen: boolean;
  open: () => void;
  close: () => void;
  setOpen: (o: boolean) => void;
};

const Ctx = createContext<CartCtx | null>(null);
const KEY = "monolith-cart-v1";

function keyOf(pid: string, size: string) { return `${pid}::${size}`; }

export function CartProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<CartItem[]>([]);
  const [isOpen, setOpen] = useState(false);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(KEY);
      if (raw) setItems(JSON.parse(raw));
    } catch { /* ignore */ }
    setHydrated(true);
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    try { localStorage.setItem(KEY, JSON.stringify(items)); } catch { /* ignore */ }
  }, [items, hydrated]);

  const add = useCallback<CartCtx["add"]>((item) => {
    setItems((prev) => {
      const qty = item.quantity ?? 1;
      const idx = prev.findIndex((p) => keyOf(p.productId, p.size) === keyOf(item.productId, item.size));
      if (idx >= 0) {
        const next = prev.slice();
        next[idx] = { ...next[idx], quantity: next[idx].quantity + qty };
        return next;
      }
      return [...prev, { ...item, quantity: qty }];
    });
  }, []);

  const remove = useCallback<CartCtx["remove"]>((pid, size) => {
    setItems((prev) => prev.filter((p) => keyOf(p.productId, p.size) !== keyOf(pid, size)));
  }, []);

  const updateQty = useCallback<CartCtx["updateQty"]>((pid, size, qty) => {
    setItems((prev) => prev.flatMap((p) => {
      if (keyOf(p.productId, p.size) !== keyOf(pid, size)) return [p];
      if (qty <= 0) return [];
      return [{ ...p, quantity: qty }];
    }));
  }, []);

  const clear = useCallback(() => setItems([]), []);

  const value = useMemo<CartCtx>(() => ({
    items,
    count: items.reduce((s, i) => s + i.quantity, 0),
    subtotal: items.reduce((s, i) => s + i.quantity * i.price, 0),
    add, remove, updateQty, clear,
    isOpen, open: () => setOpen(true), close: () => setOpen(false), setOpen,
  }), [items, isOpen, add, remove, updateQty, clear]);

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useCart() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useCart must be used within CartProvider");
  return ctx;
}

export function formatPrice(n: number) {
  return `$${n.toFixed(0)}`;
}
