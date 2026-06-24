from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="Shopify ZIP Code Pricing Demo",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Demo ke liye open. Production me Shopify store URL add karna.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ZIP_PRICES = {
    "75028": 1499,
    "10001": 1699,
    "90210": 1799,
}


class PriceRequest(BaseModel):
    product_id: str = Field(..., min_length=1)
    variant_id: str = Field(..., min_length=1)
    zip_code: str = Field(..., min_length=5, max_length=10)


class PriceResponse(BaseModel):
    success: bool
    zip_code: str
    price: Optional[int]
    currency: str
    message: str


@app.get("/")
def health_check():
    return {
        "status": "running",
        "message": "Shopify ZIP Code Pricing Backend is live"
    }


@app.post("/api/check-price", response_model=PriceResponse)
def check_price(request: PriceRequest):
    zip_code = request.zip_code.strip()

    if not zip_code.isdigit():
        raise HTTPException(
            status_code=400,
            detail="ZIP code must contain only numbers"
        )

    if zip_code in ZIP_PRICES:
        return {
            "success": True,
            "zip_code": zip_code,
            "price": ZIP_PRICES[zip_code],
            "currency": "USD",
            "message": "Price available for this location"
        }

    return {
        "success": False,
        "zip_code": zip_code,
        "price": None,
        "currency": "USD",
        "message": "Price not available for this ZIP code"
    }