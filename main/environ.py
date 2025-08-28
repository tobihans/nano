from django.core.management.utils import get_random_secret_key
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environ(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    debug: bool = False
    secret_key: str = get_random_secret_key()

    allowed_hosts: set[str] = set()
    internal_ips: set[str] = {"127.0.0.1"}

    language_code: str = "en-us"


env = Environ()
