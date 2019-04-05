# kdAutoTeamviewer
一个自动控制脚本，开机自动启动teamviewer，自动截图，并将截图发送到指定邮箱

# 截图
![截图](/screenshot/screenshot.png)

# 安装
- 安装python3和pip，[安装包地址](https://www.python.org/downloads/)
- 使用pip安装kdAutoTeamviewer，命令
> pip install kdAutoTeamviewer
- 你也可以使用[kdPythonInstaller(https://github.com/bkdwei/kdPythonInstaller/releases/download/v1.0.0/kdPythonInstaller-1.0.0.exe/) 来安装python和kdAutoTeamviewer

# 使用方式
- 在主目录（比如C:\Users\bkd\）新建kdAutoTeamviewer.ini配置文件，并写入自己邮箱的用户名和密码，以及接收截图的邮箱。

>[global]

>username = abc@163.com

>password = 123

>receiver =edf@qq.com

- 将teamviewer.exe的快捷方式teamviewer.exe.lnk放到主目录
- 将桌面的启动脚本放到系统的启动目录(在开始-启动，比如C:\Users\bkd\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup），
- 系统开机后，就会自动启动teamviewer，自动截图，并将截图发送到指定邮箱
