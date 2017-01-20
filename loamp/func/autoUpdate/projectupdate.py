#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import sys
import os
import FormatPrint
import JsonFileFunc
import __projectupdate_double
import __projectupdate_onehalf
import __projectupdate_single
import RungroupFunc
import ResourceFunc


class ProjectUpdate(object):
    def __init__(self):
        self.projectName = None
        self.updateVersion = None
        self.updateTime = None
        self.updateType = None
        self.deploymentmode = None
        self.tomcatConf = None
        self.hostInfostr = None
        self.willUpdateGroup = []


def replaceResource(projectName, updateVersion, updateTime):
    update(projectName, updateVersion, "replaceResource", updateTime)


def restartProject(projectName, updateVersion=None, updateTime=None):
    update(projectName, updateVersion, "restartProject", updateTime)


def updateProject(projectName, updateVersion=None, updateTime=None):
    update(projectName, updateVersion, "update", updateTime)


def update(projectName, updateVersion, updateType, updateTime):
    pu = ProjectUpdate()
    pu.projectName = projectName
    pu.updateVersion = updateVersion
    pu.updateType = updateType
    pu.updateTime = updateTime
    pu.willUpdateGroup = []

    confPath = sys.path[0] + os.sep + 'conf' + os.sep + 'tomcat-conf.json'
    pu.tomcatConf = JsonFileFunc.readFile(confPath)
    if pu.tomcatConf is None:
        FormatPrint.printFalat('can not read tomcat-conf configure')
    if pu.projectName not in pu.tomcatConf['projectname']:
        FormatPrint.printFalat(str(pu.projectName) + ' not configure in the tomcat-conf.json')
    pu.deploymentmode = pu.tomcatConf['projectname'][projectName]['deploymentmode']
    pu.hostInfostr = str(pu.tomcatConf['hostname']) + ":" + str(pu.tomcatConf['serverip'])

    if pu.deploymentmode == 'single':  # 单个模式
        FormatPrint.printDebug("curent project is single deploymentmode")
        pu.willUpdateGroup.append("groupmaster")

        if updateType == 'replaceResource':
            ResourceFunc.replceResource(pu)
        elif updateType == 'restartProject':
            __projectupdate_single.restartProject(pu)
        elif updateType == 'update':
            __projectupdate_single.restartProject(pu)
        else:
            pass
    elif pu.deploymentmode == 'onehalf':  # 半启动模式
        pu.willUpdateGroup.append("groupmaster")
        pu.willUpdateGroup.append("groupbackup")
        FormatPrint.printDebug("curent project is onehalf deploymentmode")

        if updateType == 'replaceResource':
            ResourceFunc.replceResource(pu)
        elif updateType == 'restartProject':
            __projectupdate_onehalf.restartProject(pu)
        elif updateType == 'update':
            __projectupdate_onehalf.restartProject(pu)
        else:
            pass
    elif pu.deploymentmode == 'double':  # 主备组模式
        FormatPrint.printDebug("curent project is double deploymentmode")
        currentRunGroup = RungroupFunc.getRunGroupName(pu.projectName)[0]
        if currentRunGroup == "groupmaster":
            pu.willUpdateGroup.append("groupbackup")
        elif currentRunGroup == "groupbackup":
            pu.willUpdateGroup.append("groupmaster")
        else:
            FormatPrint.printFalat(" can not get the will update group , please check config ")

        if updateType == 'replaceResource':
            ResourceFunc.replceResource(pu)
        elif updateType == 'restartProject':
            __projectupdate_double.restartProject(pu)
        elif updateType == 'update':
            __projectupdate_double.restartProject(pu)
        else:
            pass
    else:
        FormatPrint.printFalat(str(pu.projectName) + 'project configure wrong deploymentmode ')
