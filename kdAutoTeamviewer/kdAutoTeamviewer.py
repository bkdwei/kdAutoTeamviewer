'''
Created on 2019年4月5日

@author: bkd
'''
try:
    from os import startfile
    import win32gui
except Exception as e:
    pass
from os.path import expanduser,join
import sys
import time    
import threading

import smtplib
from email.mime.multipart import MIMEMultipart    
from email.mime.text import MIMEText    
from email.mime.image import MIMEImage 
            
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication

from .fileutil import  get_file_realpath,get_option_value


class kdAutoTeamviewer(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(get_file_realpath("kdAutoTeamviewer.ui"), self)
        
    @pyqtSlot()    
    def on_pb_start_teamwiewer_clicked(self):
        startfile(join(expanduser("~"),"teamviewer.exe.lnk"))
    @pyqtSlot()
    def on_pb_take_screenshot_clicked(self):
        hwnd = win32gui.FindWindow(None, 'C:\Windows\system32\cmd.exe') 
        screen = QApplication.primaryScreen() 
        img = screen.grabWindow(hwnd).toImage() 
        img.save(join(expanduser("~"),"teamviewer_sreenshot.png"))
    @pyqtSlot()    
    def on_pb_send_mail_clicked(self):
        #设置smtplib所需的参数
        #下面的发件人，收件人是用于邮件传输的。
#         username = 'bkdwei@163.com'
#         password='Free2009+'
#         sender='bkdwei@163.com'
#         receiver=['bkdwei@qq.com']
        username = get_option_value("username")
        password=get_option_value("password")
        sender=username
        receiver=[get_option_value("receiver")]
        
        subject = 'teamviewer远程截图 by Python'
        #通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
        #subject = '中文标题'
        #subject=Header(subject, 'utf-8').encode()
            
        #构造邮件对象MIMEMultipart对象
        #下面的主题，发件人，收件人，日期是显示在邮件页面上的。
        msg = MIMEMultipart('related') 
        msg['Subject'] = subject
        msg['From'] = 'bkdwei@163.com <bkdwei@163.com>'
        #msg['To'] = 'XXX@126.com'
        #收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
        msg['To'] = ";".join(receiver) 
        #msg['Date']='2012-3-16'
        
        #构造文字内容   
        body = "这是teamviewer的远程桌面截图<br><img src='cid:0' title='teamviewer_sreenshot' />" 
           
        body_html = MIMEText(body,'html', 'utf-8')    
        msg.attach(body_html)    
        
        #构造图片链接
        sendimagefile=open(join(expanduser("~"),"teamviewer_sreenshot.png"),'rb')
        image = MIMEImage(sendimagefile.read())
        sendimagefile.close()
        image.add_header('Content-ID','<0>')
        image.add_header('X-Attachment-Id', '0')
        image["Content-Disposition"] = 'attachment; filename="teamviewer_sreenshot.png"'
        msg.attach(image)
        
        #构造html
        #发送正文中的图片:由于包含未被许可的信息，网易邮箱定义为垃圾邮件，报554 DT:SPM ：<p><img src="cid:image1"></p>
        html = """
        <html>  
          <head></head>  
          <body>  
            <p>Hi!<br>  
               How are you?<br>  
               Here is the <a href="http://www.baidu.com">link</a> you wanted.<br> 
            </p> 
          </body>  
        </html>  
        """    
        text_html = MIMEText(html,'html', 'utf-8')
        text_html["Content-Disposition"] = 'attachment; filename="texthtml.html"'   
#         msg.attach(text_html)    
        
        #发送邮件
        smtp = smtplib.SMTP()    
        smtp.connect('smtp.163.com')
        #我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
        #smtp.set_debuglevel(1)  
        smtp.login(username, password)    
        smtp.sendmail(sender, receiver, msg.as_string())    
        smtp.quit()
        print("邮件发送成功")
    def auto_run(self):
        print("20秒后系统自动执行")
        time.sleep(20)
        print("启动teamviewer")
        self.on_pb_start_teamwiewer_clicked()
        time.sleep(60)
        print("开始截图")
        self.on_pb_take_screenshot_clicked()
        time.sleep(10)
        print("发送邮件")
        self.on_pb_send_mail_clicked()
        print("程序自动退出")
        sys.exit()
def main():
    app = QApplication(sys.argv)
    win = kdAutoTeamviewer()
    win.show()
    t = threading.Thread(target=win.auto_run)
    t.setDaemon(True)
    t.start()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()