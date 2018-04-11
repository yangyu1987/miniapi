# -*- coding: utf-8 -*-
# @Author: WildMan
# @Date: 2018/4/11
from django import forms
from captcha.fields import CaptchaField


class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()