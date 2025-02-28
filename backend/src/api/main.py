from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import openairoute,serpapiroute

app = FastAPI()

app.include_router(openairoute.router)
app.include_router(serpapiroute.router)





