#自动战斗主流程实现

from json import load
from time import sleep,time
from pathlib import Path
from random import randint,shuffle

from maa.context import Context
from maa.custom_action import CustomAction

from .infos import base_roi
from .infos import common
from .infos import Opera_Singer

#获取路径
main_path = Path.cwd()

#传出 custom 信息
def rec_name_list() -> list[str]:
    return []
def rec_list() -> list:
    return []
def act_name_list() -> list[str]:
    return ["Fight"] + ["Thumb_Ups","Move","Vision_Move","Hide_Mixed_Move_Jump"] + ["OS_Round"]
def act_list() -> list:
    Thumb_Ups = common.Thumb_Ups
    Move = common.Move
    Vision_Move = common.Vision_Move
    Hide_Mixed_Move_Jump = common.Hide_Mixed_Move_Jump
    OS_Round = Opera_Singer.OS_Round
    return [Fight()] + [Thumb_Ups(),Move(),Vision_Move(),Hide_Mixed_Move_Jump()] + [OS_Round()]

def get_roi_base_on_state(roi_state:str):
    match roi_state:
        case "PC16_9":
            roi = base_roi.PC16_9
        case "Android16_9":
            roi = base_roi.Android16_9
        case _:
            raise ValueError("roi 声明参数异常，请联系开发者。")
        
    return roi

