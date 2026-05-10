# TIJARA API Documentation - Frontend Integration Guide

This documentation provides a comprehensive guide for frontend developers to integrate with the TIJARA B2B Backend.

---

## 1. Global Specifications

### Base URL
`http://localhost:8000/api/`

### Authentication
- Uses **JWT (JSON Web Tokens)**.
- Include the access token in the header: `Authorization: Bearer <access_token>`.
- Token expires in 1 day, Refresh token in 7 days.

### Pagination
- Most List endpoints use `PageNumberPagination`.
- **Response Format**:
```json
{
  "count": 100,
  "next": "http://.../?page=2",
  "previous": null,
  "results": [...]
}
```

### Roles
- **Trader**: Standard user. Can buy from other stores and own their own store.
- **Admin**: Full access via Django Admin panel.

---

## 2. Authentication & Profile

### [POST] Register
- **Endpoint**: `/auth/register/`
- **Request Body**:
```json
{
  "phone": "01000000001",
  "name": "Full Name",
  "password": "secure_password",
  "email": "user@example.com",
  "role": "trader"
}
```
- **Response (201 Created)**:
```json
{
  "user": {
    "id": "uuid",
    "phone": "01000000001",
    "name": "Full Name",
    "email": "user@example.com",
    "role": "trader",
    "address": null,
    "notification_settings": {
      "push_enabled": true,
      "email_enabled": false,
      "order_updates_enabled": true,
      "offers_enabled": true
    },
    "created_at": "2026-05-09T..."
  },
  "token": {
    "refresh": "...",
    "access": "..."
  }
}
```

### [POST] Login
- **Endpoint**: `/auth/login/`
- **Request Body**: `{ "phone": "01000000001", "password": "secure_password" }`
- **Response (200 OK)**: `{ "refresh": "...", "access": "..." }`

### [GET] Profile
- **Endpoint**: `/auth/profile/`
- **Response (200 OK)**:
```json
{
  "id": "uuid",
  "phone": "01000000001",
  "name": "Full Name",
  "email": "user@example.com",
  "role": "trader",
  "address": "Street Address, City",
  "notification_settings": {
    "push_enabled": true,
    "email_enabled": false,
    "order_updates_enabled": true,
    "offers_enabled": true
  },
  "created_at": "2026-05-09T..."
}
```

---

## 3. Stores Management

### [GET] Categories
- **Endpoint**: `/stores/categories/`
- **Response**:
```json
[
  {
    "id": "uuid",
    "name": "Electronics",
    "icon": "devices",
    "parent": null,
    "subcategories": [
      { "id": "uuid", "name": "Mobile Phones", "icon": "smartphone", "parent": "uuid", "subcategories": [] }
    ]
  }
]
```

### [GET] List/Search Stores
- **Endpoint**: `/stores/`
- **Query Params**: `?search=store_name&category=Electronics&is_featured=true&page=1`
- **Response**:
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "owner": "user_uuid",
      "name": "Global Electronics",
      "logo_url": "http://...",
      "description": "Premium electronics supplier",
      "category": "Electronics",
      "rating": 4.5,
      "is_featured": true,
      "location_lat": 30.05,
      "location_lng": 31.23,
      "created_at": "2026-05-09T..."
    }
  ]
}
```

### [POST] Create Store
- **Endpoint**: `/stores/`
- **Auth Required**: Yes
- **Request Body**: Same as Store object fields.

---

## 4. Products Management

### [GET] List Products by Store
- **Endpoint**: `/products/store/<store_id>/`
- **Query Params**: `?category=uuid&is_popular=true&status=in_stock&page=1`
- **Response**:
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "store": {
    "id": "store_uuid",
    "owner": "user_uuid",
    "name": "Global Electronics",
    "logo_url": "http://...",
    "description": "...",
    "category": "...",
    "rating": 4.5,
    "is_featured": true,
    "location_lat": 30.05,
    "location_lng": 31.23,
    "created_at": "..."
  },
  "results": [
    {
      "id": "uuid",
      "store": "store_uuid",
      "category": "category_uuid",
      "name": "Laptop Pro 15",
      "description": "High performance laptop",
      "image_url": "http://...",
      "is_popular": true,
      "status": "in_stock",
      "variants": [
        {
          "id": "uuid",
          "size": "16GB RAM / 512GB SSD",
          "price": "1200.00",
          "cost": "900.00",
          "stock_quantity": 15,
          "sku": "LP15-16-512"
        }
      ],
      "created_at": "2026-05-09T..."
    }
  ]
}
```

