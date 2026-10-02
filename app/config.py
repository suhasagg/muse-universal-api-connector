from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env", extra="ignore")
    database_url:str="postgresql+asyncpg://connector:connector@localhost:5432/connectors"
    redis_url:str="redis://localhost:6379/0"
    admin_token:str="change-me"
    allowed_spec_hosts:str=""
    execution_allow_private_networks:bool=False
    max_spec_bytes:int=5*1024*1024
    request_timeout_seconds:float=20
settings=Settings()
