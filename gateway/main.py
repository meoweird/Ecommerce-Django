import os
from fastapi import FastAPI, HTTPException, Request
from dotenv import load_dotenv
import httpx

load_dotenv()


SERVICE_URLS = {
    'user': os.getenv("USER_SVC"),
    'items': os.getenv("ITEM_SVC"),
    'order': os.getenv("ORDER_SVC"),
    'cart': os.getenv("CART_SVC"),
    'payment': os.getenv("PAYMENT_SVC"),
    'shipment': os.getenv("SHIPMENT_SVC"),
}

app = FastAPI()

async def proxy_request(service: str, path: str, request: Request):
    if service not in SERVICE_URLS or not SERVICE_URLS[service]:
        raise HTTPException(status_code=400, detail="Invalid or missing service URL")

    url = f"{SERVICE_URLS[service]}{path}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=url,
                params=request.query_params,
                headers={key: value for key, value in request.headers.items() if key.lower() != 'host'},
                content=await request.body()
            )
            response.raise_for_status()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"Request error: {exc}")
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)

    return response.json()

@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def route_request(service: str, path: str, request: Request):
    return await proxy_request(service, f"{path}", request)