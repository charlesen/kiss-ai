from app.db import Base, engine
from app.models import linkedin_post 


def init_db():
    print("[DB] Initialisation de la base de données...")
    Base.metadata.create_all(bind=engine)
    print("[DB] Tables créées avec succès !")


if __name__ == "__main__":
    init_db()
    print("✅ Database initialized!")