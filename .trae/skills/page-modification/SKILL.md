---
name: "page-modification"
description: "Guides page modification for the stadium booking system. Invoke when modifying any template in booking/templates/booking/ to ensure consistent design and component usage."
---

# 页面修改指南 - 体育场馆预约系统

## 触发条件

当用户要求修改 `booking/templates/booking/` 目录下的任何页面时，自动触发此skill。

## 项目页面结构

### 目录结构
```
booking/templates/booking/
├── base.html                    # 基础模板，包含统一CSS和导航
├── login.html                   # 登录页面
├── includes/                    # 公共组件目录
│   ├── page_header.html         # 页面头部组件
│   ├── stat_card.html           # 统计卡片组件
│   ├── data_table.html          # 数据表格组件
│   └── empty_state.html         # 空状态组件
├── 用户页面
│   ├── court_list.html          # 场地列表（矩阵视图）
│   ├── my_bookings.html         # 我的预约
│   └── booking_form.html        # 预约表单
└── 管理页面
    ├── admin_dashboard.html     # 管理后台
    ├── admin_court_list.html    # 场地管理
    ├── admin_court_form.html    # 场地表单
    ├── admin_student_list.html  # 学员管理
    ├── admin_student_form.html  # 学员表单
    ├── admin_bookings.html      # 预约管理
    ├── admin_booking_form.html  # 预约表单
    ├── admin_booking_edit.html  # 预约编辑
    ├── admin_availability_list.html    # 时间段管理
    ├── admin_availability_form.html    # 时间段表单
    ├── admin_course_booking_list.html  # 课程预约管理
    ├── admin_course_booking_form.html  # 课程预约表单
    ├── admin_course_booking_edit.html  # 课程预约编辑
    ├── admin_statistics.html    # 数据统计
    ├── admin_court_type_list.html      # 场地类型管理
    └── admin_court_type_form.html      # 场地类型表单
```

## 修改页面规则

### 1. 必须使用公共组件

所有页面必须使用以下公共组件：

#### 页面头部
```html
{% include 'booking/includes/page_header.html' with title="页面标题" back_url="返回链接" back_text="返回文字" %}
```

**注意**：
- 用户主页面（court_list.html、my_bookings.html）不需要 back_url
- 表单页面和编辑页面需要 back_url 返回上一级
- 管理页面返回到 /manage/dashboard/ 或相应的管理列表页

#### 统计卡片
```html
{% include 'booking/includes/stat_card.html' with value="100" label="场地总数" color="blue" icon_svg="<svg>...</svg>" %}
```

#### 空状态
```html
{% include 'booking/includes/empty_state.html' with icon="🏸" title="暂无场地" message="点击上方\"添加场地\"按钮创建第一个场地" %}
```

### 2. 禁止事项

- ❌ 不要在页面中重复定义 `.page-header`、`.back-btn` 等已在 base.html 中定义的样式
- ❌ 不要使用内联样式定义颜色值，必须使用 CSS 变量
- ❌ 不要创建与公共组件功能重复的HTML结构
- ❌ 用户页面不要添加返回首页的按钮（导航栏已有）

### 3. 必须事项

- ✅ 所有页面必须继承 `base.html`
- ✅ 使用 `.card` 包裹主要内容
- ✅ 表格使用 `.table-wrapper` 包裹支持横向滚动
- ✅ 表格标题使用 `.table-header`
- ✅ 按钮使用 `.btn` 基础类 + 颜色类（`.btn-success`、`.btn-danger` 等）

### 4. CSS 变量系统

修改页面时必须使用以下 CSS 变量：

```css
/* 主题色 */
--theme-primary: #3498db;
--theme-success: #2ecc71;
--theme-danger: #e74c3c;
--theme-warning: #f39c12;
--theme-border: #bdc3c7;
--theme-border-light: #ecf0f1;

/* 文字色 */
--text-primary: #2c3e50;
--text-secondary: #7f8c8d;

/* 背景色 */
--bg-primary: white;
--bg-secondary: #f5f5f5;
```

### 5. 响应式设计

- 页面在 768px 和 480px 有断点
- 导航链接在手机端保持横向排列
- 表格使用 `.table-wrapper` 支持横向滚动
- 所有容器都有 `width: 100%` 确保响应式

## 修改流程

1. 确认要修改的页面
2. 检查是否使用了公共组件
3. 检查是否使用了 CSS 变量而非硬编码颜色
4. 检查是否有重复的样式定义
5. 检查响应式设计是否正确
6. 确保功能逻辑不被改变
