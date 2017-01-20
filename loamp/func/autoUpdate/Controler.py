#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import projectupdate
import FormatPrint
import getopt
import sys
import TomcatFunc
import HealthCheck
import platformFunc
import MailFunc


class Controler(object):
    def __init__(self):
        pass


method = None
projectName = None
projectVersion = None
tomcatTag = None
path = None
command = None
time = None


# 更新邮件配置信息
# -m updateMailConf  -P insy
def updateMailConf():
    FormatPrint.printDebug("更新邮件配置信息")
    MailFunc.updateMailConf(projectName)


# 平台项目更新
# -m platformupdate  -P insy
def platformupdate():
    FormatPrint.printInfo("平台更新" + str(projectName))
    stopHealthCheck()  # 关闭健康检查
    restartProject()  # 重启项目
    startHealthCheck()  # 启动健康检查

#平台发送邮件
def platformSendMail():
    updateInfo = platformFunc.getUpdateInfo(projectName)
    projectVersion = updateInfo.updateVersion
    subject = str(projectName) + "项目" + str(projectVersion) + "版本更新"
    messages = str(projectName) + "项目" + str(projectVersion) + "版本更新,成功"
    level = 50  # 发送给所有人
    MailFunc.sendMails(projectName,subject, messages, level)

# 删除更新信息
def platformDelUpdateFile():
    platformFunc.delUpdateFile()


# 平台资源替换
def platformReplaceResource():
    FormatPrint.printInfo("平台更新替换资源" + str(projectName))
    updateInfo = platformFunc.getUpdateInfo(projectName)
    time = updateInfo.updateTime
    projectVersion = updateInfo.updateVersion
    projectupdate.replaceResource(projectName, projectVersion, time)


# 资源替换
def replaceResource():
    FormatPrint.printInfo("更新替换资源" + str(projectName) + "替换版本" + str(projectVersion))
    projectupdate.replaceResource(projectName, projectVersion, time)


# 项目更新
def update():
    FormatPrint.printInfo("更新" + str(projectName) + "更新版本" + str(projectVersion))
    replaceResource()  # 替换资源
    stopHealthCheck()  # 关闭健康检查
    updateProject()  # 更新项目
    startHealthCheck()  # 启动健康检查

# 项目回滚
def rollback():
    FormatPrint.printInfo("更新回滚" + str(projectName) + "回滚版本" + str(projectVersion))
    replaceResource()  # 替换资源
    stopHealthCheck()  # 关闭健康检查
    updateProject()  # 更新项目
    startHealthCheck()  # 启动健康检查


# 更新项目
def updateProject():
    FormatPrint.printInfo("项目更新" + str(projectName))
    projectupdate.updateProject(projectName)


# 重启项目
def restartProject():
    FormatPrint.printInfo("重启项目" + str(projectName))
    projectupdate.restartProject(projectName)


# 启动tomcat
def startTomcat():
    FormatPrint.printDebug("startTomcat")
    FormatPrint.printInfo("启动tocmat" + str(tomcatTag))
    TomcatFunc.startTomcat(path, tomcatTag)


# 关闭tomcat
def tomatKill():
    FormatPrint.printDebug("tomatKill")
    FormatPrint.printInfo("关闭tocmat" + str(tomcatTag))
    TomcatFunc.killTomcat(path, tomcatTag)


# 启动健康检查服务
def startHealthCheck():
    FormatPrint.printDebug("startHealCheck")
    if HealthCheck.startHealthCheck(projectName):
        FormatPrint.printInfo("启动健康检查服务成功")
    else:
        FormatPrint.printInfo("启动健康检查服务失败")


# 关闭健康检查服务
def stopHealthCheck():
    FormatPrint.printDebug("stopHealthCheck")
    if HealthCheck.stopHealthCheck(projectName):
        FormatPrint.printInfo("关闭健康检查服务成功")
    else:
        FormatPrint.printInfo("关闭健康检查服务失败")


# 重启健康检查服务
def restartHealthCheck():
    FormatPrint.printDebug("restartHealthCheck")
    if HealthCheck.restartHealthCheck(projectName):
        FormatPrint.printInfo("重启健康检查服务成功")
    else:
        FormatPrint.printInfo("重启健康检查服务失败")


