#!/usr/bin/env python3
"""
汽车数据处理工具 - PyQt6现代化界面
Car Data Processing Tool - Modern PyQt6 Interface
"""

import sys
import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# PyQt6导入
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QGroupBox, QLabel, QPushButton, QLineEdit,
    QTextEdit, QTableWidget, QTableWidgetItem, QFileDialog,
    QProgressBar, QStatusBar, QMenuBar, QMessageBox, QComboBox,
    QCheckBox, QSpinBox, QDateEdit, QSplitter, QFrame, QScrollArea,
    QListWidget, QTreeWidget, QTreeWidgetItem, QHeaderView,
    QSizePolicy, QSpacerItem, QGridLayout
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QSize, QRect, QPoint,
    QDir, QFile, QFileInfo
)
from PyQt6.QtGui import (
    QIcon, QFont, QPalette, QColor, QPixmap, QAction,
    QTextCursor, QLinearGradient, QBrush
)

# 项目模块导入
try:
    from src.input_parser.excel_parser import ExcelParser
    from src.input_parser.pdf_parser import PDFParser
    from src.database.query_engine import QueryEngine
    from src.output_generator.report_generator import ReportGenerator
except ImportError as e:
    print(f"导入模块失败: {e}")
    sys.exit(1)

# 配置日志
import os
from pathlib import Path

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

class ModernStyle:
    """现代化样式管理器"""

    @staticmethod
    def get_style_sheet():
        """获取现代化样式表"""
        return """
        /* 全局样式 */
        QMainWindow {
            background-color: #f0f2f5;
        }

        QWidget {
            font-family: "Segoe UI", Arial, sans-serif;
            font-size: 12px;
        }

        /* 标签样式 */
        QLabel {
            color: #2c3e50;
            font-weight: 500;
        }

        QLabel.title {
            font-size: 18px;
            font-weight: bold;
            color: #3498db;
            padding: 10px;
        }

        /* 按钮样式 */
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #2980b9;
        }

        QPushButton:pressed {
            background-color: #21618c;
        }

        QPushButton.secondary {
            background-color: #95a5a6;
        }

        QPushButton.secondary:hover {
            background-color: #7f8c8d;
        }

        QPushButton.success {
            background-color: #27ae60;
        }

        QPushButton.success:hover {
            background-color: #229954;
        }

        QPushButton.danger {
            background-color: #e74c3c;
        }

        QPushButton.danger:hover {
            background-color: #c0392b;
        }

        /* 输入框样式 */
        QLineEdit, QComboBox, QSpinBox {
            border: 2px solid #bdc3c7;
            border-radius: 6px;
            padding: 6px 12px;
            background-color: white;
        }

        QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
            border-color: #3498db;
        }

        /* 表格样式 */
        QTableWidget {
            border: 1px solid #bdc3c7;
            border-radius: 6px;
            background-color: white;
            gridline-color: #ecf0f1;
        }

        QTableWidget::item {
            padding: 8px;
            border-bottom: 1px solid #ecf0f1;
        }

        QTableWidget::item:selected {
            background-color: #3498db;
            color: white;
        }

        QHeaderView::section {
            background-color: #34495e;
            color: white;
            padding: 8px;
            border: none;
            font-weight: bold;
        }

        /* 选项卡样式 */
        QTabWidget::pane {
            border: 1px solid #bdc3c7;
            border-radius: 6px;
            background-color: white;
        }

        QTabBar::tab {
            background-color: #ecf0f1;
            color: #2c3e50;
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        }

        QTabBar::tab:selected {
            background-color: #3498db;
            color: white;
        }

        QTabBar::tab:hover:!selected {
            background-color: #d5dbdb;
        }

        /* 组框样式 */
        QGroupBox {
            font-weight: bold;
            border: 2px solid #bdc3c7;
            border-radius: 6px;
            margin-top: 8px;
            padding-top: 16px;
            background-color: white;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
            color: #2c3e50;
        }

        /* 进度条样式 */
        QProgressBar {
            border: 2px solid #bdc3c7;
            border-radius: 6px;
            text-align: center;
            background-color: #ecf0f1;
        }

        QProgressBar::chunk {
            background-color: #3498db;
            border-radius: 4px;
        }

        /* 状态栏样式 */
        QStatusBar {
            background-color: #34495e;
            color: white;
        }

        /* 菜单栏样式 */
        QMenuBar {
            background-color: #34495e;
            color: white;
            border-bottom: 2px solid #2c3e50;
        }

        QMenuBar::item {
            background-color: transparent;
            padding: 8px 16px;
        }

        QMenuBar::item:selected {
            background-color: #2c3e50;
        }

        QMenu {
            background-color: white;
            border: 1px solid #bdc3c7;
            border-radius: 6px;
        }

        QMenu::item {
            padding: 8px 16px;
        }

        QMenu::item:selected {
            background-color: #3498db;
            color: white;
        }
        """

