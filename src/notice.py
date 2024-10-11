#通知相关功能实现

from smtplib import SMTP_SSL
from json import load,loads
from pathlib import Path
from email.mime.text import MIMEText

from maa.context import Context
from maa.custom_action import CustomAction
from plyer import notification

from .infos import notice_info

#获取路径
main_path = Path.cwd()

#传出 custom 信息
def rec_name_list() -> list[str]:
    return []
def rec_list() -> list:
    return []
def act_name_list() -> list[str]:
    return ["Desktop_notice","Email_notice"]
def act_list() -> list:
    return [Desktop_notice(),Email_notice()]

class Desktop_notice(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        infos = loads(argv.custom_action_param)
        title = infos["Title"]
        message = infos["Message"]

        notification.notify(title = title,message = message,timeout = 8)
        
        return True

class Email_notice(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:

        with open (f"{main_path}/config/email_config.json","r",encoding="utf-8") as f:
            data = load(f)
            email_enable = bool(data["是否启用邮件通知"])

        if email_enable == True:
            email_details = loads(argv.custom_action_param)
            Title = email_details["Title"]
            Body = email_details["Body"]

            email_config = data["email_config"]
            sender = str(email_config["Send_Address"])
            sender_password = str(email_config["Send_Password"])
            receiver = str(email_config["Receive_Address"])

            smtp_address = str(email_config["SMTP_Address"])
            smtp_port = int(email_config["SMTP_Port"])
                
            doctype = notice_info.email.doctype
            with_eamil = notice_info.email.with_eamil

            body = doctype + Body + with_eamil
            msg = MIMEText(body,"html","utf-8")
            msg["Subject"] = Title
            msg["From"] = sender
            msg["To"] = receiver

            smtp = SMTP_SSL(smtp_address,smtp_port)
            smtp.login(sender,sender_password)
            smtp.sendmail(sender,receiver,msg.as_string())
            smtp.quit()

        return True