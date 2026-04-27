---
name: "database-modification"
description: "Guides database modification for the stadium booking system. Invoke when user asks to modify/add/delete models, fields, or run migrations."
---

# 数据库修改指南

本Skill用于指导体育场馆预约系统的数据库修改操作。

## 触发条件

**必须调用此Skill的场景**：
- 用户要求修改数据模型（models.py）
- 用户要求添加/删除字段
- 用户要求创建新的数据表
- 用户要求运行数据库迁移
- 用户询问数据库结构相关问题

## 数据库结构概览

### 核心数据表

| 表名 | 模型类 | 说明 |
|------|--------|------|
| auth_user | User | Django内置用户表 |
| booking_profile | Profile | 用户类型扩展（admin/regular） |
| booking_court | Court | 场地表 |
| booking_courtavailability | CourtAvailability | 场地可用时间段 |
| booking_booking | Booking | 普通用户预约 |
| booking_student | Student | 学员信息（含课时） |
| booking_coursebooking | CourseBooking | 课程预约（管理员操作） |
| booking_coursebookingstudent | CourseBookingStudent | 课程-学员关联表 |

### 关键外键关系

```
User ←Profile (1:1)
User ←Booking→ Court (N:1, N:1)
Court ←CourtAvailability (1:N)
Court ←CourseBooking (1:N)
CourseBooking ←CourseBookingStudent→ Student (1:N, N:1)
Student ←CourseBookingStudent→ CourseBooking (N:M)
```

### 业务逻辑要点

1. **课时系统（Student.total_class_hours）**
   - 单位：30分钟 = 1课时
   - 添加学员到课程：扣除课时 `Student.total_class_hours -= class_hours`
   - 移除学员：退还课时 `Student.total_class_hours += class_hours`
   - 删除课程预约：所有学员课时退还

2. **时间验证规则**
   - 所有预约时间（Booking、CourseBooking）必须是整点或半点
   - TimeField使用 `step=1800`（秒）

3. **状态管理**
   - Booking和CourseBooking都有status字段
   - `active` = 有效，`cancelled` = 已取消
   - 取消时根据业务逻辑处理相关数据（如退还课时）

4. **唯一约束**
   - CourseBookingStudent使用unique_together防止同一学员重复加入同一课程

## 修改数据库的标准流程

### 1. 修改模型文件

**文件路径**：`d:\Workspace\StaduimBookingSystem\booking\models.py`

```python
from django.db import models

class YourModel(models.Model):
    # 添加字段时注意：
    # - 使用合适的Field类型
    # - 设置verbose_name作为中文显示名
    # - 使用auto_now_add/auto_now处理时间字段
    # - 设置default值（如果需要）
    field_name = models.CharField(max_length=100, verbose_name='字段名称')
```

### 2. 创建迁移文件

```bash
# 激活conda环境
conda activate django

# 创建迁移文件（仅生成，不执行）
python manage.py makemigrations booking

# 查看迁移内容
python manage.py showmigrations booking
```

### 3. 执行迁移

```bash
# 执行所有待处理迁移
python manage.py migrate

# 仅执行特定应用的迁移
python manage.py migrate booking
```

### 4. 验证结果

```bash
# 进入Django shell验证
python manage.py shell

>>> from booking.models import YourModel
>>> YourModel.objects.all()
```

## 常见修改场景

### 场景1：添加新字段

```python
# models.py
class Court(models.Model):
    # 现有字段...
    location = models.CharField(max_length=200, blank=True, verbose_name='场地位置')

# 执行迁移
python manage.py makemigrations booking
python manage.py migrate
```

### 场景2：创建新模型

```python
# models.py
class NewModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')
    description = models.TextField(blank=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '新模型'
        verbose_name_plural = '新模型'

    def __str__(self):
        return self.name
```

### 场景3：删除字段

```python
# 1. 从models.py中删除字段定义
# 2. 执行迁移（会自动生成删除字段的迁移）
python manage.py makemigrations booking
python manage.py migrate
```

### 场景4：修改外键关系

修改外键时注意CASCADE策略：
- `on_delete=models.CASCADE` - 父表删除，子表级联删除
- `on_delete=models.SET_NULL` - 父表删除，子表设为NULL
- `on_delete=models.PROTECT` - 阻止删除

## 课时操作示例

### 添加学员到课程

```python
# 在views.py的admin_course_booking_edit视图中
if action == 'add_students':
    student_ids = request.POST.getlist('students')
    class_hours = int(request.POST.get('class_hours', 1))

    for student_id in student_ids:
        student = Student.objects.get(id=student_id)
        if student.total_class_hours >= class_hours:
            # 扣除课时
            student.total_class_hours -= class_hours
            student.save()

            # 创建关联记录
            CourseBookingStudent.objects.create(
                booking=booking,
                student=student,
                class_hours=class_hours
            )
```

### 移除学员（退还课时）

```python
# 在视图中处理
if action == 'remove_student':
    cs_id = request.POST.get('cs_id')
    cs = CourseBookingStudent.objects.get(id=cs_id)

    # 退还课时
    cs.student.total_class_hours += cs.class_hours
    cs.student.save()

    # 删除关联
    cs.delete()
```

### 取消课程（退还所有学员课时）

```python
if action == 'cancel_booking':
    # 退还所有学员课时
    for cs in booking.students.all():
        cs.student.total_class_hours += cs.class_hours
        cs.student.save()

    # 更新状态
    booking.status = 'cancelled'
    booking.save()
```

## 迁移回滚

```bash
# 查看迁移历史
python manage.py showmigrations booking

# 回滚到特定迁移
python manage.py migrate booking 0002_profile

# 回滚所有迁移
python manage.py migrate booking zero
```

## 注意事项

1. **先阅读文档**：修改前先查看 `.trae/docs/database-schema.md`
2. **一次一改**：每次修改尽量只涉及一个模型的变动
3. **测试验证**：执行迁移后在Django shell中验证
4. **事务处理**：涉及课时等数值变动时注意事务一致性
5. **提交前检查**：确保迁移文件已生成且正确

## 相关文件路径

- 模型定义：`d:\Workspace\StaduimBookingSystem\booking\models.py`
- 视图逻辑：`d:\Workspace\StaduimBookingSystem\booking\views.py`
- URL路由：`d:\Workspace\StaduimBookingSystem\booking\urls.py`
- 迁移目录：`d:\Workspace\StaduimBookingSystem\booking\migrations\`
- 数据库文档：`.trae/docs/database-schema.md`
