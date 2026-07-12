# security.md

# Security Plan

## Overview

Although this project is a demonstration website, it should follow modern security practices so it can be expanded into a production-ready application with minimal architectural changes.

Technology Stack

* **Frontend:** React + TypeScript + Vite + Tailwind CSS
* **Backend:** FastAPI
* **Database:** Supabase (PostgreSQL)

---

# Data Classification

## Public Data

No special protection required.

Includes:

* Product catalog
* Categories
* Product images
* Pricing
* Homepage content

---

## Customer Data

Requires protection.

Includes:

* Customer name
* Email
* Phone number
* Delivery address
* Contact form submissions

This information should never be exposed through public API endpoints.

---

# Backend Security

## Input Validation

All incoming requests must be validated using **Pydantic** models.

Validation includes:

* Required fields
* Email format
* Phone number format
* Quantity must be greater than zero
* Price values must never be trusted from the frontend
* UUID validation for identifiers

---

## SQL Injection Protection

Database access should use parameterized queries through the Supabase client or a trusted PostgreSQL library.

Never construct SQL queries using string concatenation.

---

## API Security

Current Version

* Public read endpoints
* Public cart endpoints
* Public demo checkout
* Public contact form

Future versions can protect sensitive endpoints using **Supabase Auth** with JWT verification.

---

# CORS

FastAPI should only allow requests from approved frontend origins.

Example:

* Local development
* Production website domain

Avoid allowing unrestricted (`*`) origins in production.

---

# Environment Variables

Never hardcode secrets in the source code.

Store sensitive values in environment variables, such as:

* Supabase Project URL
* Supabase Anon Key (frontend only)
* Supabase Service Role Key (backend only)
* Email service credentials (if added later)
* Application secret keys

The Service Role Key must remain exclusively on the backend.

---

# Supabase Security

## Row Level Security (RLS)

Enable Row Level Security for all tables from the beginning.

For Version 1:

* Public read access to `categories`
* Public read access to `products`
* Public read access to `product_images`
* Restricted write access to orders, cart items, and contact submissions through the FastAPI backend

Avoid allowing direct client-side writes to sensitive tables.

---

# File Storage

Product images should be stored in a dedicated Supabase Storage bucket.

Recommendations:

* Public read access for product images
* Restrict uploads to backend-managed workflows
* Use descriptive, unique file names

---

# Rate Limiting

Protect write-heavy endpoints such as:

* `/contact`
* `/orders`
* `/cart`

This reduces the risk of spam and abuse.

A simple in-memory limiter is sufficient for development; a production deployment can use Redis or an API gateway.

---

# Logging

Log:

* Server startup
* API errors
* Unexpected exceptions
* Validation failures

Do not log:

* Customer addresses
* Phone numbers
* Email addresses
* Secrets
* Environment variables

---

# HTTPS

Development:

* HTTP is acceptable on localhost.

Production:

* Enforce HTTPS for all traffic.
* Redirect HTTP requests to HTTPS.

---

# Frontend Security

* Escape user-generated content before rendering.
* Avoid using `dangerouslySetInnerHTML` unless absolutely necessary.
* Validate forms on the client for better user experience, while relying on backend validation for security.
* Store only non-sensitive session information in browser storage.

---

# Deferred for Version 1

The following features are intentionally postponed to keep the demo focused:

* User authentication with Supabase Auth
* Password reset flows
* Multi-factor authentication (MFA)
* Role-based access control (Admin/Staff)
* Audit logs
* Payment security (no payment processing in Version 1)
* Inventory permissions
* Admin dashboard authorization
* Webhooks for external services
* Email verification

These can be added later without requiring significant changes to the current architecture.

---

# Security Goals

Version 1 should:

* Protect customer-submitted information.
* Keep sensitive credentials out of the frontend.
* Use validated API requests.
* Follow secure database access practices.
* Be structured so authentication and authorization can be added later with minimal refactoring.
