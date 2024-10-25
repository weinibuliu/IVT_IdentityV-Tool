# 启动入口
# 通过 for 循环注册 Custom

from pathlib import Path
from maa.toolkit import Toolkit

import maa

import src.ban as ban
import src.notice as notice
import src.fight as fight

# 获取路径
main_path = Path.cwd()


def main():
    # 注册自定义识别器与动作
    rec_names = ban.rec_name_list() + notice.rec_name_list() + fight.rec_name_list()
    rec_details = ban.rec_list() + notice.rec_list() + fight.rec_list()

    act_names = ban.act_name_list() + notice.act_name_list() + fight.act_name_list()
    act_details = ban.act_list() + notice.act_list() + fight.act_list()

    # 注册自定义识别器
    for name, detail in zip(rec_names, rec_details):
        Toolkit.pi_register_custom_recognition(name, detail)

    # 注册自定义动作
    for name, detail in zip(act_names, act_details):
        Toolkit.pi_register_custom_action(name, detail)

    # 启动 MaaPiCli
    Toolkit.pi_run_cli(f"{main_path}/res", f"{main_path}/cache", False)


if __name__ == "__main__":
    main()
