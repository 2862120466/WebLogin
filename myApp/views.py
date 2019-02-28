from django.shortcuts import render,HttpResponse,redirect
from . import models
from . import forms
import datetime
from django.conf import settings
# Create your views here.
def main(request):
    return redirect('/index/')

def index(request):
    pass
    return render(request,'myApp/index.html')

def login(request):
    if request.session.get('is_login',None):
        return redirect('/index/')# 登录状态不允许注册。你可以修改这条原则！
    if request.method == "POST":
        login_form = forms.UserForm(request.POST) #  login_form 包含提交的数据
        message = '请检查填写的内容'
        if login_form.is_valid(): #is_valid()是forms内置的验证方法
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message  = "密码不正确！"
            except:
                message = "用户名不存在！"
        return render(request, 'myApp/login.html', locals())

    else:
        login_form = forms.UserForm() # 正常登陆时http传递地址时一般使用GET方法，如果是通过GET方法请求数据，返回一个空的表单
    return render(request, 'myApp/login.html',locals()) #请求错误重新登陆

def register(request):
    if request.session.get('is_login', None):
        return redirect("/index/")# 登录状态不允许注册。你可以修改这条原则！
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'myApp/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'myApp/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'myApp/register.html', locals())

                # 当一切都OK的情况下，创建新用户
                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)  # 使用加密密码
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)

                message = '请前往注册邮箱，进行邮件确认！'
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = forms.RegisterForm()
    return render(request, 'myApp/register.html', locals())

def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/index/')
    request.session.flush()
    return redirect('/index/')

def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'myApp/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'myApp/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'myApp/confirm.html', locals())

import hashlib

def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code

def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自qq2862120466的注册确认邮件'

    text_content = '''感谢注册www.baidu.com，这里是吴长城的站点测试，专注于Python和Django技术的专研！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>qq2862120466</a>，\
                    这里是吴长城的站点测试，</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

'''
# 首先要在顶部导入models模块；
# 使用try异常机制，防止数据库查询失败的异常；
# 如果未匹配到用户，则执行except中的语句；
# models.User.objects.get(name=username)是Django提供的最常用的数据查询API，具体含义和用法可以阅读前面的章节，不再赘述；
# 通过user.password == password进行密码比对，成功则跳转到index页面，失败则什么都不做。
# 对于非POST方法发送数据时，比如GET方法请求页面，返回空的表单，让用户可以填入数据；
# 对于POST方法，接收表单数据，并验证；
# 使用表单类自带的is_valid()方法一步完成数据验证工作；
# 验证成功后可以从表单对象的cleaned_data数据字典中获取表单的具体值；
# 如果验证不通过，则返回一个包含先前数据的表单给前端页面，方便用户修改。也就是说，它会帮你保留先前填写的数据内容，而不是返回一个空表！
# 另外，这里使用了一个小技巧，Python内置了一个locals()函数，它返回
  当前所有的本地变量字典，我们可以偷懒的将这作为render函数的数据字典
  参数值，就不用费劲去构造一个形如{'message':message, 
  'login_form':login_form}的字典了。这样做的好处当然是大大方便了
  我们，但是同时也可能往模板传入了一些多余的变量数据，造成数据冗余降
  低效率。
'''