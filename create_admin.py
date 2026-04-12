import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stadium_booking.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin():
    username = 'admin'
    password = 'admin123'
    email = 'admin@example.com'
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, password=password, email=email)
        print(f'管理员用户创建成功！')
        print(f'用户名: {username}')
        print(f'密码: {password}')
    else:
        print(f'管理员用户 {username} 已存在')

if __name__ == '__main__':
    create_admin()
