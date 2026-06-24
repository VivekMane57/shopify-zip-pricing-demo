# Shopify ZIP Code Pricing Demo

A Shopify + FastAPI demo that provides ZIP code–based product pricing.

## Features

- Shopify Product Page Integration
- Custom Liquid Widget
- ZIP Code Input
- FastAPI Backend
- Location-Based Pricing
- REST API
- Render Deployment
- Swagger API Documentation

## Tech Stack

### Frontend
- Shopify
- Liquid
- HTML
- CSS
- JavaScript

### Backend
- FastAPI
- Python

### Deployment
- Render

## Project Structure

```text
shopify-zip-pricing-demo/
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## API Endpoint

### Check Price

```http
POST /api/check-price
```

Request:

```json
{
  "product_id": "123",
  "variant_id": "456",
  "zip_code": "75028"
}
```

Response:

```json
{
  "success": true,
  "zip_code": "75028",
  "price": 1499,
  "currency": "USD",
  "message": "Price available for this location"
}
```

## Demo ZIP Codes

| ZIP Code | Price |
|-----------|---------|
| 75028 | $1499 |
| 10001 | $1699 |
| 90210 | $1799 |
| Others | Not Available |

## Live Demo

### Backend API

https://shopify-zip-pricing-demo-6ui2.onrender.com

### API Docs

https://shopify-zip-pricing-demo-6ui2.onrender.com/docs

### Shopify Product Page

https://zip-pricing-demo-ab2kkshb.myshopify.com/products/sample-sofa

## How It Works

1. Customer enters ZIP code.
2. Shopify frontend sends request to FastAPI backend.
3. Backend validates ZIP code.
4. Pricing is returned based on location.
5. Product page displays estimated price.

## Author

Vivek Mane

GitHub:
https://github.com/VivekMane57
