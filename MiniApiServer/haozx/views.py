from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse,JsonResponse
from haozx import models
from haozx.tools import sendmsg
from utils.commom import *
from utils.config import *
import uuid,json,time
from concurrent.futures import ThreadPoolExecutor
# Create your views here.


class TokenMaker(View):
    # 访问页面挂载token
    def get(self, request):
        haozx = models.Haozx()
        token = creToken()
        haozx.token = token
        haozx.save()
        msg_res = {
            'token': token,
        }
        response = HttpResponse(json.dumps(msg_res))
        response['Content-Type'] = "application/json"
        response['Access-Control-Allow-Origin'] = "*"
        return response


class Sendmsg(View):
    # 短信发送模块
    def get(self, request):
        return render(request, 'haozx/sendmsg.html')
        # return HttpResponse('短信输入页面')

    def post(self, request):
        # 校验和发送
        phoneNum = request.POST.get('phoneNum', '')
        token = request.POST.get('token', '')
        smsCode = sms6num() # 短信验证码
        # 校验token 是否存在 短信是否已发送
        try:
            # token 校验成功
            sql_res = models.Haozx.objects.get(token=token, smsSend=0)
            # 存入手机号和短信验证码
            sql_res.phoneNum = phoneNum
            sql_res.smsCode = smsCode
            sql_res.timestamp = int(time.time() * 1000)
            # 发送短信
            __business_id = uuid.uuid1()
            params = json.dumps({'code': smsCode})
            dy_res = sendmsg.send_sms(__business_id, phoneNum, "好甄信", "SMS_130915678", params)
            dy_res = json.loads(dy_res)
            if dy_res['Code'] == "OK":
                # "Code": "OK" 表示发送成功
                sql_res.smsSend = 1
                sql_res.save()
                msg_res = {
                    'success': 1,
                    'info': '短信发送成功',
                    'token': token
                }
                response = HttpResponse(json.dumps(msg_res))
                response['Content-Type'] = "application/json"
                response['Access-Control-Allow-Origin'] = "*"
                return response
            else:
                sql_res.smsSend = 0
                sql_res.save()
                msg_res = {
                    'success': 0,
                    'info': '短信发送失败',
                }
                response = HttpResponse(json.dumps(msg_res))
                response['Content-Type'] = "application/json"
                response['Access-Control-Allow-Origin'] = "*"
                return response
        except:
            # token 校验失败
            msg_res = {
                'success': 0,
                'info': '非法请求',
            }
            response = HttpResponse(json.dumps(msg_res))
            response['Content-Type'] = "application/json"
            response['Access-Control-Allow-Origin'] = "*"
            return response


class Checkmsg(View):
    # 短信校验模块
    def get(self, request):
        return render(request, 'haozx/checkmsg.html')
        # return HttpResponse('输入页面')

    def post(self, request):
        phoneNum = request.POST.get('phoneNum', '')
        smsCode = request.POST.get('smsCode', '')
        token = request.POST.get('token', '')
        # 开始校验
        try:
            sql_res = models.Haozx.objects.get(phoneNum=phoneNum,smsCode=smsCode,token=token,codeUsed=0)
            msg_res = {
                'success': 1,
                'info': '短信校验成功'
            }
            response = HttpResponse(json.dumps(msg_res))
            response['Content-Type'] = "application/json"
            response['Access-Control-Allow-Origin'] = "*"
            return response
        except:
            msg_res = {
                'success':0,
                'info':'短信校验失败'
            }
            response = HttpResponse(json.dumps(msg_res))
            response['Content-Type'] = "application/json"
            response['Access-Control-Allow-Origin'] = "*"
            return response


class GetRes(View):
    # 接口查询 并返回结果
    def get(self, request):
        return render(request, 'haozx/getmaininfo.html')
        # return HttpResponse(status=503)

    def post(self, request):
        # 5线程查询5个接口
        name = request.POST.get('name', '')
        idCard = request.POST.get('idCard', '')
        token = request.POST.get('token', '')
        sernames = SERVICENAMES
        #开始访问
        sql_res = ''
        try:
            sql_res = models.Haozx.objects.get(token=token, codeUsed=0)
        except:
            msg_res = {
                'success': 0,
                'info': '非法访问'
            }
            response = HttpResponse(json.dumps(msg_res))
            response['Content-Type'] = "application/json"
            response['Access-Control-Allow-Origin'] = "*"
            return response

        if sql_res:
            sql_res.name = name
            sql_res.idCard = idCard
            mobile = str(sql_res.phoneNum)
            # 多线程
            executor = ThreadPoolExecutor(max_workers=5)
            res_dic = {}
            for s, u in sernames.items():
                res = executor.submit(zx_test, *(name, idCard, mobile, s, u))
                res_dic[s] = res.result()
            # 获取返回结果
            sql_res.result = json.dumps(res_dic)
            # 更新验证码为已用
            sql_res.codeUsed = 1
            sql_res.save()
            # 暴露结果
            response = HttpResponse(json.dumps(res_dic))
            response['Content-Type'] = "application/json"
            response['Access-Control-Allow-Origin'] = "*"
            return response
