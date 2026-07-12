# BACKEND PROMPT – PHASE 3
## Connect Backend + Frontend

The frontend has already been fully built.

## IMPORTANT

- Do NOT modify, rename, delete, or restructure anything inside the existing frontend project.
- The backend must communicate with the frontend exclusively through REST APIs.
- Continue from the completed Phase 1 (project scaffolding) and Phase 2 (database layer).

This phase is responsible for exposing the API, configuring middleware, validating requests, and integrating with the existing frontend.

---

# Objective

Complete the FastAPI backend by:

- Implementing all REST endpoints
- Connecting services to repositories
- Configuring CORS
- Returning consistent API responses
- Making the backend ready for the existing frontend
- Keeping the architecture clean and scalable

---

# API Base Path

All endpoints must be prefixed with:

```
/api/v1
```

---

# API Endpoints

## Products

### GET

```
/products
```

Features

- Pagination
- Search
- Category filter
- Featured filter
- Price range filter
- Sort by:
  - Newest
  - Price Low → High
  - Price High → Low

Response

```json
{
  "success": true,
  "data": [],
  "pagination": {}
}
```

---

### GET

```
/products/{slug}
```

Return

- Product details
- Category
- Image gallery
- Related products
- Customization availability

Return **404** if not found.

---

### GET

```
/products/featured
```

Return featured homepage products.

---

# Categories

### GET

```
/categories
```

Return all categories.

---

# Cart

Anonymous cart using

```
session_id
```

---

### GET

```
/cart/{session_id}
```

Returns

- Cart items
- Quantities
- Product details
- Subtotal

---

### POST

```
/cart
```

Request

```json
{
  "session_id":"abc123",
  "product_id":"uuid",
  "size":"L",
  "quantity":1
}
```

If the same product and size already exist for the session, increment the quantity instead of creating a duplicate row.

---

### PATCH

```
/cart/{item_id}
```

Update quantity.

Reject values less than 1.

---

### DELETE

```
/cart/{item_id}
```

Remove the item.

---

# Orders

### POST

```
/orders
```

Request

```json
{
  "session_id":"abc123",
  "customer_name":"John Doe",
  "email":"john@example.com",
  "phone":"+911234567890",
  "address":"Customer Address"
}
```

Flow

- Retrieve cart
- Verify products exist
- Calculate total on the server
- Ignore any client-provided prices
- Create order
- Create order items
- Clear the cart
- Return success response

Response

```json
{
  "success": true,
  "message": "Demo order submitted successfully.",
  "order_id": "uuid"
}
```

---

### GET

```
/orders/{order_id}
```

Return

- Customer information
- Ordered products
- Total
- Status
- Order date

Return **404** when appropriate.

---

# Contact

### POST

```
/contact
```

Store contact requests in the database.

Request

```json
{
  "name":"John Doe",
  "email":"john@example.com",
  "phone":"+911234567890",
  "message":"I would like a custom oversized hoodie."
}
```

Response

```json
{
  "success": true,
  "message": "Your message has been received."
}
```

---

# Health

### GET

```
/health
```

Response

```json
{
  "status":"healthy"
}
```

---

# Validation

Validate every request using Pydantic.

Examples

Email

Phone

UUID

Positive quantity

Required strings

Maximum lengths

Reject malformed requests with **422 Unprocessable Entity**.

---

# Response Format

Successful response

```json
{
  "success": true,
  "data": {}
}
```

Collection response

```json
{
  "success": true,
  "data": [],
  "pagination": {}
}
```

Error response

```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested product could not be found."
  }
}
```

Maintain this structure consistently across all endpoints.

---

# Business Logic

The routers must remain thin.

Routers should only:

- Receive requests
- Validate input
- Call services
- Return responses

Business rules belong exclusively in the service layer.

Database interaction belongs exclusively in repositories.

---

# CORS

Configure CORS to allow:

Development

```
http://localhost:5173
```

Allow additional production origins from environment variables.

Support:

- GET
- POST
- PATCH
- DELETE
- OPTIONS

Enable credentials only if required.

---

# Frontend Integration

The frontend should communicate with the backend through an API service layer using:

```
/api/v1
```

Support the following frontend actions:

- Display all products
- Display featured products
- View product details
- Search products
- Filter by category
- Filter by price
- Sort products
- Add to cart
- Update quantities
- Remove products
- Submit checkout
- Submit contact form

No frontend code should be modified.

---

# Error Handling

Implement centralized exception handlers for:

- Validation errors
- Resource not found
- Database errors
- Unexpected exceptions

Return consistent JSON responses.

Log unexpected errors without exposing sensitive implementation details to the client.

---

# Logging

Log:

- Incoming requests
- Startup
- Shutdown
- Errors
- Validation failures

Do NOT log:

- Customer address
- Phone number
- Email address
- Environment variables
- Service keys

---

# OpenAPI Documentation

Ensure:

```
/docs
```

and

```
/redoc
```

are fully functional.

Every endpoint should include:

- Summary
- Description
- Response model
- HTTP status codes

---

# Testing

Create endpoint tests for:

- Health
- Categories
- Products
- Featured products
- Product details
- Cart CRUD
- Order creation
- Contact form

Include positive and negative test cases.

---

# End-to-End Demo Flow

Verify the following scenario:

1. Frontend requests:

```
GET /api/v1/products
```

2. Backend returns products from Supabase.

3. User adds an item to the cart.

4. Cart updates successfully.

5. User completes the demo checkout.

6. Backend:

- Calculates totals
- Creates the order
- Creates order items
- Clears the cart

7. Frontend displays the demo confirmation page.

8. User submits a customization inquiry through the contact form.

9. Backend stores the inquiry successfully.

---

# Production Readiness

Structure the code so future features can be added without major refactoring, including:

- Supabase Auth
- Admin dashboard
- Product management
- Inventory tracking
- Wishlist
- Reviews and ratings
- Payment gateway integration
- Discount and coupon system
- Shipping providers
- Email notifications
- AI-powered recommendations

---

# Final Deliverable

Produce a complete FastAPI backend that:

- Preserves the existing frontend unchanged
- Connects seamlessly through REST APIs
- Uses the existing project structure from Phase 1
- Uses the database layer from Phase 2
- Provides a clean separation between routers, services, repositories, and schemas
- Implements all documented endpoints
- Includes request validation, CORS, logging, centralized error handling, OpenAPI documentation, and automated tests
- Is ready for future production expansion while fully supporting the current demo application