# 一次性健康检查服务
def healthCheckOnce():
    FormatPrint.printDebug("startHealthCheckOnce")
    if HealthCheck.checkOnce(projectName):
        FormatPrint.printInfo("一次性健康检查服务成功")
    else:
        FormatPrint.printInfo("一次性健康检查服务失败")


# 多次性健康检查服务
def healthCheckAll():
    FormatPrint.printDebug("healthCheckAll")
    if HealthCheck.checkAllTime(projectName):
        FormatPrint.printInfo("多次性健康检查服务成功")
    else:
        FormatPrint.printInfo("多次性健康检查服务失败")


def healthCheckStatus():
    FormatPrint.printDebug("healthCheckStatus")
    HealthCheck.healthCheckStatus(projectName)


# 帮助
def help():
    print ("-h,--help")
    print (
        "-m:,--method=,will be run method:platformReplaceResource|platformupdate|platformSendMail|platformDelUpdateFile|update|updateMailConf|rollBack|starttomcat|killtomcat|startHealthCheck|stopHealthCheck|restartHealthCheck|healthCheckOnce|healthCheckAll|healthCheckStatus")
    print ("-u:,--update=,specify update project name")
    print ("-r:,--roolback=,specify roolback project name")
    print ("-v:,--version=,specify projectupdate version number")
    print ("-k:,--killtomcat=,specify close tomcattag")
    print ("-s:,--starttomcat=,specify start tomcattag ")
    print ("-p:,--path=,specify a detail path")
    print ("-c:,--command=,shell command")
    print ("-P:,--Project=,project name")
    print ("-t:,--Time=,project update time")


operator = \
    {
        'platformReplaceResource': platformReplaceResource,
        'platformupdate': platformupdate,
        'platformSendMail': platformSendMail,
        'platformDelUpdateFile': platformDelUpdateFile,
        'update': update,
        'rollback': rollback,
        'help': help,
        'starttomcat': startTomcat,
        'killtomcat': tomatKill,
        'startHealthCheck': startHealthCheck,
        'stopHealthCheck': stopHealthCheck,
        'restartHealthCheck': restartHealthCheck,
        'healthCheckOnce': healthCheckOnce,
        'healthCheckAll': healthCheckAll,
        'healthCheckStatus': healthCheckStatus,
        'replaceResource': replaceResource,
        'updateMailConf': updateMailConf
    }

options, args = getopt.getopt(sys.argv[1:], "hv:p:c:m:P:t:",
                              ["help", "version=", "path=", "command=", "method=", "Project=", "Time="])

# method = "help"
if len(options) <= 0:
    if method is not None:
        FormatPrint.printFalat("已经指定方法，请使用正确方法")
    else:
        method = "help"
else:
    for name, value in options:
        if name in ['-h', '--help']:
            if method is not None:
                FormatPrint.printFalat("已经指定方法，请使用正确方法")
            else:
                method = "help"
        elif name in ['-v', '--version=']:
            if value is None or str(value).startswith("-"):
                FormatPrint.printInfo("-v:--version需要参数projectVersion")
                sys.exit(1)
            projectVersion = value
        elif name in ['-p', '--path=']:
            if value is None or str(value).startswith("-"):
                FormatPrint.printInfo("-p:--path需要参数filepath")
                sys.exit(1)
            path = value
        elif name in ['-c', '--command=']:
            if value is None or str(value).startswith("-"):
                FormatPrint.printInfo("-c:--command需要参数command")
                sys.exit(1)
            command = value
        elif name in ['-m', '--method=']:
            if value is None or str(value).startswith("-"):
                FormatPrint.printInfo("-m:--method需要参数method")
                sys.exit(1)
            method = value
        elif name in ['-P', '--Project=']:
            if value is None or str(value).startswith("-"):
                FormatPrint.printInfo("-P:--Project需要参数projectname")
                sys.exit(1)
            projectName = value
        elif name in ['-t', '--Time=']:
            if value is None or str(value).startswith("-"):
                FormatPrint.printInfo("-t:--Time需要参数timestamp")
                sys.exit(1)
            time = value
        else:
            method = "help"
operator.get(method)()
