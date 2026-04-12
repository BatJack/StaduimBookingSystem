# 羽毛球场地预约系统 - 项目上下文文档

## 项目概述

这是一个基于 **Django** 框架开发的羽毛球场地预约系统，提供场地预约、管理等功能。

---

## 项目结构

```
StaduimBookingSystem/
├── manage.py                    # Django项目管理脚本
├── db.sqlite3                   # SQLite数据库
├── create_admin.py              # 创建管理员脚本
├── README.md                    # 项目说明文档
│
├── stadium_booking/             # Django项目配置目录
│   ├── settings.py              # 项目设置
│   ├── urls.py                  # 主URL路由
│   ├── wsgi.py                  # WSGI部署配置
│   └── asgi.py                  # ASGI部署配置
│
└── booking/                     # 核心应用目录
    ├── models.py                # 数据模型定义
    ├── views.py                 # 视图函数/业务逻辑
    ├── urls.py                  # 应用URL路由
    ├── admin.py                 # Django Admin配置
    ├── apps.py                  # 应用配置
    ├── tests.py                 # 测试文件
    └── templates/booking/       # UI模板目录
        ├── base.html            # 基础模板（全局样式）
        ├── court_list.html      # 场地列表页
        ├── booking_form.html    # 预约表单页
        ├── my_bookings.html     # 我的预约页
        ├── login.html           # 登录页
        ├── admin_dashboard.html # 管理后台首页
        ├── admin_court_list.html    # 场地管理页
        ├── admin_court_form.html    # 场地表单页
        ├── admin_bookings.html      # 预约管理页
        ├── admin_booking_form.html  # 预约表单页
        ├── admin_availability_list.html  # 时间段列表页
        └── admin_availability_form.html  # 时间段表单页
```

---

## UI界面编辑指南

### 主要UI文件位置

**核心目录：** `booking/templates/booking/`

| 文件 | 用途 | 说明 |
|------|------|------|
| `base.html` | 基础模板 | 包含全局CSS样式、导航栏、页面框架结构 |
| `court_list.html` | 场地列表 | 用户首页，展示所有可预约场地 |
| `booking_form.html` | 预约表单 | 用户预约场地的表单页面 |
| `my_bookings.html` | 我的预约 | 用户查看自己预约记录的页面 |
| `login.html` | 登录页面 | 用户登录界面 |
| `admin_dashboard.html` | 管理后台首页 | 管理员功能入口 |
| `admin_court_list.html` | 场地管理 | 管理员管理场地列表 |
| `admin_court_form.html` | 场地表单 | 添加/编辑场地 |
| `admin_bookings.html` | 预约管理 | 管理员查看所有预约 |
| `admin_booking_form.html` | 预约表单 | 管理员编辑预约 |
| `admin_availability_list.html` | 时间段管理 | 管理场地开放时间 |
| `admin_availability_form.html` | 时间段表单 | 添加/编辑开放时间段 |

### 样式编辑

**所有CSS样式都内嵌在 `base.html` 中**，包括：
- 全局样式：字体、背景色、盒模型
- 导航栏样式：`.header`, `.nav`
- 按钮样式：`.btn`, `.btn-danger`, `.btn-success`
- 卡片样式：`.card`
- 网格布局：`.grid`
- 消息提示：`.messages`, `.message`

### 模板继承结构

```
base.html (基础模板)
   ├── court_list.html
   ├── booking_form.html
   ├── my_bookings.html
   ├── login.html
   └── admin_*.html
```

所有子页面通过 `{% extends 'booking/base.html' %}` 继承基础模板。

---

## 后端逻辑编辑指南

### 数据模型 (models.py)

主要模型类：
- `Court` - 场地模型
- `Booking` - 预约模型
- `Availability` - 可用时间段模型

### 视图函数 (views.py)

包含所有业务逻辑和请求处理函数。

### URL路由 (urls.py)

定义所有URL路径与视图函数的映射关系。

---

## 开发规范

### 修改UI时

1. **修改全局样式** → 编辑 `base.html` 中的 `<style>` 标签
2. **修改页面布局** → 编辑对应的子模板文件
3. **修改导航栏** → 编辑 `base.html` 中的 `.nav` 部分
4. **添加新页面** → 创建新模板，继承 `base.html`

### 修改后端时

1. **添加新功能** → 先在 `models.py` 定义数据模型，再在 `views.py` 编写视图，最后在 `urls.py` 添加路由
2. **修改业务逻辑** → 编辑 `views.py` 中对应的视图函数
3. **数据库变更** → 创建并运行 migration

### 命名约定

- 模板文件：使用下划线命名法 (snake_case)
- URL名称：使用下划线命名法 (snake_case)
- 模板块：使用下划线命名法 (snake_case)

---

## 常用命令

```bash
# 运行开发服务器
python manage.py runserver

# 创建数据库迁移
python manage.py makemigrations

# 执行数据库迁移
python manage.py migrate

# 创建管理员用户
python create_admin.py
```

---

## 注意事项

1. 所有UI模板都在 `booking/templates/booking/` 目录下
2. CSS样式统一在 `base.html` 中管理，避免样式分散
3. 新增页面需继承 `base.html` 并填充 `{% block content %}`
4. 修改模型后记得执行数据库迁移
