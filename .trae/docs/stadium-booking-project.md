# 羽毛球场地预约系统 - 项目上下文文档

## 项目概述

这是一个基于 **Django 6.0** 框架开发的羽毛球场地预约系统，支持用户登录、场地预约、管理员管理等功能。

---

## 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                         前端 (HTML Templates)                    │
│  booking/templates/booking/                                     │
│  ├── base.html          # 基础模板 (全局CSS样式、导航栏)          │
│  ├── login.html         # 登录页                               │
│  ├── court_list.html    # 场地列表 + AJAX预约                   │
│  ├── my_bookings.html   # 我的预约                             │
│  └── admin_*.html       # 管理后台页面                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      URL路由 (booking/urls.py)                  │
│  /                → login_view      # 登录页                    │
│  /courts/         → court_list     # 场地列表                    │
│  /api/time-slots/ → get_time_slots # 获取可用时间段 (AJAX)      │
│  /api/create-booking/ → create_booking_api # 创建预约 (AJAX)    │
│  /my-bookings/    → my_bookings    # 我的预约                   │
│  /admin/          → admin_*        # 管理后台相关路由            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      视图函数 (booking/views.py)                 │
│  login_view()           # 用户登录                              │
│  court_list()           # 场地列表页面                          │
│  get_time_slots()       # API: 获取时间段 (GET)                │
│  create_booking_api()   # API: 创建预约 (POST)                 │
│  my_bookings()          # 我的预约列表                          │
│  cancel_booking()        # 取消预约                             │
│  admin_*()              # 管理后台相关函数                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      数据模型 (booking/models.py)                 │
│  Court                 # 场地表                                │
│  CourtAvailability     # 可预约时间段表 (日期范围+每天时间)       │
│  Booking               # 预约记录表                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 项目文件结构

```
StaduimBookingSystem/
├── manage.py                     # Django项目管理脚本
├── db.sqlite3                    # SQLite数据库文件
├── create_admin.py               # 创建管理员脚本
├── README.md                     # 项目说明文档
├── .gitignore                    # Git忽略配置
│
├── stadium_booking/              # Django项目配置
│   ├── settings.py               # 项目设置 (INSTALLED_APPS等)
│   ├── urls.py                   # 主URL路由 (包含booking.urls)
│   ├── wsgi.py                   # WSGI部署配置
│   └── asgi.py                   # ASGI部署配置
│
└── booking/                      # 核心应用
    ├── models.py                 # 数据模型 (Court, CourtAvailability, Booking)
    ├── views.py                  # 视图函数 (所有业务逻辑)
    ├── urls.py                   # 应用URL路由
    ├── admin.py                  # Django Admin配置
    │
    └── templates/booking/       # HTML模板
        ├── base.html              # 基础模板 (全局CSS: ~700行)
        ├── login.html             # 登录页
        ├── court_list.html        # 场地列表 (AJAX预约)
        ├── my_bookings.html       # 我的预约
        ├── admin_dashboard.html    # 管理后台首页
        ├── admin_court_list.html   # 场地管理列表
        ├── admin_court_form.html   # 添加/编辑场地
        ├── admin_availability_list.html  # 时间段管理
        ├── admin_availability_form.html # 添加/编辑时间段
        ├── admin_bookings.html     # 预约管理列表
        └── admin_booking_form.html # 管理员添加预约

```

---

## 数据模型详解

### 1. Court (场地)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| name | CharField(100) | 场地名称 |
| description | TextField | 场地描述 |
| created_at | DateTimeField | 创建时间 |
| updated_at | DateTimeField | 更新时间 |

**外键关系**：一个场地有多个预约 (`court.bookings`)，一个场地有多个可用时间段 (`court.availabilities`)

### 2. CourtAvailability (可用时间段)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| court | ForeignKey | 关联场地 |
| start_date | DateField | 可预约开始日期 |
| end_date | DateField | 可预约结束日期 |
| start_time | TimeField | 每天开始时间 |
| end_time | TimeField | 每天结束时间 |
| created_at | DateTimeField | 创建时间 |
| updated_at | DateTimeField | 更新时间 |

**关键方法**：`is_date_available(date)` - 检查指定日期是否在可用范围内

### 3. Booking (预约)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| user | ForeignKey | 预约用户 |
| court | ForeignKey | 预约场地 |
| date | DateField | 预约日期 |
| start_time | TimeField | 开始时间 |
| end_time | TimeField | 结束时间 |
| status | CharField | 状态 (active/cancelled) |
| created_at | DateTimeField | 创建时间 |
| updated_at | DateTimeField | 更新时间 |

**业务规则**：
- 时间必须是整点或半点 (minute ∈ {0, 30})
- 预约时间必须在场地可用时间段内
- 不能与已有预约冲突

---

## URL路由表

