-- Seed categories
INSERT INTO categories (id, name, slug, description) VALUES
('c0000000-0000-0000-0000-000000000001', 'Oversized T-Shirts', 'oversized-t-shirts', 'Premium heavy cotton oversized tees with street-inspired drop shoulders and graphics.'),
('c0000000-0000-0000-0000-000000000002', 'Oversized Hoodies', 'oversized-hoodies', 'Thick fleece oversized hoodies featuring metallic embroidery and streetwear fits.'),
('c0000000-0000-0000-0000-000000000003', 'Tank Tops', 'tank-tops', 'Ribbed and mesh streetwear tank tops with deep armholes and raw edge detailing.'),
('c0000000-0000-0000-0000-000000000004', 'Jackets', 'jackets', 'Heavy denim, utility bombers, and cargo windbreakers with metallic grey accents.')
ON CONFLICT (id) DO NOTHING;

-- Seed products
-- Category 1: Oversized T-Shirts (c0000000-0000-0000-0000-000000000001)
INSERT INTO products (id, category_id, name, slug, description, price, stock, featured, customization_available) VALUES
('p1000000-0000-0000-0000-000000000001', 'c0000000-0000-0000-0000-000000000001', 'Heavyweight Graphic Tee', 'heavyweight-graphic-tee', 'A 300GSM heavy cotton t-shirt featuring a custom puff-print gothic graphic on the back. Engineered with a loose boxy fit, dropped shoulders, and a thick ribbed collar.', 29.99, 150, true, true),
('p1000000-0000-0000-0000-000000000002', 'c0000000-0000-0000-0000-000000000001', 'Vintage Washed Oversized Tee', 'vintage-washed-oversized-tee', 'Acid-washed boxy tee with a distressed finish. Feels incredibly soft and worn-in from the first wear. Designed to fade beautifully over time.', 34.99, 85, true, false),
('p1000000-0000-0000-0000-000000000003', 'c0000000-0000-0000-0000-000000000001', 'Cyberpunk Neon Tee', 'cyberpunk-neon-tee', 'A vibrant neon graphic printed on a pitch-black heavy knit tee. Features reflective metallic print highlights for an industrial night-time vibe.', 32.00, 120, false, true),
('p1000000-0000-0000-0000-000000000004', 'c0000000-0000-0000-0000-000000000001', 'Minimalist Embroidered Tee', 'minimalist-embroidered-tee', 'Classy and clean. A heavy-knit t-shirt with a miniature metallic silver brand crest embroidered on the chest. Perfect for layering.', 28.00, 200, false, true),
('p1000000-0000-0000-0000-000000000005', 'c0000000-0000-0000-0000-000000000005', 'Distressed Drop Shoulder Tee', 'distressed-drop-shoulder-tee', 'Featuring raw edge finishes and subtle distressing on the hem and collar. This tee adds instant rugged character to your outfit.', 35.50, 60, false, false),
('p1000000-0000-0000-0000-000000000006', 'c0000000-0000-0000-0000-000000000001', 'Acid Wash Street Tee', 'acid-wash-street-tee', 'Dark charcoal wash with vintage gray undertones. Relaxed silhouette that couples perfectly with baggy cargo trousers.', 31.99, 90, false, true);

