from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import command

app = FastAPI(
    title="NL2RC API",
    description="Natural Language to Robot Command",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(command.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"status": "NL2RC API running", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}