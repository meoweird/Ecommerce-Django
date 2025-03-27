import asyncio
import logging
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import httpx

load_dotenv()
logging.basicConfig(level=logging.INFO)

app = FastAPI()

SERVICE_URLS = {
    "books" : os.getenv("BOOKSVC_URL"),
    "clothes" : os.getenv("CLOTHESSVC_URL"),
    "laptops" : os.getenv("LAPTOPSVC_URL")
}

@app.get("/api/items/")
async def get_all_items(): 
    invalid_services = [service for service, url in SERVICE_URLS.items() if url is None]
    if invalid_services:
        raise HTTPException(status_code=500, detail=f"Missing URLs for services: {', '.join(invalid_services)}")

    all_items = []
    async with httpx.AsyncClient(follow_redirects=True) as client:
        for service, url in SERVICE_URLS.items():
            logging.info(f"Fetching data from {service} service at {url}")
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    items = response.json()
                    logging.info(f"Items from {service} service: {items}")
                    for item in items:
                        item["category"] = service
                        all_items.append(item)
                else:
                    logging.error(f"Failed to fetch data from {service} service: {response.text}")
            except httpx.ConnectError:
                logging.error(f"Connection error while fetching data from {service} service at {url}")
            except Exception as e:
                logging.error(f"Unexpected error while fetching data from {service} service: {e}")

    return {"items": all_items}

@app.get("/api/items/{category}/")
async def get_items_by_category(category: str):
    if category not in SERVICE_URLS:
        raise HTTPException(status_code=400, detail="Invalid category")

    async with httpx.AsyncClient() as client:
        response = await client.get(SERVICE_URLS[category])

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Service unavailable")

    return response.json()

@app.get("/api/items/{category}/{item_id}/")
async def get_item_detail(category: str, item_id: str):
    if category not in SERVICE_URLS:
        raise HTTPException(status_code=400, detail="Invalid category")

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICE_URLS[category]}/{item_id}/")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Item not found")

    return response.json()