-- Category 2: Oversized Hoodies (c0000000-0000-0000-0000-000000000002)
INSERT INTO products (id, category_id, name, slug, description, price, stock, featured, customization_available) VALUES
('p2000000-0000-0000-0000-000000000001', 'c0000000-0000-0000-0000-000000000002', 'Heavyweight Fleece Hoodie', 'heavyweight-fleece-hoodie', 'Crafted from ultra-thick 450GSM organic cotton fleece. Features a double-lined hood, no drawstrings for a clean look, and a kangaroo pouch.', 69.99, 100, true, true),
('p2000000-0000-0000-0000-000000000002', 'c0000000-0000-0000-0000-000000000002', 'Metallic Embroidery Hoodie', 'metallic-embroidery-hoodie', 'An oversized hoodie showcasing a bold branding script embroidered across the chest in metallic silver threads. Elevate your streetwear outerwear.', 79.99, 45, true, true),
('p2000000-0000-0000-0000-000000000003', 'c0000000-0000-0000-0000-000000000002', 'Acid Wash Distressed Hoodie', 'acid-wash-distressed-hoodie', 'Individually dyed for a unique slate-gray finish. Features hand-distressed detailing along the cuffs and waistband for a vintage feel.', 74.99, 50, false, false),
('p2000000-0000-0000-0000-000000000004', 'c0000000-0000-0000-0000-000000000002', 'Cyber Graphic Oversized Hoodie', 'cyber-graphic-oversized-hoodie', 'Features a high-definition cybernetic skeleton print in metallic ink on both sleeves and back. Thick brushed interior for ultimate warmth.', 72.00, 75, false, true),
('p2000000-0000-0000-0000-000000000005', 'c0000000-0000-0000-0000-000000000002', 'Vintage Washed Drop-Shoulder Hoodie', 'vintage-washed-drop-shoulder-hoodie', 'Relaxed silhouette with slouchy dropped shoulders and a short, boxy waist. Perfect classic street look.', 68.50, 80, false, true),
('p2000000-0000-0000-0000-000000000006', 'c0000000-0000-0000-0000-000000000002', 'Minimal Box Logo Hoodie', 'minimal-box-logo-hoodie', 'A clean, tonal box logo embroidered in matte black on a rich charcoal-colored fleece backdrop.', 65.00, 110, false, false);

-- Category 3: Tank Tops (c0000000-0000-0000-0000-000000000003)
INSERT INTO products (id, category_id, name, slug, description, price, stock, featured, customization_available) VALUES
('p3000000-0000-0000-0000-000000000001', 'c0000000-0000-0000-0000-000000000003', 'Oversized Ribbed Tank', 'oversized-ribbed-tank', 'Heavy ribbed-knit tank top cut with a modern relaxed drape. Features high-quality binding along the armholes and neckline.', 24.99, 140, true, true),
('p3000000-0000-0000-0000-000000000002', 'c0000000-0000-0000-0000-000000000003', 'Mesh Athletic Street Tank', 'mesh-athletic-street-tank', 'Breathable double-layer mesh tank designed for hot summer days. Embellished with sporty black-on-black side stripe graphics.', 27.99, 95, false, true),
('p3000000-0000-0000-0000-000000000003', 'c0000000-0000-0000-0000-000000000003', 'Raw Edge Cotton Tank', 'raw-edge-cotton-tank', 'Pure cotton tank top featuring cut-off raw edges that curl naturally over time for an authentic retro feel.', 22.00, 160, false, false),
('p3000000-0000-0000-0000-000000000004', 'c0000000-0000-0000-0000-000000000003', 'Graphic Acid Wash Tank', 'graphic-acid-wash-tank', 'Features a distressed logo graphic on an acid-washed slate gray base. Loose fit for extra breathing room.', 26.50, 70, false, true),
('p3000000-0000-0000-0000-000000000005', 'c0000000-0000-0000-0000-000000000003', 'Drop Armhole Gym Tank', 'drop-armhole-gym-tank', 'Deep cut armholes for ultimate comfort and mobility. Made from lightweight cotton-modal blend.', 25.00, 120, false, true);

-- Category 4: Jackets (c0000000-0000-0000-0000-000000000004)
INSERT INTO products (id, category_id, name, slug, description, price, stock, featured, customization_available) VALUES
('p4000000-0000-0000-0000-000000000001', 'c0000000-0000-0000-0000-000000000004', 'Oversized Denim Streetwear Jacket', 'oversized-denim-streetwear-jacket', 'Thick 14oz rigid cotton denim jacket featuring custom distressed patches, button fastenings, and a relaxed boxy fit.', 99.99, 40, true, true),
('p4000000-0000-0000-0000-000000000004', 'c0000000-0000-0000-0000-000000000004', 'Metallic Bomber Utility Jacket', 'metallic-bomber-utility-jacket', 'Water-resistant nylon shell utility bomber jacket. Equipped with chrome metallic zippers, cargo utility pockets on the arm, and an oversized fill.', 110.00, 30, true, true),
('p4000000-0000-0000-0000-000000000003', 'c0000000-0000-0000-0000-000000000004', 'Cyber Cargo Windbreaker', 'cyber-cargo-windbreaker', 'Ultra-lightweight ripstop fabric windbreaker. Features toggle hoods, adjustable cuffs, and reflective branding scripts.', 89.99, 65, false, true),
('p4000000-0000-0000-0000-000000000004', 'c0000000-0000-0000-0000-000000000004', 'Acid Wash Canvas Work Jacket', 'acid-wash-canvas-work-jacket', 'Durable canvas construction with a heavy acid wash finish. Faux-shearling lining for warmth during transition seasons.', 105.00, 25, false, false),
('p4000000-0000-0000-0000-000000000005', 'c0000000-0000-0000-0000-000000000004', 'Fleece-Lined Street Parka', 'fleece-lined-street-parka', 'Longer cut parka with storm flap closure and thick micro-fleece lining. Metallic buttons and toggle adjusters.', 120.00, 20, false, true)
ON CONFLICT (id) DO NOTHING;

