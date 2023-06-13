from lexicon.lexicon import COLLEGE_SCHEDULE
from aiogram.types import CallbackQuery


#Функция читает файл, который будет указан
#и возвращает текст в виде 'str'
def get_text_from_file(path_to_file: str) -> str:
    info_from_file = ''
    with open(path_to_file, 'r', encoding='utf-8') as file:
        info_from_file = file.read()
    return info_from_file

# print(get_text_from_file('my_college_assistans_bot/files/file.txt'))

#Класс который создает текст для кнопок клавиатуры в зависимости от нажатых кнопок
class Add_Status_Buttons():
    #В этом списке будут храниться номера тех на кого уже нажимали кнопку
    # pressed_nums = []

    def __init__(self) -> None:
        self.pressed_nums = []

    def __call__(self, callback_num: CallbackQuery, schedule: dict[str, str]) -> bool | dict[str, str]:
        new_schedule = {}
        for num, name in schedule.items():
            if callback_num.data == num and num not in self.pressed_nums:
                new_schedule[num] = '❌ ' + name
                self.pressed_nums.append(num)
            elif callback_num.data == num and num in self.pressed_nums:
                new_schedule[num] = '✅ ' + name
                self.pressed_nums.remove(num)
            elif num in self.pressed_nums:
                new_schedule[num] = '❌ ' + name
            else:
                new_schedule[num] = '✅ ' + name
 
        # if True:
        #     with open('my_college_assistans_bot/files/file.txt', 'w', encoding='utf-8') as file:
        #         new_info = []
        #         for index, num in enumerate(self.pressed_nums, 1):
        #             new_info.append(str(index) + ') ' + schedule[num] + '\n')
        #         file.writelines(new_info)
        if new_schedule:
            return new_schedule
        else:
            return False
        
    def reset_missing_list(self):
        self.pressed_nums = []

add_status_button: Add_Status_Buttons = Add_Status_Buttons()
