# db_er.md

# Database Design

## Overview

The application uses **Supabase (PostgreSQL)** as the primary database. Although this is a demo website, the schema is designed so it can evolve into a production-ready e-commerce platform with minimal changes.

---

# Entity Relationship Diagram (Text)

```
Categories
    │
    │ 1 ────────────────∞
    ▼
Products
    │
    │ 1 ────────────────∞
    ▼
Product Images

Products
    │
    │ 1 ────────────────∞
    ▼
Cart Items

Orders
    │
    │ 1 ────────────────∞
    ▼
Order Items
```

> Since Version 1 does not include user authentication, carts and orders are associated with a generated **session_id** rather than a user account.

---

# Tables

## categories

Purpose

Stores clothing categories.

Fields

| Field       | Type      | Notes         |
| ----------- | --------- | ------------- |
| id          | UUID      | Primary Key   |
| name        | TEXT      | Unique        |
| slug        | TEXT      | Unique        |
| description | TEXT      | Optional      |
| created_at  | TIMESTAMP | Default now() |

Indexes

* Primary Key (id)
* Unique Index (slug)
* Unique Index (name)

---

## products

Purpose

Stores product information.

Fields

| Field                   | Type          | Notes              |
| ----------------------- | ------------- | ------------------ |
| id                      | UUID          | Primary Key        |
| category_id             | UUID          | FK → categories.id |
| name                    | TEXT          | Required           |
| slug                    | TEXT          | Unique             |
| description             | TEXT          | Required           |
| price                   | NUMERIC(10,2) | Required           |
| stock                   | INTEGER       | Demo inventory     |
| featured                | BOOLEAN       | Default false      |
| customization_available | BOOLEAN       | Default true       |
| created_at              | TIMESTAMP     | Default now()      |

Indexes

* Primary Key (id)
* Index(category_id)
* Unique(slug)
* Index(featured)

---

## product_images

Purpose

Supports multiple images per product.

Fields

| Field         | Type    | Notes                            |
| ------------- | ------- | -------------------------------- |
| id            | UUID    | Primary Key                      |
| product_id    | UUID    | FK → products.id                 |
| image_url     | TEXT    | Supabase Storage or external URL |
| display_order | INTEGER | Image ordering                   |

Indexes

* Index(product_id)

---

## cart_items

Purpose

Stores shopping cart contents for anonymous demo users.

Fields

| Field      | Type      | Notes                      |
| ---------- | --------- | -------------------------- |
| id         | UUID      | Primary Key                |
| session_id | TEXT      | Browser session identifier |
| product_id | UUID      | FK → products.id           |
| size       | TEXT      | XS–XXL                     |
| quantity   | INTEGER   | Default 1                  |
| created_at | TIMESTAMP | Default now()              |

Indexes

* Index(session_id)
* Index(product_id)
* Composite Index(session_id, product_id, size)

---

## orders

Purpose

Stores submitted demo orders.

Fields

| Field         | Type          | Notes          |
| ------------- | ------------- | -------------- |
| id            | UUID          | Primary Key    |
| session_id    | TEXT          | Demo session   |
| customer_name | TEXT          | Required       |
| email         | TEXT          | Required       |
| phone         | TEXT          | Required       |
| address       | TEXT          | Required       |
| total_amount  | NUMERIC(10,2) | Required       |
| status        | TEXT          | Default "demo" |
| created_at    | TIMESTAMP     | Default now()  |

Indexes

* Primary Key(id)
* Index(email)
* Index(created_at)

---

## order_items

Purpose

Stores products belonging to each order.

Fields

| Field      | Type          | Notes                      |
| ---------- | ------------- | -------------------------- |
| id         | UUID          | Primary Key                |
| order_id   | UUID          | FK → orders.id             |
| product_id | UUID          | FK → products.id           |
| quantity   | INTEGER       | Required                   |
| size       | TEXT          | Required                   |
| unit_price | NUMERIC(10,2) | Snapshot of purchase price |

Indexes

* Index(order_id)
* Index(product_id)

---

# Supabase Storage

Create a bucket:

```
product-images
```

Contents

* Product photos
* Hero banners
* Collection images

Bucket visibility

* Public (demo project)

---

# Initial Seed Data

Categories

* Oversized T-Shirts
* Oversized Hoodies
* Tank Tops
* Jackets

Seed approximately **20–30 products** distributed across the categories, each with:

* 3–5 product images
* Sizes (S, M, L, XL, XXL)
* Demo stock values
* Featured flag for selected products

---

# Relationships

```
categories.id
      │
      ▼
products.category_id

products.id
      │
      ▼
product_images.product_id

products.id
      │
      ▼
cart_items.product_id

orders.id
      │
      ▼
order_items.order_id

products.id
      │
      ▼
order_items.product_id
```

---

# Future Expansion

The schema is designed to accommodate future additions without major restructuring, including:

* User accounts (linked via Supabase Auth)
* Wishlists
* Product reviews and ratings
* Discount codes
* Inventory tracking
* Order status workflow
* Shipping addresses
* Payment records
* Product variants (colors, materials)
* AI-powered recommendations

These can be introduced by adding new tables and relationships while preserving the existing core schema.