-- Seed product_images
-- Product 1: Heavyweight Graphic Tee
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p1000000-0000-0000-0000-000000000001', 'https://example.supabase.co/storage/v1/object/public/product-images/heavyweight_graphic_tee_1.jpg', 0),
('p1000000-0000-0000-0000-000000000001', 'https://example.supabase.co/storage/v1/object/public/product-images/heavyweight_graphic_tee_2.jpg', 1),
('p1000000-0000-0000-0000-000000000001', 'https://example.supabase.co/storage/v1/object/public/product-images/heavyweight_graphic_tee_3.jpg', 2);

-- Product 2: Vintage Washed Oversized Tee
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p1000000-0000-0000-0000-000000000002', 'https://example.supabase.co/storage/v1/object/public/product-images/vintage_washed_tee_1.jpg', 0),
('p1000000-0000-0000-0000-000000000002', 'https://example.supabase.co/storage/v1/object/public/product-images/vintage_washed_tee_2.jpg', 1),
('p1000000-0000-0000-0000-000000000002', 'https://example.supabase.co/storage/v1/object/public/product-images/vintage_washed_tee_3.jpg', 2);

-- Product 3: Cyberpunk Neon Tee
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p1000000-0000-0000-0000-000000000003', 'https://example.supabase.co/storage/v1/object/public/product-images/cyberpunk_neon_tee_1.jpg', 0),
('p1000000-0000-0000-0000-000000000003', 'https://example.supabase.co/storage/v1/object/public/product-images/cyberpunk_neon_tee_2.jpg', 1),
('p1000000-0000-0000-0000-000000000003', 'https://example.supabase.co/storage/v1/object/public/product-images/cyberpunk_neon_tee_3.jpg', 2);

-- Product 4: Minimalist Embroidered Tee
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p1000000-0000-0000-0000-000000000004', 'https://example.supabase.co/storage/v1/object/public/product-images/minimalist_embroidered_tee_1.jpg', 0),
('p1000000-0000-0000-0000-000000000004', 'https://example.supabase.co/storage/v1/object/public/product-images/minimalist_embroidered_tee_2.jpg', 1);

-- Product 5: Distressed Drop Shoulder Tee
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p1000000-0000-0000-0000-000000000005', 'https://example.supabase.co/storage/v1/object/public/product-images/distressed_drop_tee_1.jpg', 0),
('p1000000-0000-0000-0000-000000000005', 'https://example.supabase.co/storage/v1/object/public/product-images/distressed_drop_tee_2.jpg', 1);

-- Product 6: Acid Wash Street Tee
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p1000000-0000-0000-0000-000000000006', 'https://example.supabase.co/storage/v1/object/public/product-images/acid_wash_street_tee_1.jpg', 0),
('p1000000-0000-0000-0000-000000000006', 'https://example.supabase.co/storage/v1/object/public/product-images/acid_wash_street_tee_2.jpg', 1);

-- Product 7: Heavyweight Fleece Hoodie
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p2000000-0000-0000-0000-000000000001', 'https://example.supabase.co/storage/v1/object/public/product-images/heavyweight_fleece_hoodie_1.jpg', 0),
('p2000000-0000-0000-0000-000000000001', 'https://example.supabase.co/storage/v1/object/public/product-images/heavyweight_fleece_hoodie_2.jpg', 1),
('p2000000-0000-0000-0000-000000000001', 'https://example.supabase.co/storage/v1/object/public/product-images/heavyweight_fleece_hoodie_3.jpg', 2);

