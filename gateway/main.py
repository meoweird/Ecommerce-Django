import os
from fastapi import FastAPI, HTTPException, Request
from dotenv import load_dotenv
import httpx

load_dotenv()


SERVICE_URLS = {
    'user': os.getenv("USER_SVC"),
    'item': os.getenv("ITEM_SVC"),
    'order': os.getenv("ORDER_SVC"),
    'cart': os.getenv("CART_SVC"),
    'payment': os.getenv("PAYMENT_SVC"),
    'shipment': os.getenv("SHIPMENT_SVC"),
}

app = FastAPI()

async def proxy_request(service: str, path: str, request: Request):
    if service not in SERVICE_URLS:
        raise HTTPException(status_code=400, detail="Invalid service")

    url = f"{SERVICE_URLS[service]}{path}"
    
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=url,
            params=request.query_params,
            headers=dict(request.headers),
            content=await request.body()
        )

    return response.json()

@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def route_request(service: str, path: str, request: Request):
    return await proxy_request(service, f"/{path}", request)