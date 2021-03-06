#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import FormatPrint
import os


class ResourceFunc(object):
    def __init__(self):
        pass


'''
 资源替换,通过执行参数
 par:pu{
    "updateTime":xxxx
    "updateVersion":xxx
    "projectname":{
        "projectName_xxx":{
            "willUpdateGroup_xxx":{
                "tomcatresourceupdatescriptpath":xxx
            }
        }
    }
 }
功能实现，实现项目资源的替换（lib，ResoutceLib，staticResource）
备注：脚本执行成功时返回0，脚本执行错误中断更新
'''


def replceResource(pu):
    tomcat_conf = pu.tomcatConf
    command = tomcat_conf['projectname'][pu.projectName][pu.willUpdateGroup[0]][
                  'tomcatresourceupdatescriptpath'] + " " + str(pu.updateVersion) + " " + str(pu.updateTime)
    FormatPrint.printInfo("执行资源替换脚本:" + str(command))
    if os.system(command) == 0:
        FormatPrint.printInfo("replace resource sucess ")
        return True
    else:
        FormatPrint.printInfo("replace resource fail ")
        return False