### [POST] Create Product
- **Endpoint**: `/products/`
- **Request Body**:
```json
{
  "category": "uuid",
  "name": "Product Name",
  "description": "Description",
  "image_url": "http://...",
  "status": "in_stock",
  "variants": [
    {
      "size": "Large",
      "price": "100.00",
      "cost": "70.00",
      "stock_quantity": 50,
      "sku": "UNIQUE-SKU-1"
    }
  ]
}
```
*(ملاحظة: يتم ربط المنتج تلقائياً بالمتجر الخاص بالمستخدم الحالي)*

---

## 5. Orders & Analytics

### [POST] Create Order
- **Endpoint**: `/orders/`
- **Request Body**:
```json
{
  "store": "store_uuid",
  "items": [
    {
      "product": "product_uuid",
      "variant": "variant_uuid",
      "quantity": 5
    }
  ]
}
```

### [GET] My Orders
- **Endpoint**: `/orders/`
- **Query Params**: `?type=placed` (Buying) OR `?type=received` (Selling)
- **Response**:
```json
{
  "count": 1,
  "results": [
    {
      "id": "uuid",
      "buyer": "user_uuid",
      "store": "store_uuid",
      "status": "pending",
      "total_amount": "500.00",
      "items": [
        {
          "id": "uuid",
          "product": "product_uuid",
          "variant": "variant_uuid",
          "quantity": 5,
          "price_at_order": "100.00"
        }
      ],
      "created_at": "2026-05-09T..."
    }
  ]
}
```

### [GET] Analytics Dashboard
- **Endpoint**: `/orders/analytics/dashboard/`
- **Auth Required**: Store Owner
- **Response**:
```json
{
  "total_sales": 15000.00,
  "total_orders": 45,
  "revenue": 15000.00,
  "best_sellers": [
    {
      "product__name": "Laptop Pro 15",
      "total_quantity": 20
    }
  ]
}
```

---

## 6. Final Database Schema

### Users App
- **User**: `id (UUID)`, `phone (Unique)`, `name`, `email`, `role (trader/admin)`, `address`, `created_at`.
- **NotificationSettings**: `id (UUID)`, `user (1-to-1)`, `push_enabled`, `email_enabled`, `order_updates_enabled`, `offers_enabled`, `updated_at`.

### Stores App
- **Category**: `id (UUID)`, `name (Unique)`, `icon`, `parent (self-referencing)`, `created_at`.
- **Store**: `id (UUID)`, `owner (User FK)`, `name`, `logo_url`, `description`, `category`, `rating`, `is_featured`, `location_lat`, `location_lng`, `created_at`.

### Products App
- **Product**: `id (UUID)`, `store (FK)`, `category (FK)`, `name`, `description`, `image_url`, `is_popular`, `status (in_stock/out_of_stock)`, `created_at`.
- **ProductVariant**: `id (UUID)`, `product (FK)`, `size`, `price`, `cost`, `stock_quantity`, `sku (Unique)`.

### Orders App
- **Order**: `id (UUID)`, `buyer (User FK)`, `store (Store FK)`, `status (pending/accepted/processing/shipped/delivered/completed/rejected)`, `total_amount`, `created_at`.
- **OrderItem**: `id (UUID)`, `order (FK)`, `product (FK)`, `variant (FK)`, `quantity`, `price_at_order`.

### Support App
- **SupportTicket**: `id (UUID)`, `user (FK)`, `subject`, `message`, `status (open/in_progress/resolved/closed)`, `priority (low/medium/high)`, `created_at`.

### Media App
- **MediaFile**: `id (UUID)`, `file (Path)`, `url`, `file_type`, `size`, `uploader (User FK)`, `created_at`.
