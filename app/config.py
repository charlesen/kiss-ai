from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    debug: bool = False
    openai_api_key: str
    openai_model: str
    master_key: str

    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.mysql_username}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"

    class Config:
        env_file = [".env", ".env.local"]  # .env.local pourra écraser .env
        env_file_encoding = "utf-8"

settings = Settings()
