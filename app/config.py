from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Mode développement (True) ou production (False)
    debug: bool = False

    # OpenAI & authentification
    openai_api_key: str
    openai_model: str
    gemini_ai_api_key: Optional[str] = None
    master_key: str

    # Option directe dans .env
    database_url: Optional[str] = None

    # URL SQLite locale par défaut (dev)
    local_sqlite_url: str = "sqlite:///./app.db"

    # Supabase (prod recommandée)
    supabase_db_url: Optional[str] = None

    # MySQL (optionnel pour prod)
    mysql_username: Optional[str] = None
    mysql_password: Optional[str] = None
    mysql_host: Optional[str] = None
    mysql_port: int = 3306
    mysql_database: Optional[str] = None

    @property
    def resolved_database_url(self) -> str:
        """
        Résout dynamiquement la base de données à utiliser.
        Priorité :
        1. database_url défini manuellement dans .env
        2. debug → SQLite local
        3. supabase_db_url (prod recommandée)
        4. MySQL (prod avancée)
        """
        if self.database_url:
            return self.database_url

        if self.debug:
            return self.local_sqlite_url

        if self.supabase_db_url:
            return self.supabase_db_url

        if all([self.mysql_username, self.mysql_password, self.mysql_host, self.mysql_database]):
            return (
                f"mysql+pymysql://{self.mysql_username}:{self.mysql_password}"
                f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
            )

        raise ValueError("Aucune configuration de base de données valide trouvée.")

    class Config:
        env_file = [".env", ".env.local"]
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