| URL路径 | 视图函数 | 方法 | 说明 |
|---------|---------|------|------|
| `/` | `login_view` | GET/POST | 登录页 |
| `/logout/` | `logout_view` | GET | 退出登录 |
| `/courts/` | `court_list` | GET | 场地列表页 |
| `/api/time-slots/` | `get_time_slots` | GET | 获取可用时间段 (AJAX) |
| `/api/create-booking/` | `create_booking_api` | POST | 创建预约 (AJAX) |
| `/my-bookings/` | `my_bookings` | GET | 我的预约 |
| `/cancel-booking/<id>/` | `cancel_booking` | GET | 取消预约 |
| `/admin/` | `admin_dashboard` | GET | 管理后台首页 |
| `/admin/courts/` | `admin_court_list` | GET | 场地管理列表 |
| `/admin/courts/add/` | `admin_court_add` | GET/POST | 添加场地 |
| `/admin/courts/edit/<id>/` | `admin_court_edit` | GET/POST | 编辑场地 |
| `/admin/courts/delete/<id>/` | `admin_court_delete` | GET | 删除场地 |
| `/admin/availabilities/` | `admin_availability_list` | GET | 时间段管理列表 |
| `/admin/availabilities/add/` | `admin_availability_add` | GET/POST | 添加时间段 |
| `/admin/bookings/` | `admin_bookings` | GET | 预约管理列表 |
| `/admin/bookings/add/` | `admin_booking_add` | GET/POST | 管理员添加预约 |

---

## API接口详情

### 1. GET /api/time-slots/?date=YYYY-MM-DD

**用途**：获取指定日期所有场地的可用时间段

**请求参数**：
- `date` (必需): 查询日期，格式 YYYY-MM-DD

**响应**：
```json
{
  "courts": [
    {
      "id": 1,
      "name": "1号场地",
      "description": "...",
      "is_available": true,
      "start_time": "08:00",
      "end_time": "22:00",
      "time_slots": [
        {"start": "08:00", "end": "08:30", "label": "08:00-08:30", "is_booked": false},
        ...
      ]
    }
  ]
}
```

### 2. POST /api/create-booking/

**用途**：创建新预约

**请求体**：
```json
{
  "court_id": 1,
  "date": "2026-04-15",
  "start_time": "09:00",
  "end_time": "10:00"
}
```

**响应**：
```json
{"success": true, "message": "预约成功"}
```

**错误响应**：
```json
{"error": "该时间段已被预约"}
```

---

## 用户权限体系

### 管理员与普通用户的区分

系统使用 Django 内置的 `User.is_staff` 字段区分管理员和普通用户：

| 用户类型 | `is_staff` | 可访问功能 |
|---------|------------|-----------|
| 普通用户 | `False` | 场地列表、我的预约、取消自己的预约 |
| 管理员 | `True` | 上述功能 + 管理后台全部功能 |

### 权限检查逻辑

管理员权限检查示例（[views.py](file:///d:/Workspace/StaduimBookingSystem/booking/views.py)）：
```python
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, '您没有权限访问此页面')
        return redirect('court_list')
    ...
```

导航栏根据用户类型显示不同链接（[base.html](file:///d:/Workspace/StaduimBookingSystem/booking/templates/booking/base.html)）：
```html
{% if user.is_staff %}
    <a href="{% url 'admin_dashboard' %}">管理后台</a>
{% endif %}
```

---

## 前后端数据流

### 用户预约流程

```
1. 用户访问 /courts/  → court_list() 渲染 court_list.html
                              ↓
2. 用户选择日期 → JavaScript调用 /api/time-slots/?date=XXX
                              ↓
3. get_time_slots() 查询数据库，返回可用时间段
                              ↓
4. 前端展示时间段网格，用户点击选择
                              ↓
5. 用户点击"确认预约" → POST /api/create-booking/
                              ↓
6. create_booking_api() 验证并创建预约
                              ↓
7. 返回结果，前端显示成功/失败提示
```

### 管理员设置可用时间段流程

```
1. 管理员访问 /admin/availabilities/add/
                              ↓
2. 填写表单：场地、开始日期、结束日期、每天时间
                              ↓
3. 提交 → admin_availability_add() 创建 CourtAvailability 记录
                              ↓
4. 该场地在指定日期范围内每天开放
```

---

## 模板继承关系

```
base.html (基础模板)
├── login.html
├── court_list.html     (用户预约界面)
├── my_bookings.html
└── admin_*.html         (管理后台)
    ├── admin_dashboard.html
    ├── admin_court_list.html
    ├── admin_court_form.html
    ├── admin_availability_list.html
    ├── admin_availability_form.html
    ├── admin_bookings.html
    └── admin_booking_form.html
```

所有子页面通过 `{% extends 'booking/base.html' %}` 继承基础模板。

---

## 样式管理

**所有CSS样式都内嵌在 `base.html` 中**，包括：

| 样式类别 | CSS变量 | 说明 |
|---------|---------|------|
| 主色 | `--primary`, `--primary-hover` | 按钮、链接 |
| 成功色 | `--success`, `--success-hover` | 成功状态 |
| 危险色 | `--danger`, `--danger-hover` | 错误、删除 |
| 警告色 | `--warning` | 警告状态 |
| 背景色 | `--gray-50` ~ `--gray-900` | 灰度色阶 |

**组件样式**：
- `.header`, `.nav` - 导航栏
- `.btn`, `.btn-success`, `.btn-danger` - 按钮
- `.card` - 卡片容器
- `.grid` - 网格布局
- `.table-wrapper table` - 表格
- `.form-group` - 表单组

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

# 进入Django shell
python manage.py shell
```

---

## 注意事项

1. **预约时间规则**：开始和结束时间必须是整点或半点 (如 09:00, 09:30, 10:00)
2. **数据库变更**：修改 `models.py` 后需要执行 `makemigrations` 和 `migrate`
3. **Django Admin**：访问 `/admin/` 可管理所有模型数据
4. **AJAX请求**：前端使用原生JavaScript，无额外框架依赖
5. **管理员权限**：使用 `is_staff` 字段控制，非 Django Admin 的 `is_superuser`
