# 体育场馆预约系统 - 数据库结构文档

## 数据库概述

- **数据库类型**：SQLite3
- **Django版本**：6.0
- **数据库文件**：`db.sqlite3`

---

## 数据表关系图

```
User ← Profile (1:1)
CourtType ← Court (1:N)
Court ← CourtAvailability (1:N)
Court ← Booking → User (N:1, N:1)
Booking ← BookingStudent → Student (1:N, N:1)
```

---

## 数据表详细说明

### 1. booking_courttype (场地类型)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| name | VARCHAR(50) | 类型名称（唯一） |
| is_default | BOOLEAN | 是否系统默认 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

**默认数据**：篮球场、网球场、羽毛球场、匹克球场、台球场

---

### 2. booking_court (场地表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| court_type_id | INTEGER | 外键关联CourtType（可空） |
| name | VARCHAR(100) | 场地名称 |
| court_number | VARCHAR(20) | 场地编号 |
| description | TEXT | 场地描述 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

**排序**：按场地类型名称、场地编号、id排序

---

### 3. booking_courtavailability (场地可用时间段)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| court_id | INTEGER | 外键关联Court |
| start_date | DATE | 可预约开始日期 |
| end_date | DATE | 可预约结束日期 |
| start_time | TIME | 每天开始时间 |
| end_time | TIME | 每天结束时间 |

---

### 4. booking_booking (预约表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| booking_type | VARCHAR(20) | 预约类型（court/course） |
| user_id | INTEGER | 外键关联User（可空） |
| court_id | INTEGER | 外键关联Court |
| date | DATE | 预约日期 |
| start_time | TIME | 开始时间 |
| end_time | TIME | 结束时间 |
| booker_name | VARCHAR(100) | 预约人姓名 |
| booker_phone | VARCHAR(20) | 预约人联系方式 |
| status | VARCHAR(20) | 状态（active/cancelled） |

---

### 5. booking_student (学员信息)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| name | VARCHAR(100) | 学员姓名 |
| phone | VARCHAR(20) | 联系电话 |
| total_class_hours | INTEGER | 课时总数（30分钟/课时） |

---

### 6. booking_bookingstudent (预约学员关联表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| booking_id | INTEGER | 外键关联Booking |
| student_id | INTEGER | 外键关联Student |
| class_hours | INTEGER | 扣除课时数 |

**唯一约束**：`['booking', 'student']`

---

### 7. booking_profile (用户类型扩展)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| user_id | INTEGER | 外键关联User（1:1） |
| user_type | VARCHAR(20) | 用户类型（admin/regular） |

---

## 模型关系总结

| 模型 | 外键来源 | 说明 |
|------|---------|------|
| Profile | User (1:1) | 用户类型 |
| CourtType | - | 场地类型 |
| Court | CourtType (N:1) | 场地 |
| CourtAvailability | Court (N:1) | 可用时间 |
| Booking | User, Court (N:1) | 预约 |
| Student | - | 学员 |
| BookingStudent | Booking, Student (N:1) | 预约-学员关联 |

---

## 修改数据库

```bash
# 创建迁移
conda run -n django python manage.py makemigrations booking

# 执行迁移
conda run -n django python manage.py migrate
```

---

## 相关文件

- 模型：`booking/models.py`
- 视图：`booking/views.py`
- 迁移：`booking/migrations/`
