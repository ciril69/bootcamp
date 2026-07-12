import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { z } from "zod";
import { Check } from "lucide-react";
import { useCart, formatPrice } from "@/lib/cart";

export const Route = createFileRoute("/checkout")({
  head: () => ({ meta: [{ title: "Checkout — MONOLITH" }, { name: "robots", content: "noindex" }] }),
  component: Checkout,
});

const schema = z.object({
  name: z.string().trim().min(2, "Enter your full name").max(80),
  email: z.string().trim().email("Enter a valid email").max(200),
  phone: z.string().trim().min(6, "Enter a valid phone").max(30),
  address: z.string().trim().min(6, "Enter your address").max(200),
  city: z.string().trim().min(2, "City required").max(80),
  postal: z.string().trim().min(3, "Postal / ZIP required").max(20),
  country: z.string().trim().min(2, "Country required").max(80),
});

type Form = z.infer<typeof schema>;
type Errors = Partial<Record<keyof Form, string>>;

function Checkout() {
  const { items, subtotal, clear } = useCart();
  const navigate = useNavigate();
  const [values, setValues] = useState<Form>({
    name: "", email: "", phone: "", address: "", city: "", postal: "", country: "",
  });
  const [errors, setErrors] = useState<Errors>({});
  const [confirmed, setConfirmed] = useState<{ id: string; name: string; email: string; total: number } | null>(null);

  const onChange = (k: keyof Form) => (e: React.ChangeEvent<HTMLInputElement>) => {
    setValues((v) => ({ ...v, [k]: e.target.value }));
  };

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    const parsed = schema.safeParse(values);
    if (!parsed.success) {
      const errs: Errors = {};
      for (const iss of parsed.error.issues) {
        const key = iss.path[0] as keyof Form;
        if (!errs[key]) errs[key] = iss.message;
      }
      setErrors(errs);
      return;
    }
    setErrors({});
    const orderId = `MNL-${Date.now().toString(36).toUpperCase()}`;
    const info = { id: orderId, name: parsed.data.name, email: parsed.data.email, total: subtotal };
    clear();
    setConfirmed(info);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  if (confirmed) {
    return (
      <section className="container-x mx-auto py-24 md:py-32 text-center animate-fade-up">
        <div className="mx-auto size-20 rounded-full grid place-items-center border border-metal-bright text-metal-bright">
          <Check className="size-9" />
        </div>
        <div className="mt-6 text-xs tracking-[0.4em] uppercase text-muted-foreground">Order Confirmed</div>
        <h1 className="mt-3 font-display text-5xl md:text-7xl tracking-[0.02em] text-metal-gradient">Thank you, {confirmed.name.split(" ")[0]}.</h1>
        <div className="mt-6 max-w-md mx-auto text-sm md:text-base text-secondary-foreground/80">
          <p>Your order <span className="text-metal-bright font-mono">{confirmed.id}</span> has been received.</p>
          <p className="mt-2">A confirmation would have been sent to <span className="text-foreground">{confirmed.email}</span>.</p>
          <p className="mt-2">Total: <span className="text-foreground">{formatPrice(confirmed.total)}</span></p>
        </div>
        <div className="mt-10 mx-auto max-w-md p-6 border border-border bg-surface text-left">
          <div className="text-xs tracking-[0.3em] uppercase text-metal-bright">Demonstration Notice</div>
          <p className="mt-2 text-sm text-muted-foreground">
            This is a demonstration website. No real order has been placed and no payment has been processed.
          </p>
        </div>
        <div className="mt-10 flex justify-center gap-3">
          <Link to="/shop" className="btn-shine px-6 py-3 text-xs tracking-[0.3em] uppercase bg-metal-bright text-background hover:bg-foreground transition-colors">Keep shopping</Link>
          <Link to="/" className="px-6 py-3 text-xs tracking-[0.3em] uppercase border border-border hover:border-metal-bright">Home</Link>
        </div>
      </section>
    );
  }

  if (items.length === 0) {
    return (
      <section className="container-x mx-auto py-24 md:py-32 text-center">
        <h1 className="font-display text-5xl md:text-7xl tracking-[0.02em]">Nothing to check out</h1>
        <p className="mt-4 text-muted-foreground">Add a piece from the collection first.</p>
        <Link to="/shop" className="btn-shine mt-8 inline-flex px-6 py-3 text-xs tracking-[0.3em] uppercase bg-metal-bright text-background hover:bg-foreground">Shop the drop</Link>
      </section>
    );
  }

  const Field = ({ k, label, type = "text", autoComplete }: { k: keyof Form; label: string; type?: string; autoComplete?: string }) => (
    <label className="block">
      <span className="text-[10px] tracking-[0.3em] uppercase text-muted-foreground">{label}</span>
      <input
        type={type}
        value={values[k]}
        onChange={onChange(k)}
        autoComplete={autoComplete}
        aria-invalid={errors[k] ? "true" : "false"}
        className={`mt-2 w-full px-4 py-3 bg-surface border outline-none text-sm transition-colors ${errors[k] ? "border-destructive" : "border-border focus:border-metal-bright"}`}
      />
      {errors[k] && <span className="mt-1 block text-xs text-destructive">{errors[k]}</span>}
    </label>
  );

  return (
    <section className="container-x mx-auto py-12 md:py-20">
      <div className="text-xs tracking-[0.4em] uppercase text-muted-foreground">Checkout</div>
      <h1 className="mt-3 font-display text-5xl md:text-7xl tracking-[0.02em]">Finalize</h1>

      <div className="mt-12 grid lg:grid-cols-[1fr_380px] gap-10 lg:gap-16">
        <form onSubmit={submit} noValidate className="space-y-8">
          <div className="p-6 md:p-8 border border-border bg-surface">
            <div className="font-display text-2xl tracking-[0.15em] mb-6">Contact</div>
            <div className="grid md:grid-cols-2 gap-4">
              <Field k="name" label="Full name" autoComplete="name" />
              <Field k="email" label="Email" type="email" autoComplete="email" />
              <Field k="phone" label="Phone" type="tel" autoComplete="tel" />
            </div>
          </div>
          <div className="p-6 md:p-8 border border-border bg-surface">
            <div className="font-display text-2xl tracking-[0.15em] mb-6">Delivery</div>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="md:col-span-2"><Field k="address" label="Street address" autoComplete="street-address" /></div>
              <Field k="city" label="City" autoComplete="address-level2" />
              <Field k="postal" label="Postal / ZIP" autoComplete="postal-code" />
              <div className="md:col-span-2"><Field k="country" label="Country" autoComplete="country-name" /></div>
            </div>
          </div>
          <div className="p-4 border border-border bg-surface-2 text-xs text-muted-foreground">
            This is a demonstration checkout — no payment step is included and no real order will be placed.
          </div>
          <button type="submit" className="btn-shine w-full px-6 py-4 text-xs tracking-[0.3em] uppercase bg-metal-bright text-background hover:bg-foreground transition-colors">
            Place demo order · {formatPrice(subtotal)}
          </button>
        </form>

        <aside className="lg:sticky lg:top-24 self-start border border-border p-6 md:p-8 bg-surface">
          <div className="text-xs tracking-[0.3em] uppercase text-muted-foreground mb-6">Order</div>
          <ul className="space-y-4">
            {items.map((it) => (
              <li key={`${it.productId}-${it.size}`} className="flex gap-3">
                <div className="w-14 h-16 shrink-0 bg-surface-2 overflow-hidden">
                  <img src={it.image} alt={it.name} className="size-full object-cover" loading="lazy" />
                </div>
                <div className="flex-1 min-w-0 text-sm">
                  <div className="truncate">{it.name}</div>
                  <div className="text-xs text-muted-foreground mt-0.5">{it.size} · Qty {it.quantity}</div>
                </div>
                <div className="text-sm text-metal-bright">{formatPrice(it.price * it.quantity)}</div>
              </li>
            ))}
          </ul>
          <div className="mt-6 pt-4 border-t border-border flex justify-between">
            <span className="text-xs tracking-[0.3em] uppercase text-muted-foreground pt-2">Total</span>
            <span className="font-display text-3xl">{formatPrice(subtotal)}</span>
          </div>
        </aside>
      </div>
    </section>
  );
}