-- Product 8: Metallic Embroidery Hoodie
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p2000000-0000-0000-0000-000000000002', 'https://example.supabase.co/storage/v1/object/public/product-images/metallic_embroidery_hoodie_1.jpg', 0),
('p2000000-0000-0000-0000-000000000002', 'https://example.supabase.co/storage/v1/object/public/product-images/metallic_embroidery_hoodie_2.jpg', 1);

-- Product 9: Acid Wash Distressed Hoodie
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p2000000-0000-0000-0000-000000000003', 'https://example.supabase.co/storage/v1/object/public/product-images/acid_wash_hoodie_1.jpg', 0),
('p2000000-0000-0000-0000-000000000003', 'https://example.supabase.co/storage/v1/object/public/product-images/acid_wash_hoodie_2.jpg', 1);

-- Product 10: Cyber Graphic Oversized Hoodie
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p2000000-0000-0000-0000-000000000004', 'https://example.supabase.co/storage/v1/object/public/product-images/cyber_graphic_hoodie_1.jpg', 0),
('p2000000-0000-0000-0000-000000000004', 'https://example.supabase.co/storage/v1/object/public/product-images/cyber_graphic_hoodie_2.jpg', 1);

-- Product 11: Vintage Washed Drop-Shoulder Hoodie
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p2000000-0000-0000-0000-000000000005', 'https://example.supabase.co/storage/v1/object/public/product-images/washed_drop_hoodie_1.jpg', 0),
('p2000000-0000-0000-0000-000000000005', 'https://example.supabase.co/storage/v1/object/public/product-images/washed_drop_hoodie_2.jpg', 1);

-- Product 12: Minimal Box Logo Hoodie
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p2000000-0000-0000-0000-000000000006', 'https://example.supabase.co/storage/v1/object/public/product-images/box_logo_hoodie_1.jpg', 0),
('p2000000-0000-0000-0000-000000000006', 'https://example.supabase.co/storage/v1/object/public/product-images/box_logo_hoodie_2.jpg', 1);

-- Product 13: Oversized Ribbed Tank
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p3000000-0000-0000-0000-000000000001', 'https://example.supabase.co/storage/v1/object/public/product-images/oversized_ribbed_tank_1.jpg', 0),
('p3000000-0000-0000-0000-000000000001', 'https://example.supabase.co/storage/v1/object/public/product-images/oversized_ribbed_tank_2.jpg', 1);

-- Product 14: Mesh Athletic Street Tank
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p3000000-0000-0000-0000-000000000002', 'https://example.supabase.co/storage/v1/object/public/product-images/mesh_athletic_tank_1.jpg', 0),
('p3000000-0000-0000-0000-000000000002', 'https://example.supabase.co/storage/v1/object/public/product-images/mesh_athletic_tank_2.jpg', 1);

-- Product 15: Raw Edge Cotton Tank
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p3000000-0000-0000-0000-000000000003', 'https://example.supabase.co/storage/v1/object/public/product-images/raw_edge_tank_1.jpg', 0),
('p3000000-0000-0000-0000-000000000003', 'https://example.supabase.co/storage/v1/object/public/product-images/raw_edge_tank_2.jpg', 1);

-- Product 16: Graphic Acid Wash Tank
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p3000000-0000-0000-0000-000000000004', 'https://example.supabase.co/storage/v1/object/public/product-images/graphic_acid_tank_1.jpg', 0),
('p3000000-0000-0000-0000-000000000004', 'https://example.supabase.co/storage/v1/object/public/product-images/graphic_acid_tank_2.jpg', 1);

-- Product 17: Drop Armhole Gym Tank
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p3000000-0000-0000-0000-000000000005', 'https://example.supabase.co/storage/v1/object/public/product-images/drop_armhole_tank_1.jpg', 0),
('p3000000-0000-0000-0000-000000000005', 'https://example.supabase.co/storage/v1/object/public/product-images/drop_armhole_tank_2.jpg', 1);

