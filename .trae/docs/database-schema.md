# 体育场馆预约系统 - 数据库结构文档

## 数据库概述

- **数据库类型**：SQLite3
- **Django版本**：6.0
- **数据库文件**：`db.sqlite3`
- **应用**：booking

---

## 数据表关系图

```
┌─────────────────┐      ┌─────────────────┐
│     User        │      │    Profile      │
│  (Django内置)   │──────│   用户类型      │
│                 │ 1:1  │  user_type      │
└─────────────────┘      └─────────────────┘
                                  │
                                  │ 1:1
                                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  ┌──────────┐     1:N      ┌──────────────────┐     1:N         │
│  │  Court   │─────────────│ CourtAvailability │                 │
│  │  场地    │             │   可用时间段      │                 │
│  └──────────┘             └──────────────────┘                 │
│       │                                                        │
│       │ 1:N                                                    │
│       ├──────────────┐                                        │
│       │              │ 1:N                                     │
│       ▼              ▼                                         │
│  ┌──────────┐  ┌─────────────────┐                           │
│  │ Booking  │  │ CourseBooking   │     课程预约              │
│  │ 预约      │  └─────────────────┘                           │
│  └──────────┘           │                                       │
│       │                 │ 1:N                                   │
│       │                 ▼                                       │
│       │        ┌─────────────────────┐                        │
│       │        │ CourseBookingStudent │                        │
│       │        │    课程学员关系       │                        │
│       │        └─────────────────────┘                        │
│       │                 │                                       │
│       │                 │ N:1                                   │
│       │                 ▼                                       │
│       │          ┌──────────────┐                              │
│       └──────────│   Student     │     学员信息                 │
│  (普通预约)      │  姓名/电话/课时 │                              │
│                  └──────────────┘                              │
└──────────────────────────────────────────────────────────────────┘
```

---

## 数据表详细说明

### 1. auth_user (Django内置用户表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY | 主键 |
| username | VARCHAR(150) | 用户名 |
| password | VARCHAR(128) | 密码哈希 |
| email | VARCHAR(254) | 邮箱 |
| first_name | VARCHAR(150) | 名 |
| last_name | VARCHAR(150) | 姓 |
| is_staff | BOOLEAN | 是否为员工 |
| is_active | BOOLEAN | 是否激活 |
| date_joined | DATETIME | 注册时间 |

---

### 2. booking_profile (用户类型扩展)

**关联**：`auth_user.id` → `booking_profile.user` (1:1)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| user_id | INTEGER | 外键关联User |
| user_type | VARCHAR(20) | 用户类型 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

**user_type选项**：
- `admin` - 管理员
- `regular` - 普通用户

---

### 3. booking_court (场地表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| name | VARCHAR(100) | 场地名称 |
| description | TEXT | 场地描述（可为空） |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

**关联关系**：
- `court.availabilities` → 1:N → `CourtAvailability`
- `court.bookings` → 1:N → `Booking`
- `court.course_bookings` → 1:N → `CourseBooking`

---

### 4. booking_courtavailability (场地可用时间段)

**关联**：`booking_court.id` → `booking_courtavailability.court` (N:1)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| court_id | INTEGER | 外键关联Court |
| start_date | DATE | 可预约开始日期 |
| end_date | DATE | 可预约结束日期 |
| start_time | TIME | 每天开始时间 |
| end_time | TIME | 每天结束时间 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

**业务逻辑**：
- 同一场地可以有多个可用时间段（不同日期范围）
- `is_date_available(date)` 方法判断指定日期是否可用

---

### 5. booking_booking (普通预约)

**关联**：
- `auth_user.id` → `booking_booking.user` (N:1)
- `booking_court.id` → `booking_booking.court` (N:1)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| user_id | INTEGER | 外键关联User |
| court_id | INTEGER | 外键关联Court |
| date | DATE | 预约日期 |
| start_time | TIME | 开始时间 |
| end_time | TIME | 结束时间 |
| status | VARCHAR(20) | 状态 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

**status选项**：
- `active` - 有效
- `cancelled` - 已取消

**业务规则**：
- 时间必须是整点或半点
- 不能与同一场地的其他有效预约冲突

