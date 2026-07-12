import tshirt from "@/assets/cat-tshirt.jpg";
import hoodie from "@/assets/cat-hoodie.jpg";
import tank from "@/assets/cat-tank.jpg";
import jacket from "@/assets/cat-jacket.jpg";
import life1 from "@/assets/lifestyle-1.jpg";
import life2 from "@/assets/lifestyle-2.jpg";

export type Category = "tshirts" | "hoodies" | "tanks" | "jackets";

export const CATEGORIES: { id: Category; label: string; blurb: string; image: string }[] = [
  { id: "tshirts", label: "Oversized T-Shirts", blurb: "Heavyweight cotton. Drop shoulder cut.", image: tshirt },
  { id: "hoodies", label: "Oversized Hoodies", blurb: "500 GSM fleece. Boxed fit.", image: hoodie },
  { id: "tanks",   label: "Tank Tops",         blurb: "Ribbed cotton. Muscle silhouette.", image: tank },
  { id: "jackets", label: "Jackets",           blurb: "Structured outerwear. Signature hardware.", image: jacket },
];

export type Product = {
  id: string;
  name: string;
  description: string;
  category: Category;
  categoryLabel: string;
  price: number;
  sizes: string[];
  images: string[];
  featured: boolean;
  customizable: boolean;
};

const IMG_POOL: Record<Category, string[]> = {
  tshirts: [tshirt, life2, life1, hoodie],
  hoodies: [hoodie, life1, life2, jacket],
  tanks:   [tank, life2, life1, tshirt],
  jackets: [jacket, life1, life2, hoodie],
};

const SIZES = ["XS", "S", "M", "L", "XL", "XXL"];

function make(
  id: string, name: string, category: Category, price: number,
  description: string, featured = false, customizable = true,
): Product {
  const cat = CATEGORIES.find((c) => c.id === category)!;
  return {
    id, name, description, category, categoryLabel: cat.label, price,
    sizes: SIZES.slice(1, 6),
    images: IMG_POOL[category].slice(0, 4),
    featured, customizable,
  };
}

export const PRODUCTS: Product[] = [
  make("ob-01", "Onyx Boxy Tee", "tshirts", 68, "Heavyweight 260 GSM cotton with a squared drop-shoulder cut. Enzyme-washed for a lived-in hand feel.", true),
  make("ob-02", "Shadow Panel Tee", "tshirts", 74, "Tonal panel construction with metallic thread pick-stitching along the yoke.", true),
  make("ob-03", "Vantage Crew", "tshirts", 62, "Long-line silhouette with reinforced ribbed collar. Fits one size larger."),
  make("ob-04", "Concrete Wash Tee", "tshirts", 78, "Stone-washed cotton with a raw-cut hem and vintage graphite tone.", true),
  make("ob-05", "Null Pocket Tee", "tshirts", 66, "Minimal chest pocket, French seams, matte-black woven label."),
  make("ob-06", "Static Long Tee", "tshirts", 72, "Extended hem with side vents. Falls just past the hip.", false, false),
  make("ob-07", "Halo Reflective Tee", "tshirts", 84, "Reflective-piping trim. Photographs like a flash of chrome at night.", true),

  make("hd-01", "Cipher Hoodie", "hoodies", 148, "500 GSM brushed-back fleece. Kangaroo pocket, brass tipped drawcords.", true),
  make("hd-02", "Monolith Zip Hoodie", "hoodies", 168, "Full YKK metallic zip. Structured hood with double lining.", true),
  make("hd-03", "Void Pullover", "hoodies", 138, "Cropped boxed pullover. Ribbed cuffs and hem."),
  make("hd-04", "Fog Overhead Hoodie", "hoodies", 154, "Washed heavyweight fleece with tonal embroidery at the wearer's left cuff.", true),
  make("hd-05", "Nightshift Hoodie", "hoodies", 158, "Fleece-lined hood with a sculpted brim. Signature drawcord tips."),
  make("hd-06", "Ash Contrast Hoodie", "hoodies", 162, "Two-tone paneling. Charcoal body, matte-black sleeves."),
  make("hd-07", "Silence Zip Hoodie", "hoodies", 178, "Concealed placket over the primary zipper. Absolutely no branding.", false, false),

  make("tk-01", "Steel Rib Tank", "tanks", 48, "Compact ribbed cotton with a raw arm-hole finish.", true),
  make("tk-02", "Chrome Muscle Tank", "tanks", 52, "Muscle-cut silhouette in silver-grey pigment dye."),
  make("tk-03", "Blackout Tank", "tanks", 44, "Straight-cut essential. Photographs like ink."),
  make("tk-04", "Vent Rib Tank", "tanks", 54, "Extra-deep armhole. Built for layering under open jackets.", true),
  make("tk-05", "Alloy Long Tank", "tanks", 56, "Elongated body with side splits. Meant to peek beneath a hoodie.", false, false),

  make("jk-01", "Onyx Bomber", "jackets", 268, "Boxed bomber silhouette with matte hardware and a fine ribbed hem.", true),
  make("jk-02", "Vault Coach Jacket", "jackets", 224, "Water-repellent shell. Snap placket over a hidden zip.", true),
  make("jk-03", "Chrome Track Jacket", "jackets", 198, "Full-zip track shell in gunmetal jacquard.", false),
  make("jk-04", "Ghost Puffer", "jackets", 324, "Recycled down. Baffled body with a stand collar.", true),
  make("jk-05", "Shadow Overcoat", "jackets", 388, "Wool-blend long coat with metallic snap details.", true, false),
  make("jk-06", "Grit Work Jacket", "jackets", 246, "Utility styling with chest pockets and a boxed hem."),
];

export function getProduct(id: string) {
  return PRODUCTS.find((p) => p.id === id);
}

export function related(id: string, category: Category, n = 4) {
  return PRODUCTS.filter((p) => p.id !== id && p.category === category).slice(0, n);
}

export const HERO_IMAGE = life1;
export const LIFESTYLE_1 = life1;
export const LIFESTYLE_2 = life2;
