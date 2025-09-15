"""
作者: CYB140705

"""

import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

class DatabaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PowerSQL数据库系统 v1.0")
        self.db_name = "default_PowerSQL.db"
        self.conn = None
        
        # 初始化UI组件
        self.setup_ui()
        self.connect_db()
    
    def setup_ui(self):
        # 数据库名称输入框
        tk.Label(self.root, text="数据库文件:").grid(row=0, column=0, padx=5, pady=5)
        self.db_entry = tk.Entry(self.root)
        self.db_entry.grid(row=0, column=1, padx=5, pady=5)
        self.db_entry.insert(0, self.db_name)
        
        # 操作按钮
        tk.Button(self.root, text="连接数据库", command=self.connect_db).grid(row=0, column=2, padx=5, pady=5)
        
        # 键值操作区域
        tk.Label(self.root, text="键:").grid(row=1, column=0, padx=5, pady=5)
        self.key_entry = tk.Entry(self.root)
        self.key_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(self.root, text="值:").grid(row=2, column=0, padx=5, pady=5)
        self.value_entry = tk.Entry(self.root)
        self.value_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # 操作按钮
        tk.Button(self.root, text="插入", command=self.insert).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(self.root, text="查询", command=self.get).grid(row=3, column=1, padx=5, pady=5)
        tk.Button(self.root, text="更新", command=self.update).grid(row=4, column=0, padx=5, pady=5)
        tk.Button(self.root, text="删除", command=self.delete).grid(row=4, column=1, padx=5, pady=5)
        
        # 数据显示区域
        self.text_area = tk.Text(self.root, height=10, width=50)
        self.text_area.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
    
    def connect_db(self):
        self.db_name = self.db_entry.get()
        try:
            # 确保文件扩展名是.db
            if not self.db_name.endswith('.db'):
                self.db_name += '.db'
            
            # 连接数据库
            self.conn = sqlite3.connect(self.db_name)
            cursor = self.conn.cursor()
            
            # 创建表(如果不存在)
            cursor.execute('''CREATE TABLE IF NOT EXISTS key_value
                            (key TEXT PRIMARY KEY, value TEXT)''')
            self.conn.commit()
            
            self.update_display()
            messagebox.showinfo("成功", f"数据库 {self.db_name} 连接成功")
        except Exception as e:
            messagebox.showerror("错误", f"连接失败: {str(e)}")
    
    def update_display(self):
        self.text_area.delete(1.0, tk.END)
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM key_value")
            rows = cursor.fetchall()
            for row in rows:
                self.text_area.insert(tk.END, f"{row[0]}: {row[1]}\n")
    
    def insert(self):
        key = self.key_entry.get()
        value = self.value_entry.get()
        if key and value and self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO key_value VALUES (?, ?)", (key, value))
                self.conn.commit()
                self.update_display()
                messagebox.showinfo("成功", f"已插入: {key} => {value}")
            except sqlite3.IntegrityError:
                messagebox.showwarning("警告", "键已存在")
            except Exception as e:
                messagebox.showerror("错误", f"插入失败: {str(e)}")
        else:
            messagebox.showwarning("警告", "键和值都不能为空")
    
    def get(self):
        key = self.key_entry.get()
        if key and self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT value FROM key_value WHERE key=?", (key,))
            result = cursor.fetchone()
            if result:
                messagebox.showinfo("查询结果", f"{key}: {result[0]}")
            else:
                messagebox.showinfo("查询结果", "键不存在")
    
    def update(self):
        key = self.key_entry.get()
        value = self.value_entry.get()
        if key and value and self.conn:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE key_value SET value=? WHERE key=?", (value, key))
            if cursor.rowcount > 0:
                self.conn.commit()
                self.update_display()
                messagebox.showinfo("成功", f"已更新: {key} => {value}")
            else:
                messagebox.showwarning("警告", "键不存在")
    
    def delete(self):
        key = self.key_entry.get()
        if key and self.conn:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM key_value WHERE key=?", (key,))
            if cursor.rowcount > 0:
                self.conn.commit()
                self.update_display()
                messagebox.showinfo("成功", f"已删除: {key}")
            else:
                messagebox.showwarning("警告", "键不存在")
    
    def __del__(self):
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseGUI(root)
    root.mainloop()
