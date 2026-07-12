# BACKEND PROMPT – PHASE 2
## Database & Supabase Implementation

The frontend is already complete.

IMPORTANT:

- Do NOT modify anything inside the frontend project.
- Continue from Phase 1.
- Do not create frontend code.
- This phase focuses only on the database layer and business models.
- Do not implement API endpoints yet.

---

# Objective

Implement the complete database layer using **Supabase PostgreSQL** together with the backend business layer.

The backend should be modular and easy to maintain.

---

# Database

Use Supabase PostgreSQL.

Create SQL inside

```
supabase/schema.sql
```

Create seed data inside

```
supabase/seed.sql
```

---

# Database Tables

Implement the following tables.

---

## categories

Fields

- id (UUID Primary Key)
- name
- slug
- description
- created_at

Constraints

- name unique
- slug unique

Indexes

- slug
- name

---

## products

Fields

- id
- category_id
- name
- slug
- description
- price
- stock
- featured
- customization_available
- created_at

Foreign Key

category_id → categories.id

Indexes

- slug
- category_id
- featured

---

## product_images

Fields

- id
- product_id
- image_url
- display_order

Foreign Key

product_id → products.id

---

## cart_items

Anonymous carts.

Fields

- id
- session_id
- product_id
- quantity
- size
- created_at

Indexes

- session_id
- product_id

Composite index

(session_id, product_id, size)

---

## orders

Fields

- id
- session_id
- customer_name
- email
- phone
- address
- total_amount
- status
- created_at

Indexes

- email
- created_at

Default status

demo

---

## order_items

Fields

- id
- order_id
- product_id
- quantity
- size
- unit_price

Foreign Keys

order_id

product_id

---

## contact_messages

Fields

- id
- name
- email
- phone
- message
- created_at

---

# Relationships

categories

↓

products

↓

product_images

products

↓

cart_items

orders

↓

order_items

products

↓

order_items

---

# Supabase Storage

Create a public storage bucket.

```
product-images
```

This bucket stores

- Product images
- Hero banners
- Promotional images

Store URLs inside

product_images.image_url

---

# Seed Data

Populate the database.

Categories

- Oversized T-Shirts
- Oversized Hoodies
- Tank Tops
- Jackets

Generate approximately

20–30 realistic products.

Each product should include

- Description
- Price
- Sizes
- Featured flag
- Customization availability
- 3–5 product image URLs

Insert several demo carts.

Insert at least one demo order.

Insert demo contact messages.

---

# Database Client

Configure a reusable Supabase client.

Create

```
db/client.py
```

Responsibilities

- Read environment variables
- Initialize Supabase
- Expose reusable client

No business logic.

---

# Repository Layer

Implement repositories.

CategoryRepository

Responsibilities

- Get all categories
- Find by ID
- Find by slug

---

ProductRepository

Responsibilities

- List products
- Search
- Filter
- Featured products
- Product details
- Related products

---

CartRepository

Responsibilities

- Get cart
- Add item
- Update quantity
- Remove item

---

OrderRepository

Responsibilities

- Create order
- Retrieve order

---

ContactRepository

Responsibilities

- Save contact form

Repositories should only communicate with Supabase.

No validation.

No business rules.

---

# Service Layer

Implement business services.

CategoryService

ProductService

CartService

OrderService

ContactService

Responsibilities

- Validation
- Business rules
- Error handling
- Repository coordination

Business logic belongs here.

Not inside routers.

---

# Pydantic Models

Create request and response models.

Category

Product

ProductImage

CartItem

Cart

Order

OrderItem

CheckoutRequest

CheckoutResponse

ContactRequest

ContactResponse

HealthResponse

PaginationResponse

---

# Validation

Implement validation using Pydantic.

Validate

Email

Phone number

UUID

Positive quantity

Positive price

Required fields

String lengths

---

# Error Classes

Create reusable exceptions.

Examples

ProductNotFound

CategoryNotFound

CartNotFound

InvalidQuantity

OrderNotFound

ValidationException

---

# Utilities

Create utility modules.

UUID helper

Pagination helper

Response formatter

Price formatter

Date formatter

---

# Constants

Centralize constants.

Categories

Available sizes

Status values

Pagination defaults

API messages

---

# Security Preparation

Prepare helper modules for future authentication.

Do NOT implement authentication.

Simply create placeholders.

---

# Testing Structure

Create starter tests for

Repositories

Services

Database client

No endpoint tests yet.

---

# Deliverables

Generate

- Complete SQL schema
- Seed data
- Supabase client
- Repository layer
- Service layer
- Pydantic schemas
- Utility helpers
- Constants
- Error classes
- Database configuration

Do NOT implement

- FastAPI routes
- API endpoints
- CORS changes
- Frontend integration

Those are implemented in Phase 3 only.