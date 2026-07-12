import { Link } from "@tanstack/react-router";
import { Instagram, Twitter, Youtube } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t border-border mt-32 bg-surface">
      <div className="container-x mx-auto py-20 grid gap-12 md:grid-cols-4">
        <div>
          <div className="font-display text-2xl tracking-[0.25em] text-metal-gradient">MONOLITH</div>
          <p className="mt-4 text-sm text-muted-foreground max-w-xs leading-relaxed">
            Premium men's streetwear built for the after-hours.
          </p>
          <div className="mt-6 flex gap-4">
            <a href="#" aria-label="Instagram" className="text-muted-foreground hover:text-metal-bright transition-colors"><Instagram className="size-5" /></a>
            <a href="#" aria-label="Twitter" className="text-muted-foreground hover:text-metal-bright transition-colors"><Twitter className="size-5" /></a>
            <a href="#" aria-label="YouTube" className="text-muted-foreground hover:text-metal-bright transition-colors"><Youtube className="size-5" /></a>
          </div>
        </div>
        <div>
          <div className="text-xs tracking-[0.25em] uppercase text-muted-foreground mb-4">Shop</div>
          <ul className="space-y-2 text-sm">
            <li><Link to="/shop" search={{ c: "hoodies" }} className="hover:text-metal-bright transition-colors">Hoodies</Link></li>
            <li><Link to="/shop" search={{ c: "tshirts" }} className="hover:text-metal-bright transition-colors">T-Shirts</Link></li>
            <li><Link to="/shop" search={{ c: "tanks" }} className="hover:text-metal-bright transition-colors">Tanks</Link></li>
            <li><Link to="/shop" search={{ c: "jackets" }} className="hover:text-metal-bright transition-colors">Jackets</Link></li>
          </ul>
        </div>
        <div>
          <div className="text-xs tracking-[0.25em] uppercase text-muted-foreground mb-4">House</div>
          <ul className="space-y-2 text-sm">
            <li><Link to="/about" className="hover:text-metal-bright transition-colors">About</Link></li>
            <li><Link to="/contact" className="hover:text-metal-bright transition-colors">Contact</Link></li>
            <li><Link to="/contact" className="hover:text-metal-bright transition-colors">Custom Orders</Link></li>
          </ul>
        </div>
        <div>
          <div className="text-xs tracking-[0.25em] uppercase text-muted-foreground mb-4">Studio</div>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>hello@monolith.studio</li>
            <li>+1 (415) 555-0134</li>
            <li>Mon–Sat · 10 – 19</li>
          </ul>
        </div>
      </div>
      <div className="border-t border-border">
        <div className="container-x mx-auto py-6 flex flex-col md:flex-row justify-between items-center gap-2 text-xs text-muted-foreground">
          <div>© {new Date().getFullYear()} MONOLITH Studio. All rights reserved.</div>
          <div className="tracking-[0.2em] uppercase">Demonstration Project — No Real Orders</div>
        </div>
      </div>
    </footer>
  );
}
