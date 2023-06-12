from dataclasses import dataclass
from environs import Env


@dataclass 
class Tg_bot:
    token: str

@dataclass
class Config:
    tg_bot: Tg_bot


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=Tg_bot(token=env('BOT_TOKEN')))