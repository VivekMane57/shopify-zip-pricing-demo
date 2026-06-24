import hmac
import hashlib
import os
import time
from typing import Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Shopify ZIP Code Pricing Demo")

SHOPIFY_API_SECRET = os.getenv("SHOPIFY_API_SECRET", "demo_secret_for_local")

ZIP_PRICES = {
    "75028": 1499,
    "10001": 1699,
    "90210": 1799,
}

RATE_LIMIT = {}
MAX_REQUESTS = 20
WINDOW_SECONDS = 60


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://zip-pricing-demo-ab2kkshb.myshopify.com",
        "https://admin.shopify.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {
        "status": "running",
        "message": "Secure Shopify ZIP Pricing Backend is live",
    }


def verify_rate_limit(ip: str):
    now = time.time()
    window_start = now - WINDOW_SECONDS

    requests = RATE_LIMIT.get(ip, [])
    requests = [t for t in requests if t > window_start]

    if len(requests) >= MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Too many requests")

    requests.append(now)
    RATE_LIMIT[ip] = requests


def verify_shopify_signature(query_params: dict):
    signature = query_params.get("signature")

    if not signature:
        raise HTTPException(status_code=401, detail="Missing Shopify signature")

    params = {
        key: value
        for key, value in query_params.items()
        if key not in ["signature", "hmac"]
    }

    message = "&".join(
        f"{key}={params[key]}"
        for key in sorted(params.keys())
    )

    calculated_signature = hmac.new(
        SHOPIFY_API_SECRET.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(calculated_signature, signature):
        raise HTTPException(status_code=401, detail="Invalid Shopify signature")


@app.get("/apps/zip-pricing/check-price")
async def check_price_proxy(request: Request):
    client_ip = request.client.host
    verify_rate_limit(client_ip)

    query_params = dict(request.query_params)

    # Shopify App Proxy security check
    verify_shopify_signature(query_params)

    zip_code = query_params.get("zip_code", "").strip()
    product_id = query_params.get("product_id", "")
    variant_id = query_params.get("variant_id", "")

    if not zip_code or not zip_code.isdigit():
        raise HTTPException(status_code=400, detail="Invalid ZIP code")

    if zip_code in ZIP_PRICES:
        return {
            "success": True,
            "zip_code": zip_code,
            "product_id": product_id,
            "variant_id": variant_id,
            "price": ZIP_PRICES[zip_code],
            "currency": "USD",
            "message": "Price available for this location",
        }

    return {
        "success": False,
        "zip_code": zip_code,
        "product_id": product_id,
        "variant_id": variant_id,
        "price": None,
        "currency": "USD",
        "message": "Price not available for this ZIP code",
    }