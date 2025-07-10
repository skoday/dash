from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env"
    )

    rama_url: str
    password: str


settings = Settings(_env_file='.env')