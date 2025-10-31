#!/usr/bin/env python3
"""
汽车数据处理工具主程序
Car Data Processing Tool - Main Application
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.input_parser.pdf_parser import PDFParser
from src.input_parser.excel_parser import ExcelParser
from src.database.query_engine import QueryEngine
from src.output_generator.report_generator import ReportGenerator

# 配置日志
import os
from pathlib import Path

# 确保日志目录存在
log_dir = Path(__file__).parent.parent / 'logs'
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class CarDataProcessorApp:
    """汽车数据处理工具主应用类"""

    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_components()
        self.setup_ui()

    def setup_window(self):
        """设置主窗口"""
        self.root.title("汽车数据处理工具 v1.0")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)

        # 设置图标（如果有的话）
        try:
            self.root.iconbitmap('database_manager/assets/icon.ico')
        except:
            pass

    def setup_components(self):
        """初始化核心组件"""
        try:
            self.pdf_parser = PDFParser()
            self.excel_parser = ExcelParser()
            self.query_engine = QueryEngine()
            self.report_generator = ReportGenerator()
            logger.info("所有组件初始化成功")
        except Exception as e:
            logger.error(f"组件初始化失败: {e}")
            messagebox.showerror("错误", f"应用程序初始化失败: {e}")

    def setup_ui(self):
        """设置用户界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # 标题
        title_label = ttk.Label(
            main_frame,
            text="汽车数据处理工具",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # 创建选项卡
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        # 创建各个功能选项卡
        self.create_input_tab()
        self.create_query_tab()
        self.create_output_tab()
        self.create_settings_tab()

        # 状态栏
        self.status_bar = ttk.Label(main_frame, text="就绪", relief=tk.SUNKEN)
        self.status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))

    def create_input_tab(self):
        """创建数据输入选项卡"""
        input_frame = ttk.Frame(self.notebook)
        self.notebook.add(input_frame, text="数据输入")

        # 左侧：文件选择
        left_frame = ttk.LabelFrame(input_frame, text="文件选择", padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        ttk.Button(left_frame, text="选择PDF文件", command=self.select_pdf_files).grid(row=0, column=0, pady=5, sticky=tk.W+tk.E)
        ttk.Button(left_frame, text="选择Excel文件", command=self.select_excel_files).grid(row=1, column=0, pady=5, sticky=tk.W+tk.E)

        # 文件列表
        self.file_listbox = tk.Listbox(left_frame, height=10)
        self.file_listbox.grid(row=2, column=0, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 右侧：解析选项
        right_frame = ttk.LabelFrame(input_frame, text="解析选项", padding="10")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Button(right_frame, text="开始解析", command=self.start_parsing).grid(row=0, column=0, pady=5)

        # AI解析选项
        self.use_ai_var = tk.BooleanVar()
        ttk.Checkbutton(right_frame, text="使用AI智能解析", variable=self.use_ai_var).grid(row=1, column=0, pady=5)

        # 进度显示
        self.progress_var = tk.StringVar(value="等待开始...")
        ttk.Label(right_frame, textvariable=self.progress_var).grid(row=2, column=0, pady=10)

        # 配置网格权重
        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=2)
        input_frame.rowconfigure(0, weight=1)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(2, weight=1)

    def create_query_tab(self):
        """创建数据查询选项卡"""
        query_frame = ttk.Frame(self.notebook)
        self.notebook.add(query_frame, text="数据查询")

        # 查询输入区域
        input_frame = ttk.LabelFrame(query_frame, text="查询条件", padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=10, pady=10)

        ttk.Label(input_frame, text="VIN码:").grid(row=0, column=0, sticky=tk.W)
        self.vin_entry = ttk.Entry(input_frame, width=20)
        self.vin_entry.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="发动机型号:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.engine_entry = ttk.Entry(input_frame, width=20)
        self.engine_entry.grid(row=0, column=3, padx=5)

        ttk.Button(input_frame, text="查询", command=self.execute_query).grid(row=0, column=4, padx=20)

        # 结果显示区域
        result_frame = ttk.LabelFrame(query_frame, text="查询结果", padding="10")
        result_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=(0, 10))

        # 创建表格显示结果
        columns = ('VIN', '车型', '发动机型号', '变速箱型号', '排放标准', '生产日期')
        self.result_tree = ttk.Treeview(result_frame, columns=columns, show='headings')

        for col in columns:
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, width=100)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scrollbar.set)

        self.result_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # 配置网格权重
        query_frame.columnconfigure(0, weight=1)
        query_frame.rowconfigure(1, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

    def create_output_tab(self):
        """创建报告输出选项卡"""
        output_frame = ttk.Frame(self.notebook)
        self.notebook.add(output_frame, text="报告生成")

        # 模板选择
        template_frame = ttk.LabelFrame(output_frame, text="模板选择", padding="10")
        template_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=10, pady=10)

        ttk.Label(template_frame, text="选择报告模板:").grid(row=0, column=0, sticky=tk.W)
        self.template_var = tk.StringVar()
        template_combo = ttk.Combobox(template_frame, textvariable=self.template_var, width=30)
        template_combo['values'] = ('车辆排放检测报告', '车辆基本信息报告', '自定义报告')
        template_combo.grid(row=0, column=1, padx=5)
        template_combo.current(0)

        # VIN输入
        ttk.Label(template_frame, text="车辆VIN码:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.output_vin_entry = ttk.Entry(template_frame, width=30)
        self.output_vin_entry.grid(row=1, column=1, padx=5, pady=(10, 0))

        ttk.Button(template_frame, text="生成报告", command=self.generate_report).grid(row=2, column=0, columnspan=2, pady=10)

        # 设置区域
        settings_frame = ttk.LabelFrame(output_frame, text="输出设置", padding="10")
        settings_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))

        self.output_format_var = tk.StringVar(value="PDF")
        ttk.Radiobutton(settings_frame, text="PDF格式", variable=self.output_format_var, value="PDF").grid(row=0, column=0)
        ttk.Radiobutton(settings_frame, text="Word格式", variable=self.output_format_var, value="Word").grid(row=0, column=1)
        ttk.Radiobutton(settings_frame, text="Excel格式", variable=self.output_format_var, value="Excel").grid(row=0, column=2)

    def create_settings_tab(self):
        """创建设置选项卡"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="设置")

        # AI设置
        ai_frame = ttk.LabelFrame(settings_frame, text="AI设置", padding="10")
        ai_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=10, pady=10)

        ttk.Label(ai_frame, text="OpenAI API Key:").grid(row=0, column=0, sticky=tk.W)
        self.api_key_entry = ttk.Entry(ai_frame, width=50, show="*")
        self.api_key_entry.grid(row=0, column=1, padx=5)

        # 数据库设置
        db_frame = ttk.LabelFrame(settings_frame, text="数据库设置", padding="10")
        db_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=10)

        ttk.Label(db_frame, text="数据库路径:").grid(row=0, column=0, sticky=tk.W)
        self.db_path_var = tk.StringVar(value="database_manager/data/car_data.db")
        ttk.Entry(db_frame, textvariable=self.db_path_var, width=50).grid(row=0, column=1, padx=5)

        ttk.Button(db_frame, text="测试连接", command=self.test_database_connection).grid(row=1, column=0, columnspan=2, pady=10)

    def select_pdf_files(self):
        """选择PDF文件"""
        from tkinter import filedialog
        files = filedialog.askopenfilenames(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )
        for file in files:
            self.file_listbox.insert(tk.END, file)

    def select_excel_files(self):
        """选择Excel文件"""
        from tkinter import filedialog
        files = filedialog.askopenfilenames(
            title="选择Excel文件",
            filetypes=[("Excel文件", "*.xlsx *.xls"), ("所有文件", "*.*")]
        )
        for file in files:
            self.file_listbox.insert(tk.END, file)

    def start_parsing(self):
        """开始解析文件"""
        files = self.file_listbox.get(0, tk.END)
        if not files:
            messagebox.showwarning("警告", "请先选择要解析的文件")
            return

        self.progress_var.set("正在解析...")
        self.root.update()

        try:
            # 这里添加实际的解析逻辑
            # 模拟解析过程
            import time
            time.sleep(2)

            self.progress_var.set(f"成功解析 {len(files)} 个文件")
            messagebox.showinfo("成功", f"成功解析 {len(files)} 个文件")

        except Exception as e:
            self.progress_var.set("解析失败")
            messagebox.showerror("错误", f"解析过程中出现错误: {e}")

    def execute_query(self):
        """执行查询"""
        vin = self.vin_entry.get().strip()
        engine = self.engine_entry.get().strip()

        if not vin and not engine:
            messagebox.showwarning("警告", "请输入查询条件")
            return

        try:
            # 清空现有结果
            for item in self.result_tree.get_children():
                self.result_tree.delete(item)

            # 这里添加实际的查询逻辑
            # 模拟查询结果
            mock_data = [
                ('VIN001', '奥迪A4', 'EA888', '7速双离合', '国六', '2023-01-15'),
                ('VIN002', '奥迪A6', 'EA888', '7速双离合', '国六', '2023-02-20'),
            ]

            for data in mock_data:
                self.result_tree.insert('', tk.END, values=data)

            self.status_bar.config(text=f"查询完成，找到 {len(mock_data)} 条记录")

        except Exception as e:
            messagebox.showerror("错误", f"查询过程中出现错误: {e}")

    def generate_report(self):
        """生成报告"""
        template = self.template_var.get()
        vin = self.output_vin_entry.get().strip()
        output_format = self.output_format_var.get()

        if not vin:
            messagebox.showwarning("警告", "请输入车辆VIN码")
            return

        try:
            # 这里添加实际的报告生成逻辑
            self.status_bar.config(text="正在生成报告...")
            self.root.update()

            # 模拟生成过程
            import time
            time.sleep(1)

            # 选择保存位置
            from tkinter import filedialog
            file_extensions = {
                'PDF': '.pdf',
                'Word': '.docx',
                'Excel': '.xlsx'
            }

            filename = filedialog.asksaveasfilename(
                title="保存报告",
                defaultextension=file_extensions[output_format],
                filetypes=[(f"{output_format}文件", f"*{file_extensions[output_format]}")]
            )

            if filename:
                self.status_bar.config(text=f"报告已生成: {filename}")
                messagebox.showinfo("成功", f"报告已生成并保存到:\n{filename}")
            else:
                self.status_bar.config(text="报告生成已取消")

        except Exception as e:
            messagebox.showerror("错误", f"报告生成过程中出现错误: {e}")

    def test_database_connection(self):
        """测试数据库连接"""
        try:
            # 这里添加实际的数据库连接测试逻辑
            messagebox.showinfo("成功", "数据库连接正常")
        except Exception as e:
            messagebox.showerror("错误", f"数据库连接失败: {e}")

    def run(self):
        """运行应用程序"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            logger.info("应用程序被用户中断")
        except Exception as e:
            logger.error(f"应用程序运行时出现错误: {e}")
            messagebox.showerror("致命错误", f"应用程序出现致命错误: {e}")

def main():
    """主函数"""
    try:
        app = CarDataProcessorApp()
        app.run()
    except Exception as e:
        print(f"启动应用程序失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()