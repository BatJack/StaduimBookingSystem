# 体育场馆预约系统 - 项目上下文文档

## 项目概述

这是一个基于 **Django 6.0** 框架开发的体育场馆预约系统，支持用户登录、场地预约、课程预约、学员管理、管理员管理等功能。

---

## 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                         前端 (HTML Templates)                    │
│  booking/templates/booking/                                     │
│  ├── base.html          # 基础模板 (全局CSS样式、导航栏、响应式)  │
│  ├── login.html         # 登录页                               │
│  ├── court_list.html    # 场地列表 + 矩阵式预约界面              │
│  ├── my_bookings.html   # 我的预约                             │
│  └── admin_*.html       # 管理后台页面                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      URL路由 (booking/urls.py)                  │
│  /                    → login_view      # 登录页                │
│  /logout/             → logout_view    # 退出登录               │
│  /courts/             → court_list     # 场地列表                │
│  /api/time-slots/     → get_time_slots # 获取可用时间段 (AJAX)  │
│  /api/create-booking/ → create_booking_api # 创建预约 (AJAX)     │
│  /my-bookings/        → my_bookings    # 我的预约                │
│  /manage/             → admin_*        # 管理后台相关路由        │
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
│  cancel_booking()       # 取消预约                             │
│  admin_*()              # 管理后台相关函数                      │
│  is_admin_user()        # 辅助函数：检查用户是否为管理员         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      数据模型 (booking/models.py)                 │
│  Profile                # 用户类型表 (admin/regular)            │
│  Student                # 学员信息表                            │
│  Court                  # 场地表                                │
│  CourtAvailability      # 可预约时间段表                        │
│  Booking                # 统一预约表 (场地预约/课程预约)         │
│  BookingStudent         # 预约学员关联表                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 项目文件结构

```
StaduimBookingSystem/
├── manage.py                     # Django项目管理脚本
├── db.sqlite3                    # SQLite数据库文件
├── create_user.py                # 创建用户脚本 (支持普通用户/管理员)
├── README.md                     # 项目说明文档
├── .gitignore                    # Git忽略配置
├── 关闭防火墙.bat                 # 一键关闭防火墙
├── 开启防火墙.bat                 # 一键开启防火墙
│
├── stadium_booking/              # Django项目配置
│   ├── settings.py               # 项目设置 (INSTALLED_APPS、缓存会话等)
│   ├── urls.py                   # 主URL路由 (包含booking.urls)
│   ├── wsgi.py                   # WSGI部署配置
│   └── asgi.py                   # ASGI部署配置
│
└── booking/                      # 核心应用
    ├── models.py                 # 数据模型
    ├── views.py                  # 视图函数 (所有业务逻辑)
    ├── urls.py                   # 应用URL路由
    ├── admin.py                  # Django Admin配置 (只读)
    │
    └── templates/booking/       # HTML模板
        ├── base.html              # 基础模板 (全局CSS、响应式设计)
        ├── login.html             # 登录页
        ├── court_list.html        # 场地列表 (矩阵式预约界面)
        ├── my_bookings.html       # 我的预约
        ├── admin_dashboard.html    # 管理后台首页 (仪表盘)
        ├── admin_court_list.html   # 场地管理列表
        ├── admin_court_form.html   # 添加/编辑场地
        ├── admin_availability_list.html  # 时间段管理
        ├── admin_availability_form.html # 添加/编辑时间段
        ├── admin_bookings.html     # 预约管理列表
        ├── admin_booking_form.html # 管理员添加预约
        ├── admin_booking_edit.html # 预约详情管理
        ├── admin_student_list.html # 学员管理列表
        ├── admin_student_form.html # 添加/编辑学员
        ├── admin_course_booking_list.html  # 课程预约列表
        ├── admin_course_booking_form.html  # 新增课程预约
        └── admin_course_booking_edit.html  # 课程预约管理

```

---

## 数据模型详解

### 1. Profile (用户类型)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| user | OneToOneField | 关联用户 |
| user_type | CharField | 用户类型 (admin/regular) |
| created_at | DateTimeField | 创建时间 |
| updated_at | DateTimeField | 更新时间 |

**用户类型**：
- `admin` - 管理员，可访问管理后台
- `regular` - 普通用户，仅可预约场地

### 2. Student (学员)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| name | CharField(100) | 学员姓名 |
| phone | CharField(20) | 联系电话 |
| total_class_hours | IntegerField | 课时总数 (30分钟/课时) |
| created_at | DateTimeField | 创建时间 |
| updated_at | DateTimeField | 更新时间 |

