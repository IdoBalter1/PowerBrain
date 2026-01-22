from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator
#allows us to take all the environemtnt variables and map them into a python object which we can then use and reference thorughout our code.
class Settings(BaseSettings):
    # need to ensure the environemnt varibales and the config file match
    API_PREFIX : str= "/api"
    DEBUG: bool=False

    DATABASE_URL: str

    ALLOWED_ORIGINS: str=""

    OPENAI_API_KEY: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @field_validator("ALLOWED_ORIGINS") # transfomr the format of the data and validate the data check it is in an acceptable ormat.
    def parse_allwoed_origins(cls,v:str) -> List[str]:
        return v.split(',') if v else []
    
    class Config: # instructions for pydantic, read form this file use this ecnoding and be case sensitife. Tells pydantic how to read the .env file
        env_file= ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        # can also pass in env_prefix - prefix for all env vars, env_nested_delimeter = "__" delimeter for nested vars. etc.

settings = Settings()