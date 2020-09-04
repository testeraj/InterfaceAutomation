# InterfaceAutomation
matters need attention
1.基于pytest和allure的接口测试框架，需安装allure并添加allure到环境变量PATH中(allure依赖jdk)
2.先安装第三库，项目所有依赖库都在requirements.txt内 (pip install requirements.txt -i https://pypi.doubanio.com/simple)
3.使用excel维护接口(casedata.xlsx)
4.mysql，excel路径，邮箱信息以及接口url都在config.yaml中设置
explain
1.common目录:
    encryption.py    对字符串加密(支持md5，base64)
    excel.py    对excel进行读写，readonly读取excel中除第一行外的所有数据
    log.py      包含LogManage装饰器以及LogRecord类，生成Logs目录以及日志文件       
    mysqldb.py   连接MySQL数据库，基本的增删查改
    readdata.py     读取config.yaml文件以及excel中的数据    
    request.py        对requests库进行封装，网络请求
    sendmails.py     发送邮件，将pytest生成的测试报告(report.html)发送至指定邮箱 
2.conftest.py:
    control: 项目的前置和后置操作，返回日志对象，数据库对象以及request类
    login: 返回登录的token给调用方，用于需要登录的接口