from sqlalchemy.orm import Session
from app.models.linkedin_post import LinkedInPost

def save_linkedin_post(
    db: Session,
    topic: str,
    tone: str,
    audience: str,
    keywords: list[str],
    content: str
) -> LinkedInPost:
    post = LinkedInPost(
        topic=topic,
        tone=tone,
        audience=audience,
        keywords=", ".join(keywords) if keywords else "",
        content=content,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
