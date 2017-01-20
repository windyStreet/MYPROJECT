#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import os
import sys
import time
import getopt
import JsonFileFunc
import FormatPrint
import platform

def isWindowsSystem():
    return 'Windows' in platform.system()
def isLinuxSystem():
    return 'Linux' in platform.system()

projectName = None


# 设置更新时间
def setUpdateTime(projectName, filePath):
    JsonFileFunc.readFile(filePath)
    updateInfo = JsonFileFunc.readFile(filePath)
    if updateInfo is None:
        FormatPrint.printFalat("未找到项目信息,退出")
    else:
        updateInfo[str(projectName)]["updateTime"] = time.strftime('%Y%m%d')
    JsonFileFunc.createFile(filePath, updateInfo)


def getLastVersionUpdateTime(projectName, updateVersion):
    versionRecordPath = sys.path[0] + os.sep + 'runtime' + os.sep + 'versionRecord.json'
    versionInfo = JsonFileFunc.readFile(versionRecordPath)
    if versionInfo is None:
        return None
    if int(float(updateVersion)) == float(updateVersion):
        return None
    updateVersion = float(updateVersion) - 0.001
    floatVersion = str("%.3f" % float(updateVersion)).split(".")[1]
    intVersion = str(int(float(updateVersion)))
    updateTime = versionInfo[projectName][intVersion][floatVersion]
    return updateTime


def recordUpdateVersion(projectName, updateVersion, updateTime):
    versionRecordPath = sys.path[0] + os.sep + 'runtime' + os.sep + 'versionRecord.json'
    versionInfo = JsonFileFunc.readFile(versionRecordPath)
    floatVersion = "000"
    if int(float(updateVersion)) == float(updateVersion):
        pass
    else:
        floatVersion = str(updateVersion).split(".")[1]
    intVersion = str(int(float(updateVersion)))

    if versionInfo is None:
        versionInfo = {}

    new_floatVersionInfo = {floatVersion: updateTime}
    new_intVersion = {intVersion: new_floatVersionInfo}
    new_versionInfo = {projectName: new_intVersion}

    if versionInfo is None:
        versionInfo = new_versionInfo
    elif projectName not in versionInfo.keys():
        versionInfo[projectName] = new_intVersion
    elif intVersion not in versionInfo[projectName].keys():
        versionInfo[projectName][intVersion] = new_floatVersionInfo
    else:
        versionInfo[projectName][intVersion][floatVersion] = updateTime
    JsonFileFunc.createFile(versionRecordPath, versionInfo)


# 平台更新项目备份
def platformbackup():
    backupShellPath = sys.path[0] + os.sep + 'shell' + os.sep + 'projectbackup.sh'
    filePath=""
    if isWindowsSystem():
        filePath = "X:/project_update/platformupdate/updateInfo.json"
    elif isLinuxSystem():
        filePath = "/data/smbshare/project_update/platformupdate/updateInfo.json"
    # 设置更新时间
    setUpdateTime(projectName, filePath)
    updateInfo = JsonFileFunc.readFile(filePath)
    command = ""
    if updateInfo is None:
        FormatPrint.printFalat("未找到项目信息,退出")
    else:
        updateVersion = updateInfo[str(projectName)]["updateVersion"]
        updateTime = updateInfo[str(projectName)]["updateTime"]
        try:
            if int(float(updateVersion)) == float(updateVersion):
                # 全量更新
                updatetype = "full"
                command = backupShellPath + " -m update -P " + str(projectName).upper() + " -v " + str(
                    updateVersion) + " -t " + str(updateTime) + " -T  " + str(updatetype)
            else:
                # 增量更新
                updatetype = "add"
                orginTime = getLastVersionUpdateTime(projectName, updateVersion)
                if orginTime is None:
                    FormatPrint.printError("未读取到增量更新信息")
                    FormatPrint.printFalat("未读取到增量更新信息,退出")
                command = backupShellPath + " -m update -P " + str(projectName).upper() + " -v " + str(
                    updateVersion) + " -t " + str(updateTime) + " -T  " + str(updatetype) + " -o " + str(orginTime)
        except Exception as e:
            FormatPrint.printError("读取到错误的版本信息:" + str(e))
            FormatPrint.printFalat("读取到错误的版本信息,退出")
        # -m update -P YXYBB -v 203 -t 20150623 -T add
        # -m update -P YXYBB -v 203.003 -t 20150623 -T add -o 20150621
        recordUpdateVersion(projectName, updateVersion, updateTime)
        FormatPrint.printInfo("执行命令" + str(command))
        if os.system(command) is 0:
            FormatPrint.printInfo(str(projectName) + str(updateVersion) + "备份项目成功")
        else:
            FormatPrint.printInfo(str(projectName) + str(updateVersion) + "备份项目失败")
            FormatPrint.printFalat(str(projectName) + str(updateVersion) + "备份项目失败,退出")


def help():
    print (
        "-m:,--method=,will be run method:help|platformbackup")
    print ("-h,--help")
    print ("-P:,--Project=,project name")
    # print ("-u:,--update=,specify update project name")


if __name__ == '__main__':
    method = None
    projectName = None

    operator = \
        {
            'platformbackup': platformbackup,
            'help': help
        }
    # options, args = getopt.getopt(sys.argv[1:], "hu:",["help", "update="])
    options, args = getopt.getopt(sys.argv[1:], "hm:P:", ["help", "Project"])

    if len(options) <= 0:
        if method is not None:
            print ("已经指定方法，请使用正确方法")
        else:
            method = "help"
    else:
        for name, value in options:
            if name in ['-h', '--help']:
                if method is not None:
                    print ("已经指定方法，请使用正确方法")
                    sys.exit(1)
                else:
                    method = "help"
            elif name in ['-m', '--method=']:
                if value is None or str(value).startswith("-"):
                    FormatPrint.printInfo("-m:--method需要参数method")
                    sys.exit(1)
                method = value
            elif name in ['-P', '--Project=']:
                if value is None or str(value).startswith("-"):
                    print ("-P:--Project需要参数projectname")
                    sys.exit(1)
                projectName = value
    operator.get(method)()
