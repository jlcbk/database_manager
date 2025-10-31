# 汽车数据处理工具 (Car Data Processing Tool)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

一个专为汽车企业认证工作员设计的智能化数据处理工具，能够自动解析Excel/PDF文件、跨表格查询数据、自动生成标准化报告。

## ✨ 主要特性

- 🔥 **智能文件解析**：自动识别不同格式的Excel和PDF文件
- 🔍 **跨表格查询**：一键查找跨文件的关联数据
- 📄 **自动报告生成**：根据模板自动填写并生成标准化报告
- 🎯 **模板化系统**：可自定义解析规则和报告模板
- 💾 **数据库管理**：SQLite数据库存储，支持复杂查询
- 🖥️ **友好界面**：简洁直观的桌面应用程序

## 🏗️ 系统架构

```
汽车数据处理工具
├── 智能数据解析器 (Smart Data Parser)
│   ├── Excel解析引擎
│   ├── PDF解析引擎
│   └── AI增强识别
├── 关联数据驾驶舱 (Relational Data Cockpit)
│   ├── 跨表查询引擎
│   ├── 数据可视化
│   └── 查询历史管理
└── 一键报告生成器 (One-Click Report Generator)
    ├── 模板映射系统
    ├── 多格式输出
    └── 批量生成功能
```

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Windows/Linux/macOS

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/jlcbk/database_manager.git
   cd database_manager
   ```

2. **创建虚拟环境**（推荐）
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/macOS
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行演示**
   ```bash
   python run_demo.py
   ```

5. **启动GUI应用**

   **PyQt6现代化界面** (推荐):
   ```bash
   python run_modern.py
   ```

   **传统Tkinter界面**:
   ```bash
   python src/main.py
   ```

### 🎨 界面版本对比

| 特性 | Tkinter版本 | PyQt6版本 |
|------|-------------|------------|
| 外观现代化 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 功能丰富度 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 用户体验 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 性能表现 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 推荐使用 | 快速原型 | 生产环境 |

## 📖 使用指南

### 基础功能演示

运行演示脚本查看所有功能：
```bash
python run_demo.py
```

### GUI界面操作

1. **数据输入**：选择Excel或PDF文件进行解析
2. **数据查询**：通过VIN码、发动机型号等条件查询
3. **报告生成**：选择模板并生成标准化报告

### 命令行使用

```python
# Excel文件解析示例
from src.input_parser.excel_parser import ExcelParser

parser = ExcelParser()
result = parser.parse_file("data/vehicles.xlsx")
print(f"解析到 {len(result['structured_data'])} 种数据类型")

# 数据库查询示例
from src.database.query_engine import QueryEngine

engine = QueryEngine()
vehicle_info = engine.search_by_vin("VIN1234567890")
print(f"车辆信息: {vehicle_info}")

# 报告生成示例
from src.output_generator.report_generator import ReportGenerator

generator = ReportGenerator()
success = generator.generate_report(
    data=vehicle_data,
    template_name="vehicle_emission_report",
    output_path="report.pdf",
    output_format="pdf"
)
```

## 📁 项目结构

```
database_manager/
├── src/                        # 源代码
│   ├── main.py                # 主程序入口
│   ├── input_parser/          # 输入解析模块
│   │   ├── excel_parser.py    # Excel解析器
│   │   └── pdf_parser.py      # PDF解析器
│   ├── database/              # 数据库模块
│   │   ├── models.py          # 数据模型
│   │   └── query_engine.py    # 查询引擎
│   ├── output_generator/      # 输出生成模块
│   │   └── report_generator.py # 报告生成器
│   └── utils/                 # 工具函数
├── data/                      # 数据文件目录
├── templates/                 # 报告模板目录
├── logs/                      # 日志文件目录
├── output/                    # 输出文件目录
├── docs/                      # 文档目录
├── tests/                     # 测试文件
├── requirements.txt           # 依赖包列表
├── run_demo.py               # 功能演示脚本
├── test_basic.py             # 基础测试脚本
└── README.md                 # 项目说明
```

## ⚙️ 配置说明

### Excel解析规则配置

```json
{
  "vehicle_info": {
    "sheet_patterns": ["车辆信息", "基本信息", "Vehicle Info"],
    "field_mappings": {
      "VIN": ["VIN码", "车辆识别码", "VIN", "车架号"],
      "make": ["品牌", "制造商", "Make", "厂牌"],
      "model": ["车型", "型号", "Model", "车辆型号"]
    }
  }
}
```

### 报告模板配置

```json
{
  "vehicle_emission_report": {
    "template_file": "emission_report_template.docx",
    "fields": {
      "[VIN码]": "vin",
      "[品牌]": "make",
      "[车型]": "model",
      "[发动机型号]": "engine_code"
    }
  }
}
```

## 🔧 开发指南

### 开发环境设置

1. **安装开发依赖**
   ```bash
   pip install -r requirements.txt
   pip install pytest black flake8 mypy
   ```

2. **运行测试**
   ```bash
   python test_basic.py
   ```

3. **代码格式化**
   ```bash
   black src/
   flake8 src/
   ```

### 添加新功能

1. 在相应模块中添加功能代码
2. 编写单元测试
3. 更新文档
4. 提交Pull Request

## 📋 功能路线图

### ✅ 已完成功能
- [x] Excel文件智能解析
- [x] SQLite数据库集成
- [x] 基础查询功能
- [x] Excel报告生成
- [x] 桌面GUI界面
- [x] 配置化规则引擎

### 🚧 开发中功能
- [ ] PDF文件OCR解析
- [ ] AI增强字段识别
- [ ] Word/PDF报告生成
- [ ] 批量处理功能
- [ ] 用户权限管理

### 📅 计划功能
- [ ] Web界面版本
- [ ] 数据可视化图表
- [ ] API接口
- [ ] 多语言支持
- [ ] 云端同步

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献

1. **Fork** 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 **Pull Request**

### 贡献类型

- 🐛 Bug报告和修复
- ✨ 新功能开发
- 📝 文档改进
- 🎨 UI/UX优化
- ⚡ 性能优化

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [pandas](https://pandas.pydata.org/) - 数据处理
- [openpyxl](https://openpyxl.readthedocs.io/) - Excel文件操作
- [SQLAlchemy](https://www.sqlalchemy.org/) - 数据库ORM
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - GUI界面

## 📞 联系方式

- 项目维护者：[您的姓名]
- 邮箱：[your.email@example.com]
- 项目地址：[https://github.com/your-username/car-data-processor]

## 🌟 Star History

如果这个项目对您有帮助，请给它一个 ⭐️！

[![Star History Chart](https://api.star-history.com/svg?repos=your-username/car-data-processor&type=Date)](https://star-history.com/#your-username/car-data-processor&Date)

---

⚡ **让汽车数据处理变得简单高效！**