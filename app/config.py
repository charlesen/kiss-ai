from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    debug: bool = False
    openai_api_key: str
    admin_secret: str
    secret_key: str = "votre_default_secret"
    mysql_username: str
    mysql_password: str
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_database: str

    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.mysql_username}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"

    class Config:
        # Charger d'abord .env, puis .env.local qui écrase les valeurs en doublon
        env_file = [".env", ".env.local"]
        env_file_encoding = "utf-8"

settings = Settings()
