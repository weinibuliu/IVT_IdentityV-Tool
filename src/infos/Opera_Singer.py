#存放歌剧演员自动战斗相关信息

from time import sleep

from maa.context import Context
from maa.custom_action import CustomAction

class OS_Round(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        context.run_pipeline("歌剧演员_影跃")
        sleep(0.45)
        context.run_pipeline("歌剧演员_普攻")
        sleep(1)
        
        return True