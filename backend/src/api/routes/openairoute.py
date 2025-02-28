from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.services.openaiservice import OpenAIService
from src.core.config import settings
import json
router = APIRouter()

@router.post("/openai")
async def openai_route(question:str):
    openai_service = OpenAIService(endpoint=settings.openai_endpoint,key=settings.openai_apikey,model=settings.openai_model,version=settings.openai_version)
    try:
        response = openai_service.find_hotels(question)
        print(response)
        print(response["response"].model_dump())
        with open ("arguments.json", "w") as f:
            json.dump(response["arguments"], f, indent=2, ensure_ascii=False)
        return JSONResponse(content=response["response"].model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
