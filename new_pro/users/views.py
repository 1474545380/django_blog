from django.shortcuts import render
from django.views import View
from django.http.response import HttpResponseBadRequest,JsonResponse
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http import HttpResponse
from utils.response_code import RETCODE
import logging
from random import randint
from libs.yuntongxun.sms import CCP
import re
from users.models import User
from django.db import DatabaseError
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import login
logger=logging.getLogger('django')
# Create your views here.
class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')
    def post(self,request):
        """
        接收数据
        验证数据
            参数是否齐全
            手机号格式是否正确
            密码是否符合格式
            两个密码是否一致
            短信验证码和Reids中的是否相同
        保存注册信息
        返回响应跳转到页面
        :param request:
        :return:
        """
        #接收数据
        mobile=request.POST.get('mobile')
        password=request.POST.get('password')
        password2=request.POST.get('password2')
        smscode=request.POST.get('sms_code')
        #验证参数是否齐全
        if not all([mobile,password,password2,smscode]):
            return HttpResponseBadRequest('缺少必要参数')
        #判断手机号格式
        if not re.match(r'^1[3-9]\d{9}$',mobile):
            return HttpResponseBadRequest("手机号不符合规则")
        #验证密码
        if not re.match(r'^[0-9A-Za-z]{8,20}$',password):
            return HttpResponseBadRequest("请输入8-20位密码")
        #两个密码是否一致
        if password!=password2:
            return HttpResponseBadRequest('两次密码不一致')
        #短信和reids中的是否一致
        redis_conn=get_redis_connection('default')
        redis_sms_code=redis_conn.get('sms:%s'%mobile)
        if redis_sms_code is None:
            return HttpResponseBadRequest("短信验证码过期")
        if smscode != redis_sms_code.decode():
            return HttpResponseBadRequest("短信验证码错误")
        #保存注册信息
        try:
            user=User.objects.create_user(username=mobile,mobile=mobile, password=password)
        except DatabaseError as e:
            logger.error(e)
            return HttpResponseBadRequest('注册失败')
        #状态保持
        login(request,user)
        #redirect重定向，reverse 通过namespace获取到视图对应的路由
        # return HttpResponse('注册成功')
        response= redirect(reverse('home:index'))
        #设置cookie信息，在index展示用户信息
        response.set_cookie('is_login',True)
        response.set_cookie('username',user.username,max_age=7*24*3600)
        return response
#注册图片验证码
class ImageCodeView(View):
    def get(self,request):
        #接收uuid
        uuid=request.GET.get('uuid')
        #判断是否收到
        if uuid is None:
            return HttpResponseBadRequest('没有传递')
        #通过调用captcha来生成图片验证码
        text,image=captcha.generate_captcha()
        #将图片保存到redis中
        #uuid为key，图片内容作为value，同时设置一个实效
        redis_connection=get_redis_connection('default')
        redis_connection.setex('img:%s'%uuid,300,text)
        #返回二进制图片
        return HttpResponse(image,content_type='image/jpeg')
# 短信验证码
class SmsCodeView(View):
    def get(self,request):
        """
        接收参数(查询字符串)
        参数验证
            验证前几个参数是否正确
            图片验证码验证
                链接redis，获取redis中的图片验证码
                判断图片验证码是否存在
                若图片验证码未过期，获取后删除图片验证码
                比对图片验证码
        生成验证码
        将短信验证码保存到redis
        发送短信
        返回响应
        :param request:
        :return:
        """
        #接受
        mobile=request.GET.get('mobile')
        image_code=request.GET.get('image_code')
        uuid=request.GET.get('uuid')
        #验证是否齐全
        if not all([mobile,image_code,uuid]):
            return JsonResponse({'code':RETCODE.NECESSARYPARAMERR,'errmsg':'缺少必要参数'})
        #验证图片验证码
        redis_conn=get_redis_connection('default')
        redis_image_code=redis_conn.get('img:%s'%uuid)
        if redis_image_code is None:
            return JsonResponse({'code':RETCODE.IMAGECODEERR,'errmsg':'图片验证码已过期'})
        #若图片验证码未过期获取后直接删除
        try:
            redis_conn.delete('img:%s'%uuid)
        except Exception as e:
            logger.error(e)
        #图片验证码比对，将字符都化为小写
        if redis_image_code.decode().lower() !=image_code.lower():
            return JsonResponse({'code':RETCODE.IMAGECODEERR,'errmsg':'图片验证码错误'})
        #生成短信验证码，将短信验证码记录到日志中
        sms_code='%06d'%randint(0,99999)
        logger.info(sms_code)
        #保存短信验证码到redis中
        redis_conn.setex('sms:%s'%mobile,300,sms_code)
        #发送短信
        CCP().send_template_sms(mobile,[sms_code,5],1)
        #返回响应
        return JsonResponse({'code':RETCODE.OK,'errmsg':'短信发送成功'})