import sys
import os

cn_mobile = [134, 135, 136, 137, 138, 139, 150, 151, 152, 157, 158, 159, 182, 183, 184, 187, 188, 147, 178, 1705]
cn_union = [130, 131, 132, 155, 156, 185,186, 145, 176, 1709]
cn_telecom = [133, 153, 180, 181, 189, 177, 1700]

def len_num(your_number):

    if len(your_number) == 11:
        return 1
    else:
        return 0

def getMobile(num):
    rightMobieTxt = sys.path[0] + os.sep + 'rightMobile.txt'
    errorMobieTxt = sys.path[0] + os.sep + 'errorMobile.txt'
    result = None
    nums = str(num).replace("\"","").replace("\n","")

    #规则一
    mobiles = str(num).replace("\"","").replace("\n", "").split("\\")[0]
    for mobile in mobiles.split(" "):
        if len(mobile) < 11:
            continue
        else:
            if len(mobile) is 11 and mobile.isdigit():
                result = mobile
                break
            else:
                continue

    #规则二
    mobileStr = str(num).replace("\"", "").replace("\n", "").replace(" ", "")
    if len(mobileStr) is 11 and mobileStr.isdigit():
        result = mobileStr

    if result is not None and verify_Mobile(result):
        with open(rightMobieTxt, 'a+', encoding='utf-8') as rightMobieTxt_tmp:
            rightMobieTxt_tmp.write(str(nums)+"<=====>"+str(result)+"\n")
        return result
    else:
        with open(errorMobieTxt, 'a+', encoding='utf-8') as errorMobieTxt_tmp:
            errorMobieTxt_tmp.write(str(nums)+"<=====>"+str(0)+"\n")
        return 0

def verify_Mobile(num):
    mobileHeader = int(num[0:3])
    if mobileHeader in cn_mobile:
        return True
    elif mobileHeader in cn_union:
        return True
    elif mobileHeader in cn_telecom:
        return True
    else:
        return False

def productValidMobileSQL(ID,newMobile,line):
    validMobileTxtPath = sys.path[0] + os.sep + 'validMobile.sql'
    with open(validMobileTxtPath, 'a+', encoding='utf-8') as valid_Mobile_txt_tmp:
        sql = "update personx set mobile = '"+newMobile+"' where id = '"+ID+"';-->"+str(line)+"\n"
        valid_Mobile_txt_tmp.write(sql)

def productInvalidMobileSQL(ID,errLine):
    invalidMobileTxtPath = sys.path[0] + os.sep + 'invalidMobile.sql'
    with open(invalidMobileTxtPath, 'a+', encoding='utf-8') as invalid_Mobile_txt_tmp:
        sql = "update personx set mobile = null where id = '"+str(ID)+"';--> "+str(errLine)+"\n"
        invalid_Mobile_txt_tmp.write(sql)

def verify_num(vnum):
    v_nmuber = int(vnum)
    cnm = v_nmuber in cn_mobile  # 验证为移动
    cnu = v_nmuber in cn_union #验证为联通
    cnt = v_nmuber in cn_telecom #验证为电信
    if cnm:
        print('Operator : China Mobile')
    elif cnu:
        print('Operator : China Union')
    elif cnt:
        print('Operator : China Telecom')
    else:
        print('No such a operator')

def start_verify():
    errorMobileTextPath = sys.path[0] + os.sep + 'errormobile.csv'

    with open(errorMobileTextPath, 'r', encoding='utf-8') as error_mobile_tmp:
        for line in error_mobile_tmp:
            try:
                ID = str(line).split(',')[0].replace("\"", "")
                mobile = str(line).split(',')[1].replace("\"", "")
                newMobile = getMobile(mobile)
                if newMobile is not 0:
                    productValidMobileSQL(ID, newMobile, line.replace("\n",""))
                else:
                    productInvalidMobileSQL(ID, line.replace("\n",""))
            except Exception as e:
                print(e)
                print(line)
start_verify()
