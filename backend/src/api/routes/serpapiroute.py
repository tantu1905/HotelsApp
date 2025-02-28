from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.services.serpservice import SerpService
from src.core.config import settings
import json
router = APIRouter()
@router.post("/serpapi")
async def get_details(property_token:str):
    with open ("arguments.json", "r") as f:
        data = json.load(f)
    location = data["city"]
    check_in = data["check_in"]
    check_out = data["check_out"]
    serp = SerpService(api_key=settings.hotels_apikey)
    details = serp.very_details(property_key=property_token,city_name=location,check_in=check_in,check_out=check_out)
    extracted_data = []

    for entry in details["featured_prices"]:
        rooms = entry.get("rooms", [])
        if rooms:
            room = rooms[0]
            extracted_data.append({
                "source": entry.get("source"),
                "link": entry.get("link"),
                "logo": entry.get("logo"),
                "lowest_daily_with_tax": room["rate_per_night"].get("lowest"),
                "lowest_daily_without_tax": room["rate_per_night"].get("before_taxes_fees"),
                "total_price_with_tax": room["total_rate"].get("lowest"),
                "total_price_without_tax": room["total_rate"].get("before_taxes_fees")
            })
    return JSONResponse(content=extracted_data)