# 羽毛球场地预约系统

这是一个基于Django开发的简单羽毛球场地预约系统。

## 功能特性

### 用户功能
1. 用户登录后可以选择场地
2. 用户可以选择预约的时间
3. 预约时间最小单位为半小时，开始时间和结束时间只能是整点或整点过半小时（例如：9:00-9:30）
4. 用户可以查看自己的预约记录
5. 用户可以取消自己的预约

### 管理员功能
1. 管理员可以管理每个场地当天的预约时间段（例如：早上八点至晚上十点）
2. 管理员可以增删场地，编辑场地信息
3. 管理员可以查看所有用户的预约信息
4. 管理员可以帮助用户取消或预定指定时间的场地

## 安装和运行

### 1. 安装依赖
```bash
pip install django
```

### 2. 运行数据库迁移
```bash
python manage.py migrate
```

### 3. 创建管理员用户
```bash
python create_admin.py
```

默认管理员账号：
- 用户名：admin
- 密码：admin123

### 4. 启动开发服务器
```bash
python manage.py runserver
```

### 5. 访问系统
打开浏览器访问：http://127.0.0.1:8000/

## 使用说明

### 管理员操作流程
1. 使用管理员账号登录系统
2. 进入"管理后台"
3. 首先添加场地（例如：1号场地、2号场地等）
4. 设置场地的可用时间段（例如：设置今天8:00-22:00）
5. 可以添加普通用户（通过Django admin后台或命令行）

### 普通用户操作流程
1. 使用普通用户账号登录系统
2. 查看"场地列表"
3. 选择要预约的场地
4. 选择预约日期和时间（注意：时间必须是整点或半点）
5. 提交预约
6. 在"我的预约"中查看预约记录
7. 如需取消，点击"取消"按钮

### 创建普通用户
可以通过Django命令行创建普通用户：
```bash
python manage.py createsuperuser
```

或者通过Django admin后台创建：
1. 访问 http://127.0.0.1:8000/admin/
2. 使用管理员账号登录
3. 在"Users"部分添加新用户
4. 注意：不要勾选"Superuser status"和"Staff status"来创建普通用户

## 项目结构

```
StaduimBookingSystem/
├── booking/                    # 主应用
│   ├── migrations/            # 数据库迁移文件
│   ├── templates/booking/     # HTML模板
│   ├── admin.py               # 管理后台配置
│   ├── models.py              # 数据模型
│   ├── urls.py                # URL配置
│   └── views.py               # 视图函数
├── stadium_booking/           # 项目配置
│   ├── settings.py            # 项目设置
│   └── urls.py                # 主URL配置
├── manage.py                  # Django管理脚本
└── create_admin.py            # 创建管理员脚本
```

## 数据模型

### Court（场地）
- name: 场地名称
- description: 场地描述

### CourtAvailability（场地可用时间段）
- court: 关联的场地
- date: 日期
- start_time: 开始时间
- end_time: 结束时间

### Booking（预约）
- user: 预约用户
- court: 预约场地
- date: 预约日期
- start_time: 开始时间
- end_time: 结束时间
- status: 状态（active/cancelled）

## 注意事项

1. 预约时间必须在场地可用时间段内
2. 预约时间不能与其他预约冲突
3. 时间必须是整点或半点（如：9:00、9:30、10:00等）
4. 结束时间必须大于开始时间
5. 管理员可以取消任何用户的预约
