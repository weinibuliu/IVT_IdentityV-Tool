from pathlib import Path

from maa.context import Context
from maa.custom_action import CustomAction
from maa.custom_recognition import CustomRecognition

#获取路径
main_path = Path.cwd()

#传出 custom 信息
def rec_name_list() -> list[str]:
    return []
def rec_list() -> list:
    return []
def act_name_list() -> list[str]:
    return []
def act_list() -> list:
    return []

class just_rec_sample(CustomRecognition):
    pass

class just_act_sample(CustomAction):
    pass