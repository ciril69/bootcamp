import { createFileRoute } from "@tanstack/react-router";
import { LIFESTYLE_1, LIFESTYLE_2, HERO_IMAGE } from "@/lib/products";
import { Reveal } from "@/components/site/Reveal";

export const Route = createFileRoute("/about")({
  head: () => ({
    meta: [
      { title: "About — MONOLITH" },
      { name: "description", content: "MONOLITH is a men's streetwear label built on oversized silhouettes, heavyweight fabrics, and a dark editorial house code." },
      { property: "og:title", content: "About — MONOLITH" },
      { property: "og:description", content: "The story, mission, and philosophy behind MONOLITH." },
    ],
  }),
  component: About,
});

function About() {
  return (
    <>
      <section className="relative min-h-[60vh] -mt-16 md:-mt-20 overflow-hidden grid place-items-end">
        <img src={LIFESTYLE_2} alt="" className="absolute inset-0 size-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-b from-background/50 via-background/40 to-background" />
        <div className="relative container-x mx-auto pb-16 pt-32">
          <div className="text-xs tracking-[0.4em] uppercase text-metal animate-fade-up">The House</div>
          <h1 className="mt-4 font-display text-6xl md:text-9xl tracking-[0.02em] text-metal-gradient animate-fade-up" style={{ animationDelay: "150ms" }}>
            About MONOLITH
          </h1>
        </div>
      </section>

      <section className="container-x mx-auto py-20 md:py-32 grid lg:grid-cols-2 gap-16">
        <Reveal>
          <div>
            <div className="text-xs tracking-[0.4em] uppercase text-muted-foreground">Story</div>
            <h2 className="mt-3 font-display text-4xl md:text-6xl tracking-[0.02em]">Cut from the city</h2>
            <p className="mt-6 text-base md:text-lg text-secondary-foreground/80 leading-relaxed">
              MONOLITH began in a shared studio behind a concrete garage — one pattern-cutter, one printer, and a stack of heavyweight fabric.
              Everything we make is a reaction to what streetwear had become: too loud, too disposable, too soft in the hand.
              We build the opposite.
            </p>
          </div>
        </Reveal>
        <Reveal delay={100}>
          <div className="aspect-[4/5] overflow-hidden">
            <img src={LIFESTYLE_1} alt="" className="size-full object-cover" loading="lazy" />
          </div>
        </Reveal>
      </section>

      <section className="border-y border-border bg-surface">
        <div className="container-x mx-auto py-20 md:py-32 grid md:grid-cols-3 gap-12">
          {[
            { label: "Mission", body: "Design pieces that outlast the season. Heavyweight cotton, considered patterns, and a colour palette that stays timeless." },
            { label: "Vision",  body: "A men's label defined by silhouette rather than logo — quiet on the outside, precisely engineered on the inside." },
            { label: "Philosophy", body: "Streetwear is a uniform, not a costume. Build it dense, wear it hard, keep it dark." },
          ].map((p, i) => (
            <Reveal key={p.label} delay={i * 120}>
              <div>
                <div className="text-xs tracking-[0.4em] uppercase text-metal-bright">0{i + 1}</div>
                <div className="mt-3 font-display text-3xl md:text-4xl tracking-[0.05em]">{p.label}</div>
                <p className="mt-4 text-sm md:text-base text-secondary-foreground/80 leading-relaxed">{p.body}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      <section className="container-x mx-auto py-20 md:py-32">
        <Reveal>
          <div className="grid md:grid-cols-2 gap-2 md:gap-4">
            <div className="aspect-[4/5] overflow-hidden"><img src={HERO_IMAGE} alt="" className="size-full object-cover" loading="lazy" /></div>
            <div className="aspect-[4/5] overflow-hidden mt-8 md:mt-16"><img src={LIFESTYLE_2} alt="" className="size-full object-cover" loading="lazy" /></div>
          </div>
        </Reveal>
      </section>
    </>
  );
}
