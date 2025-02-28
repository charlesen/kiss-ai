# FastAPI
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

# Routers
from app.api.routers.openai import router as openai_router
from app.config import settings


app = FastAPI(title="AI API by Charles EDOU NZE", debug=settings.debug)

# Endpoints de l'API publique
app.include_router(openai_router, prefix="/api/openai", tags=["Generate"])

# Redirige la racine vers l'admin
@app.get("/", include_in_schema=False)
async def home():
    # Return to docs page
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

#uvicorn app.main:app --reload