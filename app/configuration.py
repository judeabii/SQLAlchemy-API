from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOSTNAME: str
    DATABASE_NAME: str

    class Config:
        env_file = "../.env"


settings = Settings()
print(settings.DATABASE_NAME)
