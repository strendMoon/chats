from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OAUTH_GOOGLE_CLIENT_SECRET: str
    OAUTH_GOOGLE_CLIENT_ID: str
    OAUTH_GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/google/callback"
    OAUTH_GOOGLE_YOUTUBE_REDIRECT_URI: str = "http://localhost:8000/auth/google/youtube/callback"
    OAUTH_GOOGLE_BASE_URI: str = "https://accounts.google.com/o/oauth2/v2/auth"
    JWT_SECRET_KEY: str = "dev-secret-change-me"
    JWT_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()