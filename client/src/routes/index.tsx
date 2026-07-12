import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowRight, ChevronDown, Mail, Package, Phone, Scissors, Sparkles } from "lucide-react";
import { CATEGORIES, HERO_IMAGE, LIFESTYLE_2, PRODUCTS } from "@/lib/products";
import { ProductCard } from "@/components/site/ProductCard";
import { Reveal } from "@/components/site/Reveal";
import { BtnLink } from "@/components/site/Btn";
import { useState } from "react";
import { toast } from "sonner";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "MONOLITH — Premium Men's Streetwear" },
      { name: "description", content: "Oversized silhouettes. Heavyweight fabrics. A luxury dark streetwear label for men aged 12–30." },
    ],
  }),
  component: Home,
});

function Home() {
  return (
    <>
      <Hero />
      <FeaturedCategories />
      <NewArrivals />
      <WhyChoose />
      <CustomApparel />
      <Newsletter />
    </>
  );
}

function Hero() {
  return (
    <section className="relative min-h-[92vh] md:min-h-screen -mt-16 md:-mt-20 overflow-hidden">
      <img
        src={HERO_IMAGE}
        alt="Model in oversized black hoodie"
        width={1200}
        height={1500}
        className="absolute inset-0 size-full object-cover object-center scale-105 animate-fade-in"
      />
      <div className="absolute inset-0 bg-gradient-to-b from-background/60 via-background/30 to-background" />
      <div className="absolute inset-0 bg-gradient-to-r from-background/70 via-transparent to-background/40" />

      <div className="relative container-x mx-auto flex flex-col justify-end min-h-[92vh] md:min-h-screen pb-24 md:pb-32 pt-32">
        <div className="max-w-2xl">
          <div className="text-xs tracking-[0.4em] uppercase text-metal animate-fade-up" style={{ animationDelay: "100ms" }}>
            Chapter 04 — Ash & Chrome
          </div>
          <h1 className="mt-6 font-display text-[14vw] md:text-[8rem] leading-[0.85] tracking-[0.02em] text-metal-gradient animate-fade-up" style={{ animationDelay: "200ms" }}>
            Built for<br />after dark.
          </h1>
          <p className="mt-6 max-w-md text-base md:text-lg text-secondary-foreground/80 animate-fade-up" style={{ animationDelay: "350ms" }}>
            Oversized silhouettes, heavyweight fabrics, and a colour palette engineered for the city at 3AM. This is streetwear as a second skin.
          </p>
          <div className="mt-10 flex flex-wrap gap-3 animate-fade-up" style={{ animationDelay: "500ms" }}>
            <BtnLink to="/shop" size="lg" variant="solid">
              Shop Collection <ArrowRight className="size-4" />
            </BtnLink>
            <BtnLink to="/contact" size="lg" variant="outline">
              Explore Customization
            </BtnLink>
          </div>
        </div>
      </div>

      <div className="absolute bottom-6 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 text-muted-foreground animate-scroll-hint">
        <span className="text-[10px] tracking-[0.4em] uppercase">Scroll</span>
        <ChevronDown className="size-4" />
      </div>
    </section>
  );
}

function FeaturedCategories() {
  return (
    <section className="container-x mx-auto py-24 md:py-32">
      <Reveal>
        <div className="flex items-end justify-between gap-6 mb-12">
          <div>
            <div className="text-xs tracking-[0.4em] uppercase text-muted-foreground">01 / Silhouettes</div>
            <h2 className="mt-3 font-display text-5xl md:text-7xl tracking-[0.02em]">The Categories</h2>
          </div>
          <Link to="/shop" className="hidden md:inline-flex items-center gap-2 text-xs tracking-[0.25em] uppercase text-metal hover:text-metal-bright transition-colors">
            View all <ArrowRight className="size-4" />
          </Link>
        </div>
      </Reveal>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4">
        {CATEGORIES.map((c, i) => (
          <Reveal key={c.id} delay={i * 100}>
            <Link
              to="/shop"
              search={{ c: c.id }}
              className="group relative aspect-[3/4] block overflow-hidden bg-surface-2"
            >
              <img
                src={c.image}
                alt={c.label}
                loading="lazy"
                className="size-full object-cover transition-transform duration-[900ms] ease-out group-hover:scale-110"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-background via-background/30 to-transparent" />
              <div className="absolute inset-0 flex flex-col justify-end p-4 md:p-6">
                <div className="text-[10px] tracking-[0.3em] uppercase text-metal">0{i + 1}</div>
                <div className="font-display text-xl md:text-3xl tracking-[0.05em] mt-2 transition-transform duration-500 group-hover:-translate-y-1">
                  {c.label}
                </div>
                <div className="text-xs text-muted-foreground mt-1 md:mt-2 opacity-0 md:opacity-100 group-hover:opacity-100 transition-opacity duration-500">
                  {c.blurb}
                </div>
                <div className="mt-3 inline-flex items-center gap-2 text-[10px] tracking-[0.3em] uppercase text-metal-bright opacity-0 -translate-y-1 group-hover:opacity-100 group-hover:translate-y-0 transition-all duration-500">
                  Shop <ArrowRight className="size-3" />
                </div>
              </div>
            </Link>
          </Reveal>
        ))}
      </div>
    </section>
  );
}

