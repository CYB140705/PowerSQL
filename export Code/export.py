

"""
当你打开此项目时，你会发现"export.py"未被我转换为"export.exe"文件。
因：pyinstaller无法打包此Py File,用到了无法支持打包的第三方python库
"""

"""
因为作者不会SQL语句，所以请自行探索!
"""


import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import sqlite3
import os

class ExcelExporter:
    def __init__(self, root):
        self.root = root
        self.root.title("数据库导出工具 v1.0")
        self.setup_ui()
        
    def setup_ui(self):
        # 数据库连接配置
        tk.Label(self.root, text="数据库路径:").grid(row=0, column=0, padx=5, pady=5)
        self.db_path = tk.Entry(self.root, width=40)
        self.db_path.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.root, text="浏览", command=self.browse_db).grid(row=0, column=2, padx=5, pady=5)
        
        # SQL查询区域
        tk.Label(self.root, text="SQL查询语句:").grid(row=1, column=0, padx=5, pady=5)
        self.sql_entry = tk.Text(self.root, height=5, width=50)
        self.sql_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        self.sql_entry.insert(tk.END, "SELECT * FROM table_name")
        
        # 导出选项
        tk.Label(self.root, text="导出选项:").grid(row=2, column=0, padx=5, pady=5)
        self.export_var = tk.StringVar(value="xlsx")
        tk.Radiobutton(self.root, text="Excel(.xlsx)", variable=self.export_var, value="xlsx").grid(row=2, column=1, sticky="w")
        tk.Radiobutton(self.root, text="CSV(.csv)", variable=self.export_var, value="csv").grid(row=2, column=2, sticky="w")
        
        # 导出按钮
        tk.Button(self.root, text="导出数据", command=self.export_data, bg="green", fg="white").grid(row=3, column=1, pady=10)
    
    def browse_db(self):
        filepath = filedialog.askopenfilename(filetypes=[("SQLite数据库", "*.db *.sqlite")])
        if filepath:
            self.db_path.delete(0, tk.END)
            self.db_path.insert(0, filepath)
    
    def export_data(self):
        try:
            db_file = self.db_path.get()
            if not os.path.exists(db_file):
                raise FileNotFoundError("数据库文件不存在")
            
            sql = self.sql_entry.get("1.0", tk.END).strip()
            if not sql:
                raise ValueError("SQL查询语句不能为空")
            
            # 连接数据库并执行查询
            conn = sqlite3.connect(db_file)
            df = pd.read_sql(sql, conn)
            conn.close()
            
            if df.empty:
                messagebox.showwarning("警告", "查询结果为空")
                return
            
            # 选择保存路径
            file_ext = self.export_var.get()
            save_path = filedialog.asksaveasfilename(
                defaultextension=f".{file_ext}",
                filetypes=[("Excel文件", "*.xlsx"), ("CSV文件", "*.csv")]
            )
            
            if save_path:
                if file_ext == "xlsx":
                    df.to_excel(save_path, index=False, engine="openpyxl")
                else:
                    df.to_csv(save_path, index=False)
                
                messagebox.showinfo("成功", f"数据已成功导出到:\n{save_path}")
        
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExcelExporter(root)
    root.mainloop()
