#!/usr/bin/env python
#!-*- coding:utf-8 -*-
import FormatPrint
import psycopg2
import sys
import os
import json

#之前备份的数据库
# pagesize = 50000
# old_DBINFO={
#     "dbname":"testrestoreperson",
#     "dbhost":"10.0.0.31",
#     "dbport":"5432",
#     "dbuser":"postgres",
#     "dbpassword":"Yxybbdb2015"
# }
# #现在运行的数据库
# new_DBINFO={
#     "dbname":"lsipperson",
#     "dbhost":"10.0.0.31",
#     "dbport":"5432",
#     "dbuser":"postgres",
#     "dbpassword":"Yxybbdb2015"
# }

pagesize = 10
old_DBINFO={
    "dbname":"testrestoreperson",
    "dbhost":"10.0.0.31",
    "dbport":"5432",
    "dbuser":"postgres",
    "dbpassword":"Yxybbdb2015"
}
#现在运行的数据库
new_DBINFO={
    "dbname":"lsipperson",
    "dbhost":"10.0.0.31",
    "dbport":"5432",
    "dbuser":"postgres",
    "dbpassword":"Yxybbdb2015"
}

#修改数据
'''
1、读取new_DBINFO  中指定的几个数据表中的指定数据
2、读取一个表中的数据，将数据写入文件中
3、读取文件，查询 old_DBINFO 中的数据（指定需要更新的字段）
4、更新 new_DBINFO 中的数据 ，同时写入到另外一个文件中（包括执行结果）
5、重复上述1234操作
'''
#第一步，列出需要修改的数据，写入文本中
def createNeedModifyDataFiles(tablenames):
    FormatPrint.printInfo("开始person数据修改")
    for tablename in tablenames:
        conditon = " email is null and mobile is null "
        COUNTSQL = "select count(*) from " + tablename + " where " + conditon
        countResult = DB_selectOne(new_DBINFO,COUNTSQL)
        FormatPrint.printInfo(str(tablename)+"表共计"+str(countResult[0])+"条数据")
        pageCount = getPageCount(countResult[0])
        for pagenum in range(0,pageCount):
            returnfields = ['id', 'cardno','nickname']
            returnFieldsStr = ","
            returnFieldsStr = returnFieldsStr.join(returnfields)
            limt = str(pagesize)
            offset = str(pagenum * pagesize)
            conditon = " email is null and mobile is null limit " + limt + " offset " + offset
            new_search_SQL = "select " + str(returnFieldsStr) + " " + str(tablename) + " from " + str(tablename) + " where " + str(conditon)
            new_search_result = DB_select(new_DBINFO,new_search_SQL)
            jsonData = dealToJSONStr(returnfields,new_search_result)
            new_search_fileName = sys.path[0] + os.sep + "toDoFiles" + os.sep + str(tablename) + "-" + str(offset) + "-data.txt"
            productDataFile(new_search_fileName,jsonData)


#第二步，获取到能够修改的数据，写入文本中
def dealNeedModifyData():
    files = os.listdir(sys.path[0] + os.sep + "toDoFiles")
    for fileName in files:
        FormatPrint.printInfo(fileName)
        filePath = sys.path[0] + os.sep + "toDoFiles" + os.sep + str(fileName)
        tableName = fileName.split("-")[0]
        FormatPrint.printInfo(tableName)
        fopen = open(filePath, 'r')  # r 代表read
        for eachLine in fopen:
            eachLine = eachLine.replace("\n", "")
            jo = json.loads(eachLine)
            returnfields = ['id', 'cardno','email','mobile']
            returnFieldsStr = ","
            returnFieldsStr = returnFieldsStr.join(returnfields)
            conditon = " id = '"+jo['id']+"' ;"
            old_search_SQL = "select " + returnFieldsStr + " from "+ tableName + " where " + conditon

            old_search_result = DB_select(old_DBINFO,old_search_SQL)
            if len(old_search_result) <= 0:
                old_error_search_fileName = sys.path[0] + os.sep + "resultErrorFiles" + os.sep + str(fileName)
                productDataFile(old_error_search_fileName, eachLine+"\n", "add")
            else:
                jsonData = dealToJSONStr(returnfields, old_search_result)
                old_search_fileName = sys.path[0] + os.sep + "resultFiles" + os.sep + str(fileName)
                productDataFile(old_search_fileName, jsonData, "add")
        fopen.close()