### 3. Court (场地)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| name | CharField(100) | 场地名称 |
| description | TextField | 场地描述 |
| created_at | DateTimeField | 创建时间 |
| updated_at | DateTimeField | 更新时间 |

**外键关系**：一个场地有多个预约 (`court.bookings`)，一个场地有多个可用时间段 (`court.availabilities`)

### 4. CourtAvailability (可用时间段)

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

### 5. Booking (统一预约)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| booking_type | CharField | 预约类型 (court/course) |
| user | ForeignKey | 预约用户 (可为空) |
| court | ForeignKey | 预约场地 |
| date | DateField | 预约日期 |
| start_time | TimeField | 开始时间 |
| end_time | TimeField | 结束时间 |
| booker_name | CharField(100) | 预约人姓名 |
| booker_phone | CharField(20) | 预约人联系方式 |
| status | CharField | 状态 (active/cancelled) |
| created_at | DateTimeField | 创建时间 |
| updated_at | DateTimeField | 更新时间 |

**辅助方法**：
- `is_court_booking()` - 判断是否为场地预约
- `is_course_booking()` - 判断是否为课程预约
- `get_student_count()` - 获取学员人数
- `get_total_class_hours()` - 获取总课时数

### 6. BookingStudent (预约学员关联)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| booking | ForeignKey | 关联预约 |
| student | ForeignKey | 关联学员 |
| class_hours | IntegerField | 扣除课时数 |
| created_at | DateTimeField | 创建时间 |

**唯一约束**：`unique_together: ['booking', 'student']`

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
| `/manage/` | `admin_dashboard` | GET | 管理后台首页 |
| `/manage/courts/` | `admin_court_list` | GET | 场地管理列表 |
| `/manage/courts/add/` | `admin_court_add` | GET/POST | 添加场地 |
| `/manage/courts/edit/<id>/` | `admin_court_edit` | GET/POST | 编辑场地 |
| `/manage/courts/delete/<id>/` | `admin_court_delete` | GET | 删除场地 |
| `/manage/availabilities/` | `admin_availability_list` | GET | 时间段管理列表 |
| `/manage/availabilities/add/` | `admin_availability_add` | GET/POST | 添加时间段 |
| `/manage/bookings/` | `admin_bookings` | GET | 预约管理列表 |
| `/manage/bookings/add/` | `admin_booking_add` | GET/POST | 管理员添加预约 |
| `/manage/bookings/edit/<id>/` | `admin_booking_edit` | GET/POST | 预约详情管理 |
| `/manage/students/` | `admin_student_list` | GET | 学员管理列表 |
| `/manage/students/add/` | `admin_student_add` | GET/POST | 添加学员 |
| `/manage/students/edit/<id>/` | `admin_student_edit` | GET/POST | 编辑学员 |
| `/manage/students/delete/<id>/` | `admin_student_delete` | GET | 删除学员 |
| `/manage/course-bookings/` | `admin_course_booking_list` | GET | 课程预约列表 |
| `/manage/course-bookings/add/` | `admin_course_booking_add` | GET/POST | 新增课程预约 |
| `/manage/course-bookings/edit/<id>/` | `admin_course_booking_edit` | GET/POST | 课程预约管理 |
| `/manage/course-bookings/delete/<id>/` | `admin_course_booking_delete` | GET | 删除课程预约 |

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
        {
          "start": "08:00",
          "end": "08:30",
          "label": "08:00-08:30",
          "is_booked": false
        },
        {
          "start": "09:00",
          "end": "09:30",
          "label": "09:00-09:30",
          "is_booked": true,
          "booking_type": "court",
          "booking_id": 1,
          "booker_name": "张三",
          "booker_phone": "13800138000"
        },
        {
          "start": "10:00",
          "end": "10:30",
          "label": "10:00-10:30",
          "is_booked": true,
          "booking_type": "course",
          "booking_id": 2,
          "student_count": 3,
          "total_class_hours": 6,
          "students": [
            {"student__name": "李四", "student__phone": "13900139000", "class_hours": 2},
            ...
          ]
        }
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
  "end_time": "10:00",
  "booker_name": "张三",
  "booker_phone": "13800138000"
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

系统使用 `Profile.user_type` 字段区分管理员和普通用户：

| 用户类型 | `user_type` | 可访问功能 |
|---------|------------|-----------|
| 普通用户 | `regular` | 场地列表、我的预约、取消自己的预约 |
| 管理员 | `admin` | 上述功能 + 管理后台全部功能 |

### 权限检查逻辑