function NewArrivals() {
  const items = PRODUCTS.filter((p) => p.featured).slice(0, 8);
  return (
    <section className="container-x mx-auto py-24 md:py-32">
      <Reveal>
        <div className="flex items-end justify-between gap-6 mb-12">
          <div>
            <div className="text-xs tracking-[0.4em] uppercase text-muted-foreground">02 / Just Landed</div>
            <h2 className="mt-3 font-display text-5xl md:text-7xl tracking-[0.02em]">New Arrivals</h2>
          </div>
          <Link to="/shop" className="hidden md:inline-flex items-center gap-2 text-xs tracking-[0.25em] uppercase text-metal hover:text-metal-bright transition-colors">
            Shop the drop <ArrowRight className="size-4" />
          </Link>
        </div>
      </Reveal>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-x-4 gap-y-10 md:gap-x-6 md:gap-y-14">
        {items.map((p, i) => (
          <Reveal key={p.id} delay={i * 60}>
            <ProductCard product={p} />
          </Reveal>
        ))}
      </div>
    </section>
  );
}

function WhyChoose() {
  const pillars = [
    { icon: Sparkles, title: "Premium Fabrics", body: "Heavyweight cotton, brushed fleece, and Japanese-milled shells sourced for hand feel." },
    { icon: Package,  title: "Oversized Comfort", body: "Every silhouette is pattern-drafted for a squared, boxed cut that falls naturally." },
    { icon: Scissors, title: "Custom Apparel", body: "Prints, embroidery, and bulk orders handled in-studio. Direct line to a real tailor." },
    { icon: ArrowRight, title: "Modern Streetwear", body: "A house style built for the city — dark, metallic, quietly confident." },
  ];
  return (
    <section className="border-y border-border bg-surface">
      <div className="container-x mx-auto py-24 md:py-32">
        <Reveal>
          <div className="max-w-2xl">
            <div className="text-xs tracking-[0.4em] uppercase text-muted-foreground">03 / House Code</div>
            <h2 className="mt-3 font-display text-5xl md:text-7xl tracking-[0.02em]">Why MONOLITH</h2>
          </div>
        </Reveal>
        <div className="mt-16 grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {pillars.map((p, i) => (
            <Reveal key={p.title} delay={i * 100}>
              <div className="group p-8 bg-background border border-border h-full transition-colors hover:border-metal">
                <p.icon className="size-8 text-metal group-hover:text-metal-bright transition-colors" />
                <div className="mt-6 font-display text-2xl tracking-[0.1em]">{p.title}</div>
                <p className="mt-3 text-sm text-muted-foreground leading-relaxed">{p.body}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}

function CustomApparel() {
  return (
    <section className="container-x mx-auto py-24 md:py-32">
      <div className="grid lg:grid-cols-2 gap-10 lg:gap-16 items-center">
        <Reveal>
          <div className="relative aspect-[4/5] overflow-hidden">
            <img src={LIFESTYLE_2} alt="Custom apparel" className="size-full object-cover" loading="lazy" />
          </div>
        </Reveal>
        <Reveal delay={150}>
          <div>
            <div className="text-xs tracking-[0.4em] uppercase text-muted-foreground">04 / Made to Order</div>
            <h2 className="mt-3 font-display text-5xl md:text-7xl tracking-[0.02em] text-metal-gradient">Custom Apparel</h2>
            <p className="mt-6 text-base md:text-lg text-secondary-foreground/80 max-w-lg">
              Prints, embroidery, and bulk orders — every piece can be tailored to a name, a team, or a season. Reach out directly and the studio handles the rest.
            </p>
            <ul className="mt-8 space-y-3 text-sm">
              {["Custom prints on any silhouette", "Chest & sleeve embroidery", "Bulk orders for teams & brands"].map((t) => (
                <li key={t} className="flex items-center gap-3">
                  <span className="size-1.5 rounded-full bg-metal-bright" />
                  <span className="text-secondary-foreground/90">{t}</span>
                </li>
              ))}
            </ul>
            <div className="mt-10 flex flex-wrap gap-3">
              <a href="mailto:custom@monolith.studio" className="btn-shine inline-flex items-center gap-2 px-6 py-3 text-xs tracking-[0.25em] uppercase bg-metal-bright text-background hover:bg-foreground transition-colors">
                <Mail className="size-4" /> Email the studio
              </a>
              <a href="tel:+14155550134" className="inline-flex items-center gap-2 px-6 py-3 text-xs tracking-[0.25em] uppercase border border-border hover:border-metal-bright hover:text-metal-bright transition-colors">
                <Phone className="size-4" /> Call
              </a>
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  );
}

function Newsletter() {
  const [email, setEmail] = useState("");
  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    const ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
    if (!ok) {
      toast.error("Enter a valid email");
      return;
    }
    toast.success("You're on the list", { description: "Demo signup — no email will be sent." });
    setEmail("");
  };
  return (
    <section className="container-x mx-auto py-24 md:py-32">
      <Reveal>
        <div className="border border-border p-8 md:p-16 bg-surface text-center max-w-3xl mx-auto">
          <div className="text-xs tracking-[0.4em] uppercase text-muted-foreground">Field Notes</div>
          <h2 className="mt-4 font-display text-4xl md:text-6xl tracking-[0.02em]">Join the dispatch</h2>
          <p className="mt-4 text-sm md:text-base text-muted-foreground max-w-md mx-auto">
            Early drops, studio access, and one email a month. That's it.
          </p>
          <form onSubmit={submit} className="mt-8 flex flex-col sm:flex-row gap-2 max-w-md mx-auto">
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              aria-label="Email address"
              className="flex-1 px-4 py-3 bg-background border border-border focus:border-metal-bright outline-none text-sm placeholder:text-muted-foreground"
            />
            <button
              type="submit"
              className="btn-shine px-6 py-3 text-xs tracking-[0.3em] uppercase bg-metal-bright text-background hover:bg-foreground transition-colors"
            >
              Subscribe
            </button>
          </form>
        </div>
      </Reveal>
    </section>
  );
}
