#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import JsonFileFunc
import FormatPrint
import sys
import os
import time


class platformFunc(object):
    def __init__(self):
        self.projectName = None
        self.updateTime = None
        self.updateVersion = None
        self.updateMsg = None

    def __getUpdateTime__(self):
        return self.updateTime

    def __getUpdateVersion__(self):
        return self.updateVersion

    def __getUpdateInfo__(self):
        return self

    def __getUpdateMsg__(self):
        return self.updateMsg

    def __delUpdateFile__(self):
        orginFile = sys.path[0] + os.sep + 'files' + os.sep + 'updateInfo.json'
        if os.path.exists(orginFile):
            try:
                new_file = sys.path[0] + os.sep + 'files' + os.sep + time.strftime('%Y%m%d%H%M%S') + 'updateInfo.json'
                os.rename(orginFile, new_file)
            except Exception as e:
                FormatPrint.printError("删除 updateInfo.json 文件出错:" + str(e))
        else:
            FormatPrint.printFalat(" updateInfo.json 文件不存在")

    def __initUpdateInfo__(self, projectName):
        self.projectName = projectName
        path = sys.path[0] + os.sep + 'files' + os.sep + 'updateInfo.json'
        updateInfos = JsonFileFunc.readFile(path)
        if updateInfos is not None and updateInfos[projectName] is not None:
            updateInfo = updateInfos[projectName]
            self.updateMsg = updateInfo['updateMsg']
            self.updateVersion = updateInfo['updateVersion']
            self.updateTime = updateInfo['updateTime']
        else:
            FormatPrint.printFalat("can not get right updateinfo")


def getUpdateTime(projectName):
    pf = platformFunc()
    pf.__initUpdateInfo__(projectName)
    return pf.__getUpdateTime__()


def getUpdateVersion(projectName):
    pf = platformFunc()
    pf.__initUpdateInfo__(projectName)
    return pf.__getUpdateVersion__()


def delUpdateFile():
    pf = platformFunc()
    pf.__delUpdateFile__()


def getUpdateMsg(projectName):
    pf = platformFunc()
    pf.__initUpdateInfo__(projectName)
    return pf.__getUpdateMsg__()


def getUpdateInfo(projectName):
    pf = platformFunc()
    pf.__initUpdateInfo__(projectName)
    return pf.__getUpdateInfo__()
