#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import JsonFileFunc
import sys
import os
import FormatPrint


class MailFunc(object):
    def __init__(self):
        self.mailConf = None
        self.message = None
        self.subject = None
        self.sendLevel = None  # 发送等级
        self.senderMailAccount = None  # 发送者邮箱账户
        self.senderMailName = None  # 发送者名称
        self.senderMailPassword = None  # 发送者邮箱账户密码
        self.SMTPName = None  # SMTP 名称
        self.SMTPPort = None  # SMTP 端口

    # 发送邮件
    def sendMail(self):
        msg = MIMEText(self.message, 'plain', 'utf-8')
        receiverAccounts = []
        receiverNames = []
        for receiverInfo in self.mailConf['receiver']:
            if str(receiverInfo['level']) < str(self.sendLevel):
                receiverAccounts.append(receiverInfo['email'])
                receiverNames.append(str(receiverInfo['name']))

        receiverAccounts = list(set(receiverAccounts))
        receiverNames = list(set(receiverNames))
        receiverNamesStr = "【" + ",".join(receiverNames) + "】"

        msg['From'] = formataddr([self.senderMailName, self.senderMailAccount])  # 显示发件人信息
        msg['To'] = ";".join(receiverAccounts)  # 显示收件人信息
        msg['Subject'] = self.subject  # 定义邮件主题
        try:
            # 创建SMTP对象
            server = smtplib.SMTP(self.SMTPName, int(self.SMTPPort))
            # server.set_debuglevel(1)  # 可以打印出和SMTP服务器交互的所有信息
            # login()方法用来登录SMTP服务器
            server.login(self.senderMailAccount, self.senderMailPassword)
            # sendmail()方法就是发邮件，由于可以一次发给多个人，所以传入一个list，邮件正文是一个str，as_string()把MIMEText对象变成str

            if len(receiverAccounts) <= 0:
                FormatPrint.printInfo("未找到可以发送邮件的对象")
            else:
                server.sendmail(self.senderMailAccount, receiverAccounts, msg.as_string())
                FormatPrint.printInfo("标题为《" + str(self.subject) + "》的邮件已发送至" + receiverNamesStr + "的邮箱!")
            server.quit()
        except smtplib.SMTPException as e:
            FormatPrint.printError("无法发送邮件" + str(e))

    # 初始化邮箱配置
    def initMailConf(self, projectName):
        mailConfPath = sys.path[0] + os.sep + 'conf' + os.sep + str(projectName) + '_mail-conf.json'
        mailConfInfo = JsonFileFunc.readFile(mailConfPath)
        if mailConfInfo is None:
            FormatPrint.printError("mail-conf.json file is not exist")
            FormatPrint.printFalat("mail-conf.json file is not exist,exit!")
        else:
            self.mailConf = mailConfInfo  # 配置信息
            self.senderMailAccount = mailConfInfo['SMTP']['senderMailAccount']  # 发送者邮箱账户
            self.senderMailName = mailConfInfo['SMTP']['senderMailName']  # 发送者名称
            self.senderMailPassword = mailConfInfo['SMTP']['senderMailPassword']  # 发送者邮箱账户密码
            self.SMTPName = mailConfInfo['SMTP']['name']  # SMTP 名称
            self.SMTPPort = mailConfInfo['SMTP']['port']  # SMTP 端口

    # 发送邮件定义
    def sendMails(self, subject, messages, level):
        self.subject = subject
        self.message = messages
        self.sendLevel = level
        self.sendMail()

    # 更新邮件配置文件
    def updateMailConf(self, projectName):
        updateInfoFile = sys.path[0] + os.sep + 'files' + os.sep + 'mailconf.json'
        updateInfo = JsonFileFunc.readFile(updateInfoFile)
        if updateInfo is None:
            FormatPrint.printError("初始化 mail 配置文件错误")
            FormatPrint.printFalat("初始化 mail 配置文件错误,退出")
        else:
            mailConPath = sys.path[0] + os.sep + 'conf' + os.sep + str(projectName) + '_mail-conf.json'
            updateMailInfo = updateInfo[projectName]
            JsonFileFunc.createFile(mailConPath, updateMailInfo)


# 发送邮件接口
def sendMails(projectName, subject, messages, level):
    MF = MailFunc()
    MF.initMailConf(projectName)
    MF.sendMails(subject, messages, level)


# 更新邮件配置
def updateMailConf(projectName):
    MF = MailFunc()
    MF.updateMailConf(projectName)