---

### 6. booking_student (学员信息)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| name | VARCHAR(100) | 学员姓名 |
| phone | VARCHAR(20) | 联系电话 |
| total_class_hours | INTEGER | 课时总数（30分钟/课时） |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

**关联关系**：
- `student.course_bookings` → N:M → `CourseBooking` (通过CourseBookingStudent)

**业务规则**：
- 课时数必须 ≥ 0
- 添加学员到课程预约时扣除课时
- 移除学员时退还课时

---

### 7. booking_coursebooking (课程预约)

**关联**：`booking_court.id` → `booking_coursebooking.court` (N:1)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| court_id | INTEGER | 外键关联Court |
| date | DATE | 预约日期 |
| start_time | TIME | 开始时间 |
| end_time | TIME | 结束时间 |
| status | VARCHAR(20) | 状态 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

**status选项**：
- `active` - 有效
- `cancelled` - 已取消（学员课时将全部退还）

**关联关系**：
- `booking.students` → 1:N → `CourseBookingStudent`

**辅助方法**：
- `get_student_count()` - 获取学员人数
- `get_total_class_hours()` - 获取总课时数

---

### 8. booking_coursebookingstudent (课程学员关联表)

**关联**：
- `booking_coursebooking.id` → `booking_coursebookingstudent.booking` (N:1)
- `booking_student.id` → `booking_coursebookingstudent.student` (N:1)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| booking_id | INTEGER | 外键关联CourseBooking |
| student_id | INTEGER | 外键关联Student |
| class_hours | INTEGER | 扣除课时数 |
| created_at | DATETIME | 创建时间 |

**唯一约束**：`unique_together: ['booking', 'student']` - 同一学员不能重复加入同一课程

**业务规则**：
- 添加学员时：从Student.total_class_hours中扣除相应课时
- 移除学员时：将对应课时退还给Student.total_class_hours

---

## 模型对应关系总结

| 模型 | 外键来源 | 说明 |
|------|---------|------|
| Profile | User (1:1) | 扩展用户类型 |
| Court | - | 场地主表 |
| CourtAvailability | Court (N:1) | 场地可用时间 |
| Booking | User (N:1), Court (N:1) | 普通用户预约 |
| Student | - | 学员信息 |
| CourseBooking | Court (N:1) | 课程预约（管理员操作） |
| CourseBookingStudent | CourseBooking (N:1), Student (N:1) | 课程-学员多对多关联 |

---

## 索引信息

| 表名 | 索引字段 |
|------|---------|
| booking_booking | (court_id, date, start_time), (user_id) |
| booking_courtavailability | (court_id, start_date, end_date) |
| booking_coursebooking | (court_id, date, start_time) |
| booking_coursebookingstudent | (booking_id, student_id) UNIQUE |

---

## 修改数据库的步骤

### 1. 修改模型 (`models.py`)

```python
# 示例：添加新字段
class Court(models.Model):
    # ... 现有字段 ...
    location = models.CharField(max_length=200, verbose_name='场地位置')  # 新增
```

### 2. 创建迁移文件

```bash
conda activate django
python manage.py makemigrations booking
```

### 3. 执行迁移

```bash
python manage.py migrate
```

### 4. 如需回滚

```bash
python manage.py migrate booking <迁移名称>
```

---

## 注意事项

1. **外键关系**：修改外键时要注意级联关系
2. **课时逻辑**：Student.total_class_hours的增减必须在同一事务中完成
3. **唯一约束**：CourseBookingStudent使用unique_together防止重复
4. **时间验证**：Booking和CourseBooking的开始/结束时间必须是整点或半点
5. **状态流转**：Booking和CourseBooking的status变更要注意业务逻辑（如取消预约、删除课程等）

---

## 相关文件

- 模型定义：`d:\Workspace\StaduimBookingSystem\booking\models.py`
- 视图逻辑：`d:\Workspace\StaduimBookingSystem\booking\views.py`
- URL路由：`d:\Workspace\StaduimBookingSystem\booking\urls.py`
- 迁移记录：`d:\Workspace\StaduimBookingSystem\booking\migrations\`
