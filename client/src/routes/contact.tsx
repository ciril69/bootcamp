import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { z } from "zod";
import { Mail, MapPin, Phone, Clock } from "lucide-react";
import { toast } from "sonner";
import { Reveal } from "@/components/site/Reveal";

export const Route = createFileRoute("/contact")({
  head: () => ({
    meta: [
      { title: "Contact — MONOLITH" },
      { name: "description", content: "Reach the MONOLITH studio for custom apparel, wholesale, and press inquiries." },
      { property: "og:title", content: "Contact — MONOLITH" },
      { property: "og:description", content: "Get in touch — the studio handles custom prints, embroidery, and bulk orders directly." },
    ],
  }),
  component: Contact,
});

const schema = z.object({
  name: z.string().trim().min(2, "Enter your name").max(80),
  email: z.string().trim().email("Enter a valid email"),
  phone: z.string().trim().max(30).optional().or(z.literal("")),
  message: z.string().trim().min(10, "Tell us a bit more (10+ characters)").max(1000),
});

type Form = z.infer<typeof schema>;

function Contact() {
  const [values, setValues] = useState<Form>({ name: "", email: "", phone: "", message: "" });
  const [errors, setErrors] = useState<Partial<Record<keyof Form, string>>>({});

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    const parsed = schema.safeParse(values);
    if (!parsed.success) {
      const errs: Partial<Record<keyof Form, string>> = {};
      for (const iss of parsed.error.issues) {
        const k = iss.path[0] as keyof Form;
        if (!errs[k]) errs[k] = iss.message;
      }
      setErrors(errs);
      return;
    }
    setErrors({});
    toast.success("Message received", { description: "Demo submission — the studio would respond within one business day." });
    setValues({ name: "", email: "", phone: "", message: "" });
  };

  return (
    <section className="container-x mx-auto py-16 md:py-24">
      <div className="text-xs tracking-[0.4em] uppercase text-muted-foreground">The Studio</div>
      <h1 className="mt-3 font-display text-6xl md:text-8xl tracking-[0.02em] text-metal-gradient">Contact</h1>

      <div className="mt-14 grid lg:grid-cols-[1fr_1.2fr] gap-12 lg:gap-20">
        <Reveal>
          <div className="space-y-8">
            <div>
              <div className="text-xs tracking-[0.3em] uppercase text-muted-foreground mb-3">The house</div>
              <p className="text-base leading-relaxed text-secondary-foreground/80 max-w-md">
                For custom prints, embroidery, wholesale, or press — reach us directly. One inbox, one line, one studio.
              </p>
            </div>
            <ul className="space-y-6">
              {[
                { icon: Mail, label: "Email", value: "hello@monolith.studio", href: "mailto:hello@monolith.studio" },
                { icon: Phone, label: "Phone", value: "+1 (415) 555-0134", href: "tel:+14155550134" },
                { icon: MapPin, label: "Studio", value: "224 Alameda Ave · Los Angeles, CA" },
                { icon: Clock, label: "Hours", value: "Mon – Sat · 10:00 – 19:00" },
              ].map((r) => (
                <li key={r.label} className="flex gap-4">
                  <div className="size-10 shrink-0 grid place-items-center border border-border">
                    <r.icon className="size-4 text-metal-bright" />
                  </div>
                  <div>
                    <div className="text-[10px] tracking-[0.3em] uppercase text-muted-foreground">{r.label}</div>
                    {r.href
                      ? <a href={r.href} className="text-sm hover:text-metal-bright transition-colors">{r.value}</a>
                      : <div className="text-sm">{r.value}</div>}
                  </div>
                </li>
              ))}
            </ul>
            <div className="aspect-[16/9] border border-border bg-surface-2 grid place-items-center text-xs tracking-[0.3em] uppercase text-muted-foreground">
              Map · Los Angeles
            </div>
          </div>
        </Reveal>

        <Reveal delay={100}>
          <form onSubmit={submit} noValidate className="p-6 md:p-10 border border-border bg-surface space-y-5">
            <div className="font-display text-3xl tracking-[0.15em]">Send a message</div>
            {(
              [
                { k: "name" as const, label: "Name", type: "text", auto: "name" },
                { k: "email" as const, label: "Email", type: "email", auto: "email" },
                { k: "phone" as const, label: "Phone (optional)", type: "tel", auto: "tel" },
              ]
            ).map((f) => (
              <label key={f.k} className="block">
                <span className="text-[10px] tracking-[0.3em] uppercase text-muted-foreground">{f.label}</span>
                <input
                  type={f.type}
                  autoComplete={f.auto}
                  value={values[f.k] as string}
                  onChange={(e) => setValues((v) => ({ ...v, [f.k]: e.target.value }))}
                  aria-invalid={errors[f.k] ? "true" : "false"}
                  className={`mt-2 w-full px-4 py-3 bg-background border outline-none text-sm transition-colors ${errors[f.k] ? "border-destructive" : "border-border focus:border-metal-bright"}`}
                />
                {errors[f.k] && <span className="mt-1 block text-xs text-destructive">{errors[f.k]}</span>}
              </label>
            ))}
            <label className="block">
              <span className="text-[10px] tracking-[0.3em] uppercase text-muted-foreground">Message</span>
              <textarea
                rows={6}
                value={values.message}
                onChange={(e) => setValues((v) => ({ ...v, message: e.target.value }))}
                aria-invalid={errors.message ? "true" : "false"}
                className={`mt-2 w-full px-4 py-3 bg-background border outline-none text-sm transition-colors resize-none ${errors.message ? "border-destructive" : "border-border focus:border-metal-bright"}`}
              />
              {errors.message && <span className="mt-1 block text-xs text-destructive">{errors.message}</span>}
            </label>
            <button type="submit" className="btn-shine w-full px-6 py-4 text-xs tracking-[0.3em] uppercase bg-metal-bright text-background hover:bg-foreground transition-colors">
              Send message
            </button>
          </form>
        </Reveal>
      </div>
    </section>
  );
}