`is_admin_user()` 辅助函数（[views.py](file:///d:/Workspace/StaduimBookingSystem/booking/views.py)）：
```python
def is_admin_user(user):
    try:
        return user.profile.user_type == 'admin'
    except Profile.DoesNotExist:
        return False
```

管理员权限检查示例：
```python
@login_required
def admin_dashboard(request):
    if not is_admin_user(request.user):
        messages.error(request, '您没有权限访问此页面')
        return redirect('court_list')
    ...
```

登录后跳转逻辑：
```python
def login_view(request):
    ...
    if user:
        login(request, user)
        if is_admin_user(user):
            return redirect('admin_dashboard')
        return redirect('court_list')
```

导航栏根据用户类型显示不同链接（[base.html](file:///d:/Workspace/StaduimBookingSystem/booking/templates/booking/base.html)）：
```html
{% if user.profile.user_type == 'admin' %}
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
3. get_time_slots() 查询数据库，返回可用时间段（含预约类型、预约人信息）
                              ↓
4. 前端展示矩阵式时间段网格，用户点击选择
                              ↓
5. 用户点击"确认预约" → 弹出填写预约人信息弹窗
                              ↓
6. 用户填写姓名和手机号 → POST /api/create-booking/
                              ↓
7. create_booking_api() 验证并创建预约
                              ↓
8. 返回结果，前端显示成功/失败提示
```

### 管理员设置可用时间段流程

```
1. 管理员访问 /manage/availabilities/add/
                              ↓
2. 填写表单：场地、开始日期、结束日期、每天时间
                              ↓
3. 提交 → admin_availability_add() 创建 CourtAvailability 记录
                              ↓
4. 该场地在指定日期范围内每天开放
```

### 课程预约流程

```
1. 管理员访问 /manage/course-bookings/add/
                              ↓
2. 选择场地和预约时间 → 提交
                              ↓
3. 进入添加学员页面 → 选择学员并设置课时
                              ↓
4. 确认预约 → 创建Booking记录(booking_type='course')
                              ↓
5. 自动扣除学员课时 → 创建BookingStudent记录
```

---

## 模板继承关系

```
base.html (基础模板，含响应式CSS)
├── login.html
├── court_list.html     (矩阵式预约界面)
├── my_bookings.html
└── admin_*.html         (管理后台)
    ├── admin_dashboard.html
    ├── admin_court_list.html
    ├── admin_court_form.html
    ├── admin_availability_list.html
    ├── admin_availability_form.html
    ├── admin_bookings.html
    ├── admin_booking_form.html
    ├── admin_booking_edit.html
    ├── admin_student_list.html
    ├── admin_student_form.html
    ├── admin_course_booking_list.html
    ├── admin_course_booking_form.html
    └── admin_course_booking_edit.html
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
- `.stat-cards` - 统计卡片
- `.matrix-table` - 矩阵式预约表格

**响应式设计**：
- `@media (max-width: 768px)` - 平板适配
- `@media (max-width: 480px)` - 手机适配

---

## 会话配置

系统使用缓存会话存储（LocMemCache）：
- 会话数据存储在内存缓存中
- 服务器重启后会话丢失，用户需重新登录
- 配置在 `stadium_booking/settings.py` 中

---

## 常用命令

```bash
# 运行开发服务器
python manage.py runserver

# 运行开发服务器（允许局域网访问）
python manage.py runserver 0.0.0.0:8000

# 创建数据库迁移
python manage.py makemigrations

# 执行数据库迁移
python manage.py migrate

# 创建用户 (运行GUI工具)
python create_user.py

# 进入Django shell
python manage.py shell
```

---

## 默认管理员账号

运行 `python create_user.py` 创建用户，选择"管理员"类型即可。

---

## 注意事项

1. **用户类型**：使用 `Profile.user_type` 字段控制管理员/普通用户权限
2. **预约时间规则**：开始和结束时间必须是整点或半点 (如 09:00, 09:30, 10:00)
3. **数据库变更**：修改 `models.py` 后需要执行 `makemigrations` 和 `migrate`
4. **AJAX请求**：前端使用原生JavaScript，无额外框架依赖
5. **Profile自动创建**：新用户通过 `create_user.py` 创建时会自动创建 Profile 记录
6. **统一预约模型**：Booking模型通过booking_type区分场地预约和课程预约
7. **冲突检测**：场地预约和课程预约共享冲突检测逻辑
8. **响应式设计**：系统支持手机端访问，界面自动适配
9. **会话存储**：服务器重启后需重新登录
10. **URL路由**：自定义管理后台使用 `/manage/` 前缀，避免与Django Admin冲突
