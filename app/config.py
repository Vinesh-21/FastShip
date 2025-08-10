from pydantic_settings import BaseSettings, SettingsConfigDict


_model_config = SettingsConfigDict(
    env_file="./.env",
    env_ignore_empty=True,
    extra="ignore",
)

class AppSettings(BaseSettings):
    APP_NAME: str 
    APP_DOMAIN: str
    model_config=_model_config

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


class NotificationSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str

    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

   

    model_config = _model_config 

class TwilioSettings(BaseSettings):
    TWILIO_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_NUMBER: str

    model_config = _model_config 


twilio_settings = TwilioSettings()


security_settings=SecuritySettings()

mongoDB_Settings =MongoDBSettings()

settings = DatabaseSettings()

notification_settings = NotificationSettings()

app_settings = AppSettings()
