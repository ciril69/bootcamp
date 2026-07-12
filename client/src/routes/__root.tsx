import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  Outlet,
  Link,
  createRootRouteWithContext,
  useRouter,
  HeadContent,
  Scripts,
} from "@tanstack/react-router";
import { useEffect, type ReactNode } from "react";

import appCss from "../styles.css?url";
import { reportLovableError } from "../lib/lovable-error-reporting";
import { CartProvider } from "@/lib/cart";
import { Nav } from "@/components/site/Nav";
import { Footer } from "@/components/site/Footer";
import { CartSheet } from "@/components/site/CartSheet";
import { Toaster } from "@/components/ui/sonner";

function NotFoundComponent() {
  return (
    <div className="min-h-[70vh] grid place-items-center px-6 text-center">
      <div>
        <div className="font-display text-[24vw] md:text-[12rem] leading-none text-metal-gradient">404</div>
        <div className="mt-4 tracking-[0.3em] text-xs uppercase text-muted-foreground">Off the grid</div>
        <p className="mt-4 max-w-md mx-auto text-sm text-muted-foreground">
          This page has slipped into the fog. Head back to the collection.
        </p>
        <Link to="/" className="btn-shine mt-8 inline-flex items-center px-8 py-4 text-xs tracking-[0.3em] uppercase bg-metal-bright text-background hover:bg-foreground transition-colors">
          Return home
        </Link>
      </div>
    </div>
  );
}

function ErrorComponent({ error, reset }: { error: Error; reset: () => void }) {
  console.error(error);
  const router = useRouter();
  useEffect(() => {
    reportLovableError(error, { boundary: "tanstack_root_error_component" });
  }, [error]);

  return (
    <div className="min-h-[70vh] grid place-items-center px-6 text-center">
      <div className="max-w-md">
        <h1 className="font-display text-4xl tracking-[0.15em]">Something broke</h1>
        <p className="mt-3 text-sm text-muted-foreground">
          The stitching gave out on our side. Try again or head home.
        </p>
        <div className="mt-8 flex justify-center gap-3">
          <button
            onClick={() => { router.invalidate(); reset(); }}
            className="btn-shine px-6 py-3 text-xs tracking-[0.25em] uppercase bg-metal-bright text-background hover:bg-foreground"
          >
            Try again
          </button>
          <a href="/" className="px-6 py-3 text-xs tracking-[0.25em] uppercase border border-border hover:border-metal-bright">
            Home
          </a>
        </div>
      </div>
    </div>
  );
}

export const Route = createRootRouteWithContext<{ queryClient: QueryClient }>()({
  head: () => ({
    meta: [
      { charSet: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { title: "MONOLITH — Premium Men's Streetwear" },
      { name: "description", content: "Luxury dark streetwear for men. Oversized cuts, heavyweight fabrics, custom apparel on request." },
      { name: "author", content: "MONOLITH Studio" },
      { property: "og:title", content: "MONOLITH — Premium Men's Streetwear" },
      { property: "og:description", content: "Luxury dark streetwear for men. Oversized cuts, heavyweight fabrics, custom apparel on request." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
    links: [
      { rel: "stylesheet", href: appCss },
      { rel: "icon", href: "/favicon.ico", type: "image/x-icon" },
      { rel: "preconnect", href: "https://fonts.googleapis.com" },
      { rel: "preconnect", href: "https://fonts.gstatic.com", crossOrigin: "anonymous" },
      { rel: "stylesheet", href: "https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&display=swap" },
    ],
  }),
  shellComponent: RootShell,
  component: RootComponent,
  notFoundComponent: NotFoundComponent,
  errorComponent: ErrorComponent,
});

function RootShell({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className="dark">
      <head>
        <HeadContent />
      </head>
      <body>
        {children}
        <Scripts />
      </body>
    </html>
  );
}

function RootComponent() {
  const { queryClient } = Route.useRouteContext();

  return (
    <QueryClientProvider client={queryClient}>
      <CartProvider>
        <div className="min-h-screen flex flex-col">
          <Nav />
          <main className="flex-1">
            <Outlet />
          </main>
          <Footer />
          <CartSheet />
          <Toaster />
        </div>
      </CartProvider>
    </QueryClientProvider>
  );
}
