from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict( 
        env_file='.env', env_file_encoding='utf-8'
    )

    DATABASE_URL: str


"""
SettingsConfigDict: é um objeto do pydantic-settings que carrega as variáveis
em um arquivo de configuração. Por exemplo, um .env.

env_file='.env', env_file_encoding='utf-8' Aqui definimos o caminho para o
arquivo de configuração e o encoding dele.

DATABASE_URL: Essa variável será preenchida com o valor encontrado com o mesmo
nome no arquivo .env.
"""
