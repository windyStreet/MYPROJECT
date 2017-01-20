#!/usr/bin/env python
#!-*- coding:utf-8 -*-

import sys
import os

def writeFlile(path,line):
    with open(path, 'a+') as tmpfile:
        tmpfile.write(line)
def writeResultChecked(line):
    path = sys.path[0] + os.sep + "result" + os.sep + "result_checked.txt"
    writeFlile(path,line)

def writeResultUnchecked(line):
    path = sys.path[0] + os.sep + "result" + os.sep + "result_unchecked.txt"
    writeFlile(path, line)
def getSingle(checkedFile,todealFile):
    with open(checkedFile, 'r') as checked_file:
        with open(todealFile, 'r') as todeal_ile:
            for todealLine in todeal_ile:
                if todealLine in (checked_file):
                    writeResultChecked(todealLine)
                else:
                    writeResultUnchecked(todealLine)

if __name__ == '__main__':
    checkedFile = sys.path[0] + os.sep +"checked.txt"
    todealFile = sys.path[0] + os.sep +"todeal.txt"
    getSingle(checkedFile,todealFile);