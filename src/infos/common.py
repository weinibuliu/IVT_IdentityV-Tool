#存放战斗中移动、视角移动、点击等信息

from time import sleep
from random import randint,uniform

from maa.context import Context
from maa.custom_action import CustomAction

class Move(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        def move(direction:int=0,duration:int=10000):
            match direction:
                case 0: #向前移动
                    context.override_pipeline({"基础移动":{"end": [175,415,10,10], "duration": duration}})
                case 1: #向右移动
                    context.override_pipeline({"基础移动":{"end": [275,515,10,10], "duration": duration}})
                case 2: #向后移动
                    context.override_pipeline({"基础移动":{"end": [175,615,10,10], "duration": duration}})
                case 3: #向左移动
                    context.override_pipeline({"基础移动":{"end": [75,515,10,10], "duration": duration}})
                case _:
                    raise ValueError(f"Class Error:{__class__.__name__},please contact to the developers.")
            context.run_pipeline("基础移动")

        direction = randint(0,3)
        duration = randint(7,12)*1000 #swipe 中 duration 单位为毫秒
        move(direction,duration)

        return True
    
class Vision_Move(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        def move(direction:int,duration:int):
            match direction:
                case 0: #向左移动视角
                    context.override_pipeline({"基础视角移动":{"end": [370,255,10,10], "duration": duration}})
                case 1 : #向右移动视角
                    context.override_pipeline({"基础视角移动":{"end": [970,255,10,10], "duration": duration}})
                case _:
                    raise ValueError(f"Class Error:{__class__.__name__},please contact to the developers.")
            context.run_pipeline("基础视角移动")

        direction = randint(0,1)
        move(direction,1000)
        
        return True

class Hide_Mixed_Move_Jump(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        direction = randint(0,3)
        context.tasker.controller.post_touch_down(175,515,0,50)
        sleep(0.05)
        match direction:
            case 0:
                stop_x = 175
                stop_y = 415
            case 1:
                stop_x = 275
                stop_y = 515
            case 2:
                stop_x = 175
                stop_y = 615
            case 3:
                stop_x = 75
                stop_y = 515
            case _:
                raise ValueError(f"Class Error:{__class__.__name__},please contact to the developers.")

        duration_time = randint(5,8)
        
        i = 0
        ti = 0
        click_x = randint(1125,1195)
        click_y = randint(550,620)
        if stop_x != 175:
            if stop_x > 175:
                stop_x = list(range(175,stop_x))
            elif stop_x < 175:
                stop_x = list(range(stop_x,175))

            for x in stop_x:
                context.tasker.controller.post_touch_move(x,515,0,50)
                i += 1
                ti += 1
                sleep(0.1)
                if i == 20:
                    job_statu = context.run_recognition("fight_赛后_继续_仅识别",context.tasker.controller.post_screencap().wait().get())
                    if job_statu is not None and job_statu.best_result.text == "继续":
                        break
                    context.tasker.controller.post_touch_down(click_x,click_y,1,30)
                    sleep(0.1)
                    context.tasker.controller.post_touch_up(contact=1)
                    i = 0
                    job_statu = None
                if ti >= duration_time*10:
                    break

        if stop_y != 515:
            if stop_y > 515:
                stop_y = list(range(515,stop_y))
            elif stop_y < 515:
                stop_y = list(range(stop_y,515))

            for y in stop_y:
                context.tasker.controller.post_touch_move(175,y,0,50)
                i += 1
                ti += 1
                sleep(0.1)
                if i == 20:
                    job_statu = None
                    job_statu = context.run_recognition("fight_赛后_继续_仅识别",context.tasker.controller.post_screencap().wait().get())
                    if job_statu is not None and job_statu.best_result.text == "继续":
                        break
                    context.tasker.controller.post_touch_down(click_x,click_y,1,30)
                    sleep(0.1)
                    context.tasker.controller.post_touch_up(contact=1)
                    i = 0
                if ti >= duration_time*10:
                    break

        context.tasker.controller.post_touch_up(contact=0)

        return True