class Fight(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        model_list = "匹配模式"
        character_list = "歌剧演员"
        with open(f"{main_path}/config/fight_config.json","r",encoding="utf-8") as f:
            data = load(f)
            
        base_options = data["基础设置"]
        character_list = list(base_options["角色队列"])
        character_list_random = bool(base_options["角色队列乱序"])
        model_list = list(base_options["模式队列"])
        model_list_random = bool(base_options["模式队列乱序"])
        thumbs_up = bool(base_options["启用赛后点赞"])
        desktop_notice = bool(base_options["启用桌面通知"])
        email_notice = bool(base_options["启用邮件通知"])

        stop_options = data["停止相关设置"]
        up_weekly = bool(stop_options["启用周上限限制"])
        reputation_limit = stop_options["最低人品值"] #bool and int
        limit_time = stop_options["限制时间"] #bool,int,float
        limit_times = stop_options["限制对局次数"] #bool and int
        
        check_options = data["检测频率设置"]
        check_reputation_rate = check_options["检测人品值频率"]
        check_weely_rate = check_options["检测周上限频率"]

        context.override_pipeline({"匹配成功":{"post_delay": 7000, "next": []}})

        if reputation_limit < 0 or reputation_limit > 100:
            reputation_limit = int(100)
 
        def fight_main(character:str):
            fight_start_time = time()
            time_diff = 0
            check_fight_statu = None
            check_fight_statu = context.run_recognition("fight_赛后_继续_仅识别",context.tasker.controller.post_screencap().wait().get())
            match character:
                case "歌剧演员":
                    context.run_pipeline("歌剧演员_获取影跃位置")
                    context.run_pipeline("歌剧演员_获取普攻位置")

                    while time_diff < 235 and check_fight_statu != "继续":
                        context.run_pipeline("随机移动")
                        context.run_pipeline("随机视角移动")

                        for i in range(randint(20,30)):
                            context.run_pipeline("歌剧演员_循环")
                            i += 1
                            fight_now_time = time()
                            time_diff = fight_now_time - fight_start_time
                            if time_diff >= 235:
                                break

                        check_fight_statu = context.run_recognition("fight_赛后_继续_仅识别",context.tasker.controller.post_screencap().wait().get())
                        if check_fight_statu is not None:
                            check_fight_statu = check_fight_statu.best_result.text
                        fight_now_time = time()
                        time_diff = fight_now_time - fight_start_time
                        if time_diff >= 235:
                                break
                        context.run_pipeline("随机视角移动")

                case _:
                    raise ValueError(f"Class Error:{__class__.__name__},please contact to the developers.")
                
            if time_diff >= 235:
                context.run_pipeline("fight_打开设置")

            context.run_pipeline("fight_赛后_继续")
            context.run_pipeline("fight_点赞")

        def hide_main():
            context.run_pipeline("捉迷藏变身")
            task_statu = None
            
            while task_statu is None and task_statu != "继续":
                context.run_pipeline("随机视角移动")
                context.run_pipeline("捉迷藏移动与跳跃")
                task_statu = context.run_recognition("fight_赛后_继续_仅识别",context.tasker.controller.post_screencap().wait().get())
                if task_statu is not None:
                    task_statu = task_statu.best_result.text
                    if task_statu == "继续":
                        break
                context.run_pipeline("捉迷藏移动与跳跃")
                context.run_pipeline("捉迷藏变身")

            sleep(1)
            context.run_pipeline("fight_点赞")

        def ready(model:str,character:str) -> None:
            context.override_pipeline({"检测是否进入游戏": {"next" :[]}})
            context.run_pipeline("fight_点击书")
            sleep(0.5)
            context.run_pipeline(f"fight_{model}")
            sleep(0.5)
            if model == "匹配模式" or model == "排位模式":
                context.run_pipeline("fight_点击监管者")
                sleep(0.5)
                context.run_pipeline("fight_开始匹配")
                if model == "排位模式":
                    context.run_pipeline("确认禁用",pipeline_override={"确认禁用": {"timeout": 3000}})
                context.override_pipeline({"fight_选择角色":{"template":f"characters//{character}.png"}})
                context.run_pipeline("fight_切换角色")
            elif model == "捉迷藏":
                context.run_pipeline("fight_准备开始")
            else:
                raise ValueError(f"Class Error:{__class__.__name__},please contact to the developers.")

        def main(desktop_notice:bool=desktop_notice,email_notice:bool=email_notice,
                 model_list:list=model_list,model_list_random:bool=model_list_random,
                 character_list:list=character_list,character_list_random:bool=character_list_random,
                 thumbs_up:bool=thumbs_up,
                 reputation_limit:int=reputation_limit,up_weekly:bool=up_weekly,
                 limit_time:bool|int|float=limit_time,limit_times:bool|int=limit_times,
                 check_reputation_rate:int=check_reputation_rate , check_weely_rate:int=check_weely_rate):

            def list_ramdon(m_list_random:bool=model_list_random,c_list_random:bool=character_list_random): #模式、角色队列乱序
                if m_list_random == True:
                    shuffle(model_list)
                if c_list_random == True:
                    shuffle(character_list)

            #flags
            weekly_flag = bool(up_weekly)
            time_flag  = bool(limit_time)
            reputation_flag = bool(reputation_limit)

            stop_time = int(0)
            current_time = int(time())
            if isinstance(limit_time,int):
                stop_time = int(current_time + limit_time*60)
            elif isinstance(limit_time,float):
                limit_time = round(limit_time,1)
                stop_time = int(current_time + limit_time*60*60)
            else:
                raise ValueError(f"Class Error:{__class__.__name__},please contact to the developers.")

            if limit_times == False:
                limit_times = int(-1) #-1 始终为 true  while 循环不会因此中断

            if reputation_limit == False:
                reputation_limit == bool(True)

            #while 循环的初始化工作
            weekly = bool(True)
            limit_time = bool(True)
            fight_times_weekly = int(0)
            fight_times_reputation = int(0)
            while weekly and limit_time and limit_times and reputation_limit:
                list_ramdon()
                real_time = int(time())
                for character in character_list:
                    if time_flag != False and real_time >= stop_time:
                        limit_time = False
                        break
                    if weekly == False or limit_time == False or limit_times == False or reputation_limit == False:
                        break

                    for model in model_list:
                        if weekly == False or limit_time == False or limit_times == False or reputation_limit == False:
                            break
                        if time_flag != False and real_time >= stop_time:
                            limit_time = False
                            break
                        if model == "匹配模式" or model == "排位模式":
                            model_detail = "标准模式"
                            
                        context.override_pipeline({"fight_等待全体玩家准备": {"next":[f"fight_{model_detail}_等待加载"]}})
                        
                        if thumbs_up == False:
                            context.override_pipeline({"fight_赛后_继续": {"next": ["fight_赛后_返回大厅"]}})
                        else:
                            context.override_pipeline({"fight_点赞": {"custom_action_param": {"model_detail": model_detail}}})

                        ready(model,character)
                        if model == "匹配模式" or model == "排位模式":
                            fight_main(character)
                        elif model == "捉迷藏":
                            sleep(2)
                            hide_main()
                        else:
                            raise ValueError(f"Class Error:{__class__.__name__},please contact to the developers.")

                        real_time = int(time())
                        fight_times_weekly += 1
                        fight_times_reputation += 1
                        limit_times -= 1
                        
                        if weekly_flag != False and fight_times_weekly == check_weely_rate:
                            fight_times_weekly = int(0)
                            context.run_pipeline("fight_检测周上限_打开推理之径")
                            sleep(3.5)
                            weekly_detail = context.run_recognition("fight_检测周上限",context.tasker.controller.post_screencap().wait().get())
                            if weekly_detail is not None and int(weekly_detail.best_result.text) == 42000 or int(weekly_detail.best_result.text) == 50400:
                                weekly = bool(False)
                                break
                            context.run_pipeline("退出推理之径")

                        if reputation_flag != False and fight_times_reputation == check_reputation_rate:
                            fight_times_reputation = int(0)
                            context.run_pipeline("fight_检测人品值_打开个人名片")
                            sleep(3.5)
                            reputation_detail = context.run_recognition("fight_检测人品值",context.tasker.controller.post_screencap().wait().get())
                            if reputation_detail is not None and int(reputation_detail.best_result.text) <= reputation_limit:
                                reputation_limit = bool(False)
                                break
                            context.run_pipeline("退出个人名片")

            #notice
            if desktop_notice == True:
                context.run_pipeline("桌面通知",pipeline_override={"桌面通知": {"custom_action_param": {"Title": "任务结束提醒","Message": "本次任务已运行结束。"}}})
            if email_notice == True:
                context.run_pipeline("邮件通知",pipeline_override={"邮件通知": {"custom_action_param": {"Title": "任务结束提醒","Body": "<p><b>本次任务已运行结束。</b></p>"}}})

        main()
        
        return True
 
class Fight_Config_Check(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        #TODO:fight_config.json 文件校验
        return True