#第三步，修改数据，写入文本中
def updateNeedModifyData():
    files = os.listdir(sys.path[0] + os.sep + "resultFiles")
    for fileName in files:
        FormatPrint.printInfo(fileName)
        filePath = sys.path[0] + os.sep + "resultFiles" + os.sep + str(fileName)
	print (filePath)
        tableName = fileName.split("-")[0]
        FormatPrint.printInfo(tableName)
        fopen = open(filePath, 'r')  # r 代表read
        for eachLine in fopen:
	    try:
		eachLine = eachLine.replace("\n", "")
                jo = json.loads(eachLine)
                if  jo['email']  == None:
                    email = "null"
	        else:
                    email = "'"+str(jo['email'])+"'"
                if jo['mobile']  == None:
                    mobile = "null"
                else:
                    mobile = str(jo['mobile'])
                    print ('mobile is :'+ mobile)
                    mobile = "'"+str(jo['mobile'])+"'"

                UpdataSQL = "update " + tableName + " set email = " + email + ", mobile = " + mobile + " where id = '" + jo['id'] + "' returning id ;"
                #update_SQL_fileName = sys.path[0] + os.sep + "updateSQLFiles" + os.sep + str(fileName)
                #productDataFile(update_SQL_fileName, UpdataSQL, "str")


                update_result = DB_update(new_DBINFO,UpdataSQL)
                jo["updateSQL"] = UpdataSQL
                if update_result != None:
                    jo["updateresult"] = "update sucess"
                    resultStr = json.dumps(jo) + "\n"
                    update_result_fileName = sys.path[0] + os.sep + "updateResultFiles" + os.sep + str(fileName)
                    productDataFile(update_result_fileName, resultStr, "add")
                else:
                    jo["updateresult"] = "update fail"
                    resultStr = json.dumps(jo) + "\n"
                    update_error_result_fileName = sys.path[0] + os.sep + "updateRrrorResultFiles" + os.sep + str(fileName)
                    productDataFile(update_error_result_fileName, resultStr, "add")

	    except Exception as e:
                jo["updateresult"] = "update fail"
                resultStr = json.dumps(jo) + "\n"
                update_chinese_error_result_fileName = sys.path[0] + os.sep + "updateRrrorResultFiles" + os.sep + "chineseErrorSQL.txt"
                productDataFile(update_chinese_error_result_fileName, resultStr, "add")

        fopen.close()



#将数据处理成json格式
def dealToJSONStr(fields,rows):
    exportStrs = ""
    for row in rows:
        toDealData={}
        for index in range(0, len(fields)):
            toDealData[fields[index]] = str(row[index])
        needExportStr = json.dumps(toDealData)+"\n"
        exportStrs += needExportStr
    return exportStrs
#
def productDataFile(file,data,type="default"):
    #encoding
    if type == "default":
        with open(file, 'w') as tmpfile:
            tmpfile.write(data)
    elif type == "add":
        with open(file, 'a+') as tmpfile:
            tmpfile.write(data)
    elif type == "str":
        with open(file, 'a+') as tmpfile:
            tmpfile.write(data+"\n")
    else:
        FormatPrint.printFalat("error parms ")

#获取分页
def getPageCount(count):
    if int(count) % int(pagesize) == 0:
        return int(int(count)/int(pagesize))
    else:
        return int(int(count)/int(pagesize)+1)

#查询
def DB_selectOne(DBINFO,sql):
    FormatPrint.printDebug("exec SQL : "+str(sql))
    conn = None
    try:
        conn = psycopg2.connect(database=DBINFO['dbname'], user=DBINFO['dbuser'], password=DBINFO['dbpassword'],host=DBINFO['dbhost'], port=DBINFO['dbport'])
        cursor = conn.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        return row
    finally:
        if conn:
            conn.close()

#查询多条
def DB_select(DBINFO,sql):
    FormatPrint.printDebug("exec SQL : "+str(sql))
    conn = None
    try:
        conn = psycopg2.connect(database=DBINFO['dbname'], user=DBINFO['dbuser'], password=DBINFO['dbpassword'],host=DBINFO['dbhost'], port=DBINFO['dbport'])
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows
    finally:
        if conn:
            conn.close()
#更新
def DB_update(DBINFO,sql):
    FormatPrint.printDebug("exec SQL : " + str(sql))
    conn = None
    try:
        conn = psycopg2.connect(database=DBINFO['dbname'], user=DBINFO['dbuser'], password=DBINFO['dbpassword'],host=DBINFO['dbhost'], port=DBINFO['dbport'])
        cursor = conn.cursor()
        cursor.execute(sql)
	conn.commit()
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        FormatPrint.printError(str(DBINFO)+"\n"+str(sql))
        FormatPrint.printError(str(e))
        return None
    finally:
        if conn:
            conn.close()

#记录
def DB_record():
    pass

if __name__ == '__main__':
    tableNames = ['person4100',"person5001"]
    createNeedModifyDataFiles(tableNames)
    FormatPrint.printInfo("######################setp1############################")
    dealNeedModifyData()
    FormatPrint.printInfo("######################setp2############################")
    updateNeedModifyData()
    FormatPrint.printInfo("######################setp3############################")
