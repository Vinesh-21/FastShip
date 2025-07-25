from pydantic_settings import BaseSettings, SettingsConfigDict


_model_config = SettingsConfigDict(
    env_file="./.env",
    env_ignore_empty=True,
    extra="ignore",
)

class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    model_config = _model_config

    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class SecuritySettings(BaseSettings):
    JWT_SECERET_KEY:str
    JWT_ALGORITHM:str

    model_config = _model_config


class MongoDBSettings(BaseSettings):
    MONGODBURI:str

    model_config = _model_config


security_settings=SecuritySettings()

mongoDB_Settings =MongoDBSettings()

settings = DatabaseSettings()


