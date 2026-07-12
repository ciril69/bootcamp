import { Link, useRouterState } from "@tanstack/react-router";
import { Menu, ShoppingBag, X } from "lucide-react";
import { useEffect, useState } from "react";
import { useCart } from "@/lib/cart";
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";

const LINKS = [
  { to: "/", label: "Home" },
  { to: "/shop", label: "Shop" },
  { to: "/about", label: "About" },
  { to: "/contact", label: "Contact" },
] as const;

export function Nav() {
  const { count, open } = useCart();
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const pathname = useRouterState({ select: (s) => s.location.pathname });

  useEffect(() => { setMobileOpen(false); }, [pathname]);

  useEffect(() => {
    const on = () => setScrolled(window.scrollY > 12);
    on();
    window.addEventListener("scroll", on, { passive: true });
    return () => window.removeEventListener("scroll", on);
  }, []);

  return (
    <>
      <header
        className={[
          "fixed top-0 inset-x-0 z-40 transition-all duration-500",
          scrolled
            ? "bg-background/85 backdrop-blur-xl border-b border-border/60"
            : "bg-transparent border-b border-transparent",
        ].join(" ")}
      >
        <div className="container-x mx-auto grid grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)] items-center h-16 md:h-20">
          <div className="hidden md:flex items-center gap-8 text-xs tracking-[0.2em] uppercase">
            {LINKS.map((l) => (
              <Link
                key={l.to}
                to={l.to}
                activeOptions={{ exact: l.to === "/" }}
                className="text-foreground/70 hover:text-foreground transition-colors data-[status=active]:text-foreground data-[status=active]:[text-shadow:0_0_20px_rgba(217,217,217,0.4)]"
              >
                {l.label}
              </Link>
            ))}
          </div>
          <button
            className="md:hidden justify-self-start text-foreground p-2 -ml-2"
            onClick={() => setMobileOpen(true)}
            aria-label="Open menu"
          >
            <Menu className="size-6" />
          </button>

          <Link to="/" className="justify-self-center font-display text-2xl md:text-3xl tracking-[0.25em] text-metal-gradient">
            MONOLITH
          </Link>

          <div className="justify-self-end flex items-center gap-2 md:gap-4">
            <button
              onClick={open}
              className="relative p-2 -mr-2 group"
              aria-label={`Open cart, ${count} item${count === 1 ? "" : "s"}`}
            >
              <ShoppingBag className="size-5 md:size-[22px] group-hover:text-metal-bright transition-colors" />
              {count > 0 && (
                <span className="absolute -top-0.5 -right-0.5 min-w-[18px] h-[18px] px-1 rounded-full bg-metal-bright text-background text-[10px] font-semibold grid place-items-center animate-fade-in">
                  {count}
                </span>
              )}
            </button>
          </div>
        </div>
      </header>

      <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
        <SheetContent side="left" className="w-full sm:max-w-sm bg-background border-border p-0">
          <SheetHeader className="p-6 border-b border-border">
            <SheetTitle className="font-display text-2xl tracking-[0.25em] text-left text-metal-gradient">MONOLITH</SheetTitle>
          </SheetHeader>
          <nav className="flex flex-col p-2">
            {LINKS.map((l, i) => (
              <Link
                key={l.to}
                to={l.to}
                onClick={() => setMobileOpen(false)}
                className="px-4 py-5 border-b border-border/60 text-2xl font-display tracking-[0.2em] text-foreground/80 hover:text-foreground hover:bg-surface transition-colors animate-fade-up"
                style={{ animationDelay: `${i * 60}ms` }}
              >
                {l.label}
              </Link>
            ))}
          </nav>
        </SheetContent>
      </Sheet>

      {/* Spacer so content isn't hidden under fixed nav */}
      <div className="h-16 md:h-20" aria-hidden />
    </>
  );
}
