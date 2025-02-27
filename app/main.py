# FastAPI
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

# Routers
from app.api.routers.auth import router as auth_router
from app.api.routers.posts import router as posts_router
from app.admin.routes import router as admin_router
from app.config import settings
from app.core.database import create_db_and_tables


app = FastAPI(title="AI API by Charles EDOU NZE", debug=settings.debug)


# Routes publiques pour l'authentification
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# Endpoints de l'API publique
app.include_router(posts_router, prefix="/api/posts", tags=["Posts"])

# Interface d'administration
app.include_router(admin_router, prefix="/admin", tags=["Admin"])

# Montage du répertoire des fichiers statiques pour l'admin
app.mount("/admin/static", StaticFiles(directory="app/admin/static"), name="admin_static")

# Redirige la racine vers l'admin
@app.get("/", include_in_schema=False)
async def home():
    return RedirectResponse(url="/admin")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

#uvicorn app.main:app --reload