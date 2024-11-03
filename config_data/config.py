from dataclasses import dataclass
from environs import Env

@dataclass
class APIConfig:
    api_key: str


@dataclass
class DataBaseConfig:
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str


@dataclass
class ConfigData:
    api: APIConfig
    db: DataBaseConfig


class Config:
    def __init__(self, path: str | None = None):
        self.path = path

    def __load_api_config(self) -> APIConfig:
        env = Env()
        env.read_env(self.path)
        return APIConfig(api_key=env('API_KEY'))

    def __load_db_config(self) -> DataBaseConfig:
        env = Env()
        env.read_env(self.path)
        return DataBaseConfig(
            db_host=env("POSTGRES_HOST"),
            db_port=env("POSTGRES_PORT"),
            db_user=env("POSTGRES_USER"),
            db_password=env("POSTGRES_PASSWORD"),
            db_name=env("POSTGRES_DB")
        )

    def load_config(self) -> ConfigData:
        try:
            return ConfigData(
                api=self.__load_api_config(),
                db=self.__load_db_config()
            )

        except Exception as e:
            raise Exception("Ошибка при загрузке переменных среды: ", e)