from typing import Any
from aiogram.types import Message
from aiogram.filters import BaseFilter
from services.services import load_from_file


admin_ids: list[int] = [790465874]

class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids
    
class IsTime(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        if message.text.split(':')[0].isdigit() and message.text.split(':')[1].isdigit():
            first_dg = int(message.text.split(':')[0])
            second_dg = int(message.text.split(':')[1])
            if 0 <= first_dg <= 24 and 0 <= second_dg <= 60:
                return {'time': [first_dg, second_dg]}
        else:
            return False
                # return {'time': f'{first_dg}:{second_dg}'}
        #         return True
        #     else:
        #         return False
        # else:
        #     return False

class NewUser(BaseFilter):
    # def __init__(self) -> None:
        

    async def __call__(self, message: Message):
        users = load_from_file()
        return message.from_user.id in users