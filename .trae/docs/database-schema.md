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
│  ┌──────────┐     1:N      ┌──────────────────┐                 │
│  │  Court   │─────────────│ CourtAvailability │                 │
│  │  场地    │             │   可用时间段      │                 │
│  └──────────┘             └──────────────────┘                 │
│       │                                                        │
│       │ 1:N                                                    │
│       ▼                                                        │
│  ┌──────────────────────────────┐                             │
│  │         Booking              │                             │
│  │  预约（统一模型）             │                             │
│  │  booking_type: 场地/课程      │                             │
│  │  booker_name, booker_phone   │                             │
│  └──────────────────────────────┘                             │
│       │                                                        │
│       │ 1:N                                                    │
│       ▼                                                        │
│  ┌─────────────────────┐         ┌──────────────┐             │
│  │  BookingStudent     │────────│   Student     │             │
│  │  预约学员关系        │  N:1   │  学员信息      │             │
│  └─────────────────────┘         └──────────────┘             │
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

### 5. booking_booking (预约表 - 统一模型)

**关联**：
- `auth_user.id` → `booking_booking.user` (N:1, 可为空)
- `booking_court.id` → `booking_booking.court` (N:1)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| booking_type | VARCHAR(20) | 预约类型 |
| user_id | INTEGER | 外键关联User（可为空） |
| court_id | INTEGER | 外键关联Court |
| date | DATE | 预约日期 |
| start_time | TIME | 开始时间 |
| end_time | TIME | 结束时间 |
| booker_name | VARCHAR(100) | 预约人姓名（可为空） |
| booker_phone | VARCHAR(20) | 预约人联系方式（可为空） |
| status | VARCHAR(20) | 状态 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

**booking_type选项**：
- `court` - 场地预约
- `course` - 课程预约

**status选项**：
- `active` - 有效
- `cancelled` - 已取消

**辅助方法**：
- `is_court_booking()` - 判断是否为场地预约
- `is_course_booking()` - 判断是否为课程预约
- `get_student_count()` - 获取学员人数（课程预约使用）
- `get_total_class_hours()` - 获取总课时数（课程预约使用）

**业务规则**：
- 时间必须是整点或半点
- 不能与同一场地的其他有效预约冲突（包括场地预约和课程预约）
- 课程预约的user字段可为空

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
- `student.bookings` → N:M → `Booking` (通过BookingStudent)

**业务规则**：
- 课时数必须 ≥ 0
- 添加学员到课程预约时扣除课时
- 移除学员时退还课时

---

### 7. booking_bookingstudent (预约学员关联表)

**关联**：
- `booking_booking.id` → `booking_bookingstudent.booking` (N:1)
- `booking_student.id` → `booking_bookingstudent.student` (N:1)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| booking_id | INTEGER | 外键关联Booking |
| student_id | INTEGER | 外键关联Student |
| class_hours | INTEGER | 扣除课时数 |
| created_at | DATETIME | 创建时间 |

**唯一约束**：`unique_together: ['booking', 'student']` - 同一学员不能重复加入同一预约

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
| Booking | User (N:1, 可空), Court (N:1) | 统一预约模型（场地/课程） |
| Student | - | 学员信息 |
| BookingStudent | Booking (N:1), Student (N:1) | 预约-学员多对多关联 |

---

## 索引信息

| 表名 | 索引字段 |
|------|---------|
| booking_booking | (court_id, date, start_time), (user_id) |
| booking_courtavailability | (court_id, start_date, end_date) |
| booking_bookingstudent | (booking_id, student_id) UNIQUE |

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
3. **唯一约束**：BookingStudent使用unique_together防止重复
4. **时间验证**：Booking的开始/结束时间必须是整点或半点
5. **状态流转**：Booking的status变更要注意业务逻辑（如取消预约、删除课程等）
6. **统一预约模型**：Booking模型通过booking_type区分场地预约和课程预约，冲突检测需检查所有类型的预约
7. **预约人信息**：booker_name和booker_phone字段用于记录预约人联系方式，可为空

---

## 相关文件

- 模型定义：`d:\Workspace\StaduimBookingSystem\booking\models.py`
- 视图逻辑：`d:\Workspace\StaduimBookingSystem\booking\views.py`
- URL路由：`d:\Workspace\StaduimBookingSystem\booking\urls.py`
- 迁移记录：`d:\Workspace\StaduimBookingSystem\booking\migrations\`
