# 问题记录：管理员无法访问 Django Admin

## 问题描述

### 现象
- 登录 Django Admin (`/admin/`) 后，页面显示 "你没有查看或编辑的权限。"
- 看不到任何模型（场馆、预约等）可选

### 原因分析

Django Admin 需要以下权限才能正常访问：

| 字段 | 说明 |
|------|------|
| `is_staff=True` | 允许访问 Django Admin 站点 |
| `is_superuser=True` | 拥有所有权限 |

使用 `create_user.py` 创建管理员用户时，只设置了 `is_staff=True`，未设置 `is_superuser=True`。

## 解决方案

### 方案一：重新创建管理员用户（推荐）

1. **确保执行数据库迁移**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **创建新管理员**
   ```bash
   python create_user.py
   ```
   选择"管理员"类型创建新用户

### 方案二：修复现有管理员权限

```bash
python manage.py shell
```

在 Shell 中执行：
```python
from django.contrib.auth.models import User
from booking.models import Profile

# 修改为你的管理员用户名
user = User.objects.get(username='admin')
user.is_staff = True
user.is_superuser = True
user.save()

# 确保 Profile 存在
Profile.objects.update_or_create(
    user=user,
    defaults={'user_type': 'admin'}
)

print('管理员权限已修复')
exit()
```

### 方案三：重新初始化数据库（最彻底）

```bash
# 1. 删除数据库
del db.sqlite3

# 2. 执行迁移
python manage.py migrate

# 3. 创建管理员
python create_user.py
# 选择"管理员"类型

# 4. 启动服务器
python manage.py runserver
```

## 修复后的验证

1. 访问 http://127.0.0.1:8000/admin/
2. 使用管理员账号登录
3. 应该能看到以下模型：
   - Profiles（用户类型）
   - Courts（场地）
   - Court Availabilities（可用时间段）
   - Bookings（预约）

## 相关文件

- [create_user.py](file:///d:/Workspace/StaduimBookingSystem/create_user.py) - 用户创建脚本
- [booking/admin.py](file:///d:/Workspace/StaduimBookingSystem/booking/admin.py) - Django Admin 配置

## 记录信息

- **记录日期**: 2026-04-18
- **问题类型**: 权限配置
- **影响范围**: Django Admin 后台访问
