# -*- coding: utf-8 -*-
# @Author: WildMan
# @Date: 2018/4/10
import requests,json,re
from concurrent.futures import ThreadPoolExecutor


def zx_test(name,idCard,servicename,post_url):
    headers = {
        "Content-Type": "Application/json;charset=utf-8",
    }
    params = {
        "loginName": "xyh123456",
        "pwd": "xyh123456",
        "serviceName": servicename,
        "param": {
            'idCard': idCard,
            'name': name
        }
    }
    payload = json.dumps(params)
    res = requests.post(post_url, data=payload, verify=False)

    return res.text


if __name__ == '__main__':
    name = '杨宇'
    idCard = '340223198711148117'
    sernames = {
        'ExecutedInfo': 'https://www.miniscores.cn:8313/CreditFunc/v2.1/ExecutedInfo',
        'PaymentBlackVerify': 'https://www.miniscores.cn:8313/CreditFunc/v2.1/PaymentBlackVerify',
        'RiskListCombineInfo': 'https://www.miniscores.cn:8313/CreditFunc/v2.1/RiskListCombineInfo',
        'ExecutedDefaulterInfo': 'https://www.miniscores.cn:8313/CreditFunc/v2.1/ExecutedDefaulterInfo',
        'BlackListCheck': 'https://www.miniscores.cn:8313/CreditFunc/v2.1/BlackListCheck'
    }
    # 多线程
    executor = ThreadPoolExecutor(max_workers=5)

    res_dic = {}
    for s,u in sernames.items():
        res = executor.submit(zx_test, *(name,idCard,s,u))
        res_dic[s] = res.result()

    print(res_dic)



