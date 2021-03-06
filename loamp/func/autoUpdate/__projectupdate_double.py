#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import FormatPrint
import TomcatFunc
import NginxFunc
import __checkServiceIsOK
import NodeRunStatusFunc


class __projectupdate_double(object):
    def __init__(self):
        self.hostInfostr = None
        self.projectJson = None
        self.projectName = None
        self.updateVersion = None
        self.updateTime = None
        self.updateType = None
        self.deploymentmode = None
        self.willUpdateGroup = []
        self.sucessRestartTomcatTags = []


'''
    A、关闭健康检查服务
    B、读取配置文件
        1、判断当前运行组
        D、替换资源
        2、替换将被更新组配置的项目
    E、重启tomcat
        1、判断当前运行组
        2、重启将被更新组的tomcat
    F、启动健康检查服务
'''


# 功能实现函数
def restartProject(projectJson):
    __pud = __projectupdate_double()
    __pud.projectJson = projectJson
    __pud.hostInfostr = projectJson.hostInfostr
    __pud.projectName = projectJson.projectName
    __pud.updateVersion = projectJson.updateVersion
    __pud.updateTime = projectJson.updateTime
    __pud.updateType = projectJson.updateType
    __pud.deploymentmode = projectJson.deploymentmode
    __pud.willUpdateGroup = projectJson.willUpdateGroup

    if TomcatFunc.restartWillUpdateTomcatGroup(__pud):
        __pud.sucessRestartTomcatTags = __checkServiceIsOK.checkServiceIsOk(__pud)
        if len(__pud.sucessRestartTomcatTags) > 0:
            if NodeRunStatusFunc.initNodeHealthStatus(__pud, __pud.willUpdateGroup):
                if NginxFunc.changeNginxConf(__pud.projectName, __pud.sucessRestartTomcatTags, "update"):
                    FormatPrint.printInfo(" update finish ")
                else:
                    FormatPrint.printError(" modifu Nginx error ")
            else:
                FormatPrint.printFalat(" modify runtime file fail ")
        else:
            FormatPrint.printFalat(" service is not available ")
    else:
        FormatPrint.printFalat(" restart tomcat fail ")