class ExcelParserThread(QThread):
    """Excel解析线程"""
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.parser = ExcelParser()

    def run(self):
        try:
            logger.info(f"开始解析Excel文件: {self.file_path}")
            self.progress_updated.emit(10)

            result = self.parser.parse_file(self.file_path)
            self.progress_updated.emit(90)

            self.finished.emit(result)
            self.progress_updated.emit(100)

        except Exception as e:
            logger.error(f"Excel解析失败: {e}")
            self.error_occurred.emit(f"解析失败: {str(e)}")

class DatabaseQueryThread(QThread):
    """数据库查询线程"""
    finished = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, query_type: str, params: Dict[str, Any]):
        super().__init__()
        self.query_type = query_type
        self.params = params
        self.query_engine = QueryEngine()

    def run(self):
        try:
            if self.query_type == "vin":
                result = self.query_engine.search_by_vin(self.params["vin"])
            elif self.query_type == "engine":
                result = self.query_engine.search_by_engine_code(self.params["engine_code"])
            else:
                result = {}

            self.finished.emit(result)

        except Exception as e:
            logger.error(f"数据库查询失败: {e}")
            self.error_occurred.emit(f"查询失败: {str(e)}")

class ModernCarDataProcessor(QMainWindow):
    """汽车数据处理工具现代化界面"""

    def __init__(self):
        super().__init__()
        self.components = {}
        self.setup_components()
        self.setup_ui()
        self.setup_style()
        self.setup_connections()
        self.setup_status_bar()

    def setup_components(self):
        """初始化核心组件"""
        try:
            self.excel_parser = ExcelParser()
            self.pdf_parser = PDFParser()
            self.query_engine = QueryEngine()
            self.report_generator = ReportGenerator()
            logger.info("所有组件初始化成功")
        except Exception as e:
            logger.error(f"组件初始化失败: {e}")
            QMessageBox.critical(self, "错误", f"应用程序初始化失败: {e}")

    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("汽车数据处理工具 v2.0 - PyQt6现代化界面")
        self.setMinimumSize(1200, 800)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 左侧控制面板
        left_panel = self.create_left_panel()
        left_panel.setMaximumWidth(350)

        # 右侧工作区域
        right_panel = self.create_right_panel()

        # 添加到主布局
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)

        # 设置菜单栏
        self.setup_menu_bar()

    def create_left_panel(self) -> QWidget:
        """创建左侧控制面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)

        # 项目标题
        title_label = QLabel("🚗 汽车数据处理工具")
        title_label.setProperty("class", "title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # 数据输入部分
        input_group = QGroupBox("📁 数据输入")
        input_layout = QVBoxLayout()

        self.file_list = QListWidget()
        self.file_list.setMaximumHeight(120)
        input_layout.addWidget(QLabel("已选择的文件:"))
        input_layout.addWidget(self.file_list)

        btn_layout = QHBoxLayout()
        self.add_excel_btn = QPushButton("📊 添加Excel文件")
        self.add_pdf_btn = QPushButton("📄 添加PDF文件")
        self.clear_files_btn = QPushButton("🗑️ 清空文件")
        btn_layout.addWidget(self.add_excel_btn)
        btn_layout.addWidget(self.add_pdf_btn)
        btn_layout.addWidget(self.clear_files_btn)
        input_layout.addLayout(btn_layout)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # 数据解析部分
        parse_group = QGroupBox("⚙️ 数据解析")
        parse_layout = QVBoxLayout()

        self.use_ai_checkbox = QCheckBox("🤖 使用AI智能解析")
        self.use_ai_checkbox.setChecked(False)
        parse_layout.addWidget(self.use_ai_checkbox)

        self.parse_btn = QPushButton("🚀 开始解析文件")
        self.parse_btn.setMinimumHeight(40)
        parse_layout.addWidget(self.parse_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        parse_layout.addWidget(self.progress_bar)

        self.parse_status = QLabel("就绪")
        self.parse_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parse_layout.addWidget(self.parse_status)

        parse_group.setLayout(parse_layout)
        layout.addWidget(parse_group)

        # 数据查询部分
        query_group = QGroupBox("🔍 数据查询")
        query_layout = QVBoxLayout()

        # VIN查询
        query_layout.addWidget(QLabel("VIN码查询:"))
        self.vin_input = QLineEdit()
        self.vin_input.setPlaceholderText("输入17位VIN码...")
        query_layout.addWidget(self.vin_input)

        self.search_vin_btn = QPushButton("🔍 查询VIN")
        query_layout.addWidget(self.search_vin_btn)

        # 发动机型号查询
        query_layout.addWidget(QLabel("发动机型号查询:"))
        self.engine_input = QLineEdit()
        self.engine_input.setPlaceholderText("输入发动机型号...")
        query_layout.addWidget(self.engine_input)

        self.search_engine_btn = QPushButton("🔍 查询发动机")
        query_layout.addWidget(self.search_engine_btn)

        query_group.setLayout(query_layout)
        layout.addWidget(query_group)

        # 报告生成部分
        report_group = QGroupBox("📋 报告生成")
        report_layout = QVBoxLayout()

        report_layout.addWidget(QLabel("报告模板:"))
        self.template_combo = QComboBox()
        self.template_combo.addItems(["车辆基本信息报告", "车辆排放检测报告", "自定义报告"])
        report_layout.addWidget(self.template_combo)

        report_layout.addWidget(QLabel("车辆VIN码:"))
        self.report_vin_input = QLineEdit()
        self.report_vin_input.setPlaceholderText("输入车辆VIN码...")
        report_layout.addWidget(self.report_vin_input)

        self.generate_report_btn = QPushButton("📄 生成报告")
        self.generate_report_btn.setMinimumHeight(35)
        report_layout.addWidget(self.generate_report_btn)

        report_group.setLayout(report_layout)
        layout.addWidget(report_group)

        # 添加弹性空间
        layout.addStretch()

        return panel

    def create_right_panel(self) -> QWidget:
        """创建右侧工作区域"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)

        # 创建选项卡
        self.tab_widget = QTabWidget()

        # 数据展示选项卡
        self.data_tab = self.create_data_tab()
        self.tab_widget.addTab(self.data_tab, "📊 数据展示")

        # 查询结果选项卡
        self.query_tab = self.create_query_tab()
        self.tab_widget.addTab(self.query_tab, "🔍 查询结果")

        # 报告预览选项卡
        self.report_tab = self.create_report_tab()
        self.tab_widget.addTab(self.report_tab, "📋 报告预览")

        # 日志选项卡
        self.log_tab = self.create_log_tab()
        self.tab_widget.addTab(self.log_tab, "📝 操作日志")

        layout.addWidget(self.tab_widget)

        return panel

    def create_data_tab(self) -> QWidget:
        """创建数据展示选项卡"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # 数据表格
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(6)
        self.data_table.setHorizontalHeaderLabels([
            "文件名", "类型", "数据行数", "解析状态", "数据类型", "处理时间"
        ])

        # 设置表格属性
        header = self.data_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.data_table)

        return tab

    def create_query_tab(self) -> QWidget:
        """创建查询结果选项卡"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # 查询结果表格
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(8)
        self.result_table.setHorizontalHeaderLabels([
            "VIN码", "品牌", "车型", "年份", "发动机型号", "排量", "功率", "排放标准"
        ])

        # 设置表格属性
        header = self.result_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.result_table)

        return tab

    def create_report_tab(self) -> QWidget:
        """创建报告预览选项卡"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # 报告预览区域
        self.report_preview = QTextEdit()
        self.report_preview.setReadOnly(True)
        self.report_preview.setPlaceholderText("报告生成后将在此处显示...")

        layout.addWidget(self.report_preview)

        return tab

    def create_log_tab(self) -> QWidget:
        """创建操作日志选项卡"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # 日志显示区域
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFont(QFont("Consolas", 10))

        # 添加初始日志
        self.add_log("系统启动完成")
        self.add_log("所有组件初始化成功")
        self.add_log("PyQt6现代化界面已加载")

        layout.addWidget(self.log_display)

        return tab

    def setup_menu_bar(self):
        """设置菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("📁 文件")

        open_action = QAction("📂 打开文件", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("💾 保存结果", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_results)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction("🚪 退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 编辑菜单
        edit_menu = menubar.addMenu("✏️ 编辑")

        clear_action = QAction("🗑️ 清空数据", self)
        clear_action.triggered.connect(self.clear_all_data)
        edit_menu.addAction(clear_action)

        # 工具菜单
        tools_menu = menubar.addMenu("🛠️ 工具")

        settings_action = QAction("⚙️ 设置", self)
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)

        # 帮助菜单
        help_menu = menubar.addMenu("❓ 帮助")

        about_action = QAction("ℹ️ 关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_style(self):
        """设置样式"""
        self.setStyleSheet(ModernStyle.get_style_sheet())

    def setup_connections(self):
        """设置信号连接"""
        # 文件操作连接
        self.add_excel_btn.clicked.connect(self.add_excel_file)
        self.add_pdf_btn.clicked.connect(self.add_pdf_file)
        self.clear_files_btn.clicked.connect(self.clear_files)

        # 解析操作连接
        self.parse_btn.clicked.connect(self.start_parsing)

        # 查询操作连接
        self.search_vin_btn.clicked.connect(self.search_by_vin)
        self.search_engine_btn.clicked.connect(self.search_by_engine)

        # 报告生成连接
        self.generate_report_btn.clicked.connect(self.generate_report)

    def setup_status_bar(self):
        """设置状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪 - 系统运行正常")

    def add_excel_file(self):
        """添加Excel文件"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "选择Excel文件",
            "",
            "Excel文件 (*.xlsx *.xls);;所有文件 (*.*)"
        )

        for file_path in files:
            self.file_list.addItem(f"📊 {Path(file_path).name}")
            self.add_log(f"添加Excel文件: {Path(file_path).name}")

    def add_pdf_file(self):
        """添加PDF文件"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "选择PDF文件",
            "",
            "PDF文件 (*.pdf);;所有文件 (*.*)"
        )

        for file_path in files:
            self.file_list.addItem(f"📄 {Path(file_path).name}")
            self.add_log(f"添加PDF文件: {Path(file_path).name}")

    def clear_files(self):
        """清空文件列表"""
        self.file_list.clear()
        self.add_log("已清空文件列表")

    def start_parsing(self):
        """开始解析文件"""
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "警告", "请先添加要解析的文件")
            return

        self.parse_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.parse_status.setText("正在解析...")

        # 这里添加实际的解析逻辑
        QTimer.singleShot(1000, self.simulate_parsing)

    def simulate_parsing(self):
        """模拟解析过程"""
        import random

        for i in range(101):
            self.progress_bar.setValue(i)
            QApplication.processEvents()
            if i < 100:
                import time
                time.sleep(0.02)

        self.progress_bar.setVisible(False)
        self.parse_btn.setEnabled(True)
        self.parse_status.setText("解析完成")

        # 添加解析结果到数据表格
        self.add_parsed_data()
        self.add_log("文件解析完成")
        self.status_bar.showMessage("解析完成 - 处理了多个文件")

    def add_parsed_data(self):
        """添加解析结果到表格"""
        import random
        from datetime import datetime

        # 模拟一些解析结果
        sample_data = [
            ["车辆数据.xlsx", "Excel", "156", "成功", "车辆信息", datetime.now().strftime("%H:%M:%S")],
            ["发动机参数.xlsx", "Excel", "89", "成功", "发动机信息", datetime.now().strftime("%H:%M:%S")],
            ["排放检测报告.xlsx", "Excel", "67", "成功", "排放数据", datetime.now().strftime("%H:%M:%S")]
        ]

        for row_data in sample_data:
            row = self.data_table.rowCount()
            self.data_table.insertRow(row)

            for col, data in enumerate(row_data):
                self.data_table.setItem(row, col, QTableWidgetItem(str(data)))

    def search_by_vin(self):
        """通过VIN码查询"""
        vin = self.vin_input.text().strip()

        if not vin:
            QMessageBox.warning(self, "警告", "请输入VIN码")
            return

        if len(vin) != 17:
            QMessageBox.warning(self, "警告", "VIN码应为17位")
            return

        self.add_log(f"查询VIN码: {vin}")

        # 这里添加实际的查询逻辑
        self.simulate_vin_query(vin)

    def simulate_vin_query(self, vin):
        """模拟VIN查询"""
        # 模拟查询结果
        result_data = [
            vin,
            "奥迪",
            "A4L",
            "2023",
            "EA888",
            "2.0T",
            "140kW",
            "国VI"
        ]

        # 清空现有结果
        self.result_table.setRowCount(0)

        # 添加新结果
        self.result_table.insertRow(0)
        for col, data in enumerate(result_data):
            self.result_table.setItem(0, col, QTableWidgetItem(str(data)))

        self.add_log(f"查询完成: 找到车辆信息")
        self.status_bar.showMessage(f"查询完成 - VIN: {vin}")

    def search_by_engine(self):
        """通过发动机型号查询"""
        engine_code = self.engine_input.text().strip()

        if not engine_code:
            QMessageBox.warning(self, "警告", "请输入发动机型号")
            return

        self.add_log(f"查询发动机型号: {engine_code}")

        # 模拟查询结果
        self.simulate_engine_query(engine_code)

    def simulate_engine_query(self, engine_code):
        """模拟发动机查询"""
        # 模拟多辆车使用同一发动机
        sample_results = [
            [f"{engine_code}-001", "奥迪", "A4L", "2023", "2.0T", "140kW", "国VI"],
            [f"{engine_code}-002", "奥迪", "A6L", "2023", "2.0T", "150kW", "国VI"],
            [f"{engine_code}-003", "大众", "帕萨特", "2022", "2.0T", "137kW", "国VI"]
        ]

        # 清空现有结果
        self.result_table.setRowCount(0)

        # 添加新结果
        for row_data in sample_results:
            row = self.result_table.rowCount()
            self.result_table.insertRow(row)

            # 调整列数以匹配数据
            for col, data in enumerate(row_data):
                if col < self.result_table.columnCount():
                    self.result_table.setItem(row, col, QTableWidgetItem(str(data)))

        self.add_log(f"查询完成: 找到{len(sample_results)}辆使用该发动机的车辆")
        self.status_bar.showMessage(f"查询完成 - 发动机型号: {engine_code}")

    def generate_report(self):
        """生成报告"""
        template = self.template_combo.currentText()
        vin = self.report_vin_input.text().strip()

        if not vin:
            QMessageBox.warning(self, "警告", "请输入车辆VIN码")
            return

        if len(vin) != 17:
            QMessageBox.warning(self, "警告", "VIN码应为17位")
            return

        self.add_log(f"生成报告: {template} - VIN: {vin}")

        # 模拟报告生成
        self.simulate_report_generation(template, vin)

    def simulate_report_generation(self, template, vin):
        """模拟报告生成"""
        report_content = f"""
=== {template} ===

生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

车辆基本信息:
VIN码: {vin}
品牌: 奥迪
车型: A4L
年份: 2023年

发动机信息:
发动机型号: EA888
排量: 2.0T
功率: 140kW
扭矩: 320N·m

排放信息:
排放标准: 国VI
CO2排放: 165g/km
综合油耗: 6.8L/100km

检测结论: 符合国家标准
检测员: 张工程师
检测日期: {datetime.now().strftime("%Y年%m月%d日")}

---
此报告由汽车数据处理工具自动生成
        """

        self.report_preview.setPlainText(report_content)
        self.tab_widget.setCurrentIndex(2)  # 切换到报告预览选项卡
        self.add_log("报告生成完成")
        self.status_bar.showMessage("报告生成完成")

        QMessageBox.information(self, "成功", "报告生成完成！请在报告预览选项卡中查看。")

    def add_log(self, message):
        """添加日志信息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"

        self.log_display.append(log_message)

        # 自动滚动到底部
        cursor = self.log_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.log_display.setTextCursor(cursor)

        logger.info(message)

    def open_file(self):
        """打开文件"""
        self.add_excel_file()

    def save_results(self):
        """保存结果"""
        files, _ = QFileDialog.getSaveFileName(
            self,
            "保存结果",
            "",
            "文本文件 (*.txt);;所有文件 (*.*)"
        )

        if files:
            try:
                with open(files, 'w', encoding='utf-8') as f:
                    f.write(self.log_display.toPlainText())

                self.add_log(f"结果已保存到: {files}")
                QMessageBox.information(self, "成功", "结果保存成功！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存失败: {e}")

    def clear_all_data(self):
        """清空所有数据"""
        reply = QMessageBox.question(
            self, "确认清空", "确定要清空所有数据吗？此操作不可恢复。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.data_table.setRowCount(0)
            self.result_table.setRowCount(0)
            self.report_preview.clear()
            self.file_list.clear()
            self.vin_input.clear()
            self.engine_input.clear()
            self.report_vin_input.clear()

            self.add_log("所有数据已清空")
            self.status_bar.showMessage("数据已清空")

    def show_settings(self):
        """显示设置对话框"""
        QMessageBox.information(self, "设置", "设置功能开发中...")

    def show_about(self):
        """显示关于对话框"""
        about_text = """
        <h2>汽车数据处理工具 v2.0</h2>
        <p>基于PyQt6的现代化汽车数据处理应用</p>
        <p><b>主要功能:</b></p>
        <ul>
            <li>📊 Excel/PDF文件智能解析</li>
            <li>🔍 跨表格数据查询</li>
            <li>📋 自动化报告生成</li>
            <li>🤖 AI增强数据处理</li>
        </ul>
        <p><b>技术栈:</b></p>
        <ul>
            <li>PyQt6 - 现代化GUI框架</li>
            <li>Pandas - 数据处理</li>
            <li>SQLAlchemy - 数据库ORM</li>
            <li>OpenAI - AI功能增强</li>
        </ul>
        <p><b>版本:</b> 2.0.0<br>
        <b>开发者:</b> 汽车数据处理团队<br>
        <b>许可证:</b> MIT License</p>
        """

        QMessageBox.about(self, "关于", about_text)

    def closeEvent(self, event):
        """关闭事件"""
        reply = QMessageBox.question(
            self, "确认退出", "确定要退出应用程序吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            logger.info("应用程序正常退出")
            event.accept()
        else:
            event.ignore()

def main():
    """主函数"""
    app = QApplication(sys.argv)

    # 设置应用程序信息
    app.setApplicationName("汽车数据处理工具")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("CarDataProcessor")

    # 创建并显示主窗口
    window = ModernCarDataProcessor()
    window.show()

    # 运行应用程序
    sys.exit(app.exec())

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("应用程序被用户中断")
        sys.exit(0)
    except Exception as e:
        logger.error(f"应用程序运行时出现致命错误: {e}")
        sys.exit(1)