from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_posts():
    # Logique pour récupérer les posts (exemple statique)
    return {"posts": [{"id": 1, "title": "Premier post"}, {"id": 2, "title": "Deuxième post"}]}

@router.get("/{post_id}")
async def get_post(post_id: int):
    # Logique pour obtenir un post par ID
    return {"post": {"id": post_id, "title": f"Post {post_id}"}}