#存放通知相关信息

from datetime import datetime

current_time = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")

class email():
    doctype = "<!DOCTYPE html><html><head><meta charset='utf-8'></head>"
    with_eamil = f'''<p><i>Time: {current_time}</i><br />
    <i>邮件内容由</i><b><a href='https://www.github.com/weinibuliu/IdentityV_Tool'>  IVT  </a></b><i>自动构建。</i><br />
    <i>如有错误，欢迎前往项目反馈。</i></p>'''
    
class desktop():
    pass