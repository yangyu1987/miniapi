# -*- coding: utf-8 -*-
# @Author: WildMan
# @Date: 2018/4/10
import random,hashlib,os,json,requests,re


def sms6num():
    # 短信验证码生成器
    numbers = ''
    for i in range(6):
        numbers += str(random.randint(0, 9))
    return numbers


def creToken():
    #token 生成器
    token = hashlib.sha1(os.urandom(24)).hexdigest()
    return token


def zx_test(name,idCard,mobile,servicename,post_url):
    headers = {
        "Content-Type": "Application/json;charset=utf-8",
    }
    if servicename == "ExecutedInfo" :
        postParam = {
            'idCard': idCard,
            'name': name
        }
    elif servicename == "ExecutedDefaulterInfo":
        postParam = {
            'idCard': idCard,
            'name': name
        }
    elif servicename == "PaymentBlackVerify":
        postParam = {
            'idCard': idCard,
            'name': name,
            'mobile': mobile
        }
    elif servicename == "RiskListCombineInfo":
        postParam = {
            'idCard': idCard,
            'name': name,
            'mobile': mobile
        }
    elif servicename == "BlackListCheck":
        postParam = {
            'idCard': idCard,
            'name': name,
            'mobile': mobile
        }
    else:
        postParam = {
            'idCard': idCard,
            'name': name,
            'mobile':mobile
        }

    params = {
        "loginName": "xyh123456",
        "pwd": "xyh123456",
        "serviceName": servicename,
        "param": postParam
    }
    payload = json.dumps(params)
    res = requests.post(post_url, data=payload, verify=False)

    return res.text


if __name__ == "__main__":
    pass