-- Product 18: Oversized Denim Streetwear Jacket
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p4000000-0000-0000-0000-000000000001', 'https://example.supabase.co/storage/v1/object/public/product-images/denim_jacket_1.jpg', 0),
('p4000000-0000-0000-0000-000000000001', 'https://example.supabase.co/storage/v1/object/public/product-images/denim_jacket_2.jpg', 1),
('p4000000-0000-0000-0000-000000000001', 'https://example.supabase.co/storage/v1/object/public/product-images/denim_jacket_3.jpg', 2);

-- Product 19: Metallic Bomber Utility Jacket
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p4000000-0000-0000-0000-000000000004', 'https://example.supabase.co/storage/v1/object/public/product-images/bomber_jacket_1.jpg', 0),
('p4000000-0000-0000-0000-000000000004', 'https://example.supabase.co/storage/v1/object/public/product-images/bomber_jacket_2.jpg', 1),
('p4000000-0000-0000-0000-000000000004', 'https://example.supabase.co/storage/v1/object/public/product-images/bomber_jacket_3.jpg', 2);

-- Product 20: Cyber Cargo Windbreaker
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p4000000-0000-0000-0000-000000000003', 'https://example.supabase.co/storage/v1/object/public/product-images/windbreaker_jacket_1.jpg', 0),
('p4000000-0000-0000-0000-000000000003', 'https://example.supabase.co/storage/v1/object/public/product-images/windbreaker_jacket_2.jpg', 1);

-- Product 21: Acid Wash Canvas Work Jacket
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p4000000-0000-0000-0000-000000000004', 'https://example.supabase.co/storage/v1/object/public/product-images/canvas_jacket_1.jpg', 0),
('p4000000-0000-0000-0000-000000000004', 'https://example.supabase.co/storage/v1/object/public/product-images/canvas_jacket_2.jpg', 1);

-- Product 22: Fleece-Lined Street Parka
INSERT INTO product_images (product_id, image_url, display_order) VALUES
('p4000000-0000-0000-0000-000000000005', 'https://example.supabase.co/storage/v1/object/public/product-images/street_parka_1.jpg', 0),
('p4000000-0000-0000-0000-000000000005', 'https://example.supabase.co/storage/v1/object/public/product-images/street_parka_2.jpg', 1)
ON CONFLICT (id) DO NOTHING;

-- Seed demo cart items
INSERT INTO cart_items (id, session_id, product_id, size, quantity) VALUES
('a0000000-0000-0000-0000-000000000001', 'demo-session-id-1', 'p1000000-0000-0000-0000-000000000001', 'L', 2),
('a0000000-0000-0000-0000-000000000002', 'demo-session-id-1', 'p2000000-0000-0000-0000-000000000001', 'XL', 1),
('a0000000-0000-0000-0000-000000000003', 'demo-session-id-2', 'p4000000-0000-0000-0000-000000000001', 'M', 1)
ON CONFLICT (id) DO NOTHING;

-- Seed demo order
INSERT INTO orders (id, session_id, customer_name, email, phone, address, total_amount, status) VALUES
('d0000000-0000-0000-0000-000000000001', 'demo-session-id-3', 'Jane Doe', 'jane@example.com', '+919876543210', '123 Streetwear Ave, Metro City', 129.97, 'demo')
ON CONFLICT (id) DO NOTHING;

INSERT INTO order_items (id, order_id, product_id, quantity, size, unit_price) VALUES
('e0000000-0000-0000-0000-000000000001', 'd0000000-0000-0000-0000-000000000001', 'p1000000-0000-0000-0000-000000000001', 1, 'M', 29.99),
('e0000000-0000-0000-0000-000000000002', 'd0000000-0000-0000-0000-000000000001', 'p4000000-0000-0000-0000-000000000001', 1, 'L', 99.98)
ON CONFLICT (id) DO NOTHING;

-- Seed contact messages
INSERT INTO contact_messages (id, name, email, phone, message) VALUES
('f0000000-0000-0000-0000-000000000001', 'Alex Mercer', 'alex@example.com', '+919999999999', 'Interested in a custom bulk order of 50 screen-printed Oversized T-Shirts for our streetwear group. Do you support metallic prints?'),
('f0000000-0000-0000-0000-000000000002', 'Sam Wilson', 'sam@example.com', NULL, 'Can I get custom embroidery on the Heavyweight Fleece Hoodie? I have my own logo design.')
ON CONFLICT (id) DO NOTHING;
