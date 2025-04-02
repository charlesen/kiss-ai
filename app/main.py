# System
import uvicorn

# FastAPI
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware



# Routers
from app.api.routers.linkedin import router as linkedin_router
from app.api.routers.media import router as media_router
from app.api.routers.openai import router as openai_router
from app.api.routers.text import router as text_router


from app.config import settings


app = FastAPI(title="Kiss AI", debug=settings.debug)

# On autoriser les requêtes CORS venant du frontend (Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ou ["*"] en dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# On monte le répertoire 'public' pour servir des fichiers statiques
app.mount("/public", StaticFiles(directory="public"), name="public")

# Endpoints de l'API publique
app.include_router(openai_router, prefix="/api/openai", tags=["OpenAI"])
app.include_router(media_router, prefix="/api/media", tags=["Media"])
app.include_router(text_router, prefix="/api/text", tags=["Text"])

# Endpoints de l'API privé
app.include_router(linkedin_router, prefix="/api/linkedin", tags=["LinkedIn"])

# Redirige la racine vers l'admin
@app.get("/", include_in_schema=False)
async def home():
    # Return to docs page
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

#uvicorn app.main:app --reload