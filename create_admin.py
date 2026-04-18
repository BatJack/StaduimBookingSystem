import os
import sys
import django
import tkinter as tk
from tkinter import ttk, messagebox

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stadium_booking.settings')
django.setup()

from django.contrib.auth.models import User


class AdminCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("创建管理员用户")
        self.root.geometry("480x480")
        self.root.resizable(False, False)
        
        # 居中显示
        self.center_window()
        
        # 设置主题颜色
        self.primary_color = "#4F46E5"
        self.bg_color = "#F9FAFB"
        self.input_bg = "#FFFFFF"
        self.border_color = "#D1D5DB"
        
        # 设置窗口背景色
        self.root.configure(bg=self.bg_color)
        
        self.setup_ui()
    
    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """设置界面"""
        # 标题
        title_frame = tk.Frame(self.root, bg=self.primary_color, height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🏸 创建管理员用户",
            font=("Microsoft YaHei", 16, "bold"),
            fg="white",
            bg=self.primary_color
        )
        title_label.pack(pady=15)
        
        # 表单区域
        form_frame = tk.Frame(self.root, bg=self.bg_color)
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 用户名
        tk.Label(
            form_frame,
            text="用户名",
            font=("Microsoft YaHei", 10),
            fg="#374151",
            bg=self.bg_color
        ).pack(anchor="w", pady=(10, 5))

        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(
            form_frame,
            textvariable=self.username_var,
            font=("Microsoft YaHei", 11),
            bg=self.input_bg,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=self.primary_color
        )
        self.username_entry.pack(fill="x", ipady=8)

        # 邮箱
        tk.Label(
            form_frame,
            text="邮箱",
            font=("Microsoft YaHei", 10),
            fg="#374151",
            bg=self.bg_color
        ).pack(anchor="w", pady=(10, 5))

        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(
            form_frame,
            textvariable=self.email_var,
            font=("Microsoft YaHei", 11),
            bg=self.input_bg,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=self.primary_color
        )
        self.email_entry.pack(fill="x", ipady=8)

        # 密码
        tk.Label(
            form_frame,
            text="密码",
            font=("Microsoft YaHei", 10),
            fg="#374151",
            bg=self.bg_color
        ).pack(anchor="w", pady=(10, 5))

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            form_frame,
            textvariable=self.password_var,
            font=("Microsoft YaHei", 11),
            bg=self.input_bg,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor=self.primary_color,
            show="*"
        )
        self.password_entry.pack(fill="x", ipady=8)
        
        # 按钮区域
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(fill="x", padx=30, pady=(10, 20))
        
        # 创建按钮
        self.create_btn = tk.Button(
            btn_frame,
            text="创建管理员",
            font=("Microsoft YaHei", 11, "bold"),
            fg="white",
            bg=self.primary_color,
            activebackground="#4338CA",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            bd=0,
            command=self.create_admin
        )
        self.create_btn.pack(fill="x", ipady=10)
        
        # 取消按钮
        cancel_btn = tk.Button(
            btn_frame,
            text="取消",
            font=("Microsoft YaHei", 10),
            fg="#6B7280",
            bg="white",
            activebackground="#F3F4F6",
            activeforeground="#374151",
            relief="solid",
            bd=1,
            cursor="hand2",
            command=self.root.destroy
        )
        cancel_btn.pack(fill="x", ipady=8, pady=(10, 0))
        
        # 绑定回车键
        self.root.bind('<Return>', lambda e: self.create_admin())
        
        # 默认聚焦用户名输入框
        self.username_entry.focus()
    
    def create_admin(self):
        """创建管理员"""
        username = self.username_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_var.get()
        
        # 验证输入
        if not username:
            messagebox.showwarning("提示", "请输入用户名")
            self.username_entry.focus()
            return
        
        if not password:
            messagebox.showwarning("提示", "请输入密码")
            self.password_entry.focus()
            return
        
        if len(password) < 6:
            messagebox.showwarning("提示", "密码长度至少为6位")
            self.password_entry.focus()
            return
        
        try:
            # 检查用户是否已存在
            if User.objects.filter(username=username).exists():
                messagebox.showinfo("提示", f"管理员用户 '{username}' 已存在")
                return
            
            # 创建管理员
            User.objects.create_superuser(username=username, password=password, email=email)
            
            messagebox.showinfo("成功", f"管理员用户创建成功！\n\n用户名: {username}\n密码: {password}")
            
            # 清空表单
            self.username_var.set("")
            self.email_var.set("")
            self.password_var.set("")
            self.username_entry.focus()
            
        except Exception as e:
            messagebox.showerror("错误", f"创建失败：{str(e)}")


def main():
    root = tk.Tk()
    app = AdminCreatorApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
