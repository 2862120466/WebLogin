import os
import time
from django.core.mail import send_mail

os.environ['DJANGO_SETTINGS_MODULE'] = 'WebLogin.settings'

if __name__ == '__main__':

    send_mail(
        '吴长城的消息',
        '你好，我是吴长城,这是老子的第二条消息',
        '2862120466@qq.com',
        ['2862120466@qq.com'],
    )