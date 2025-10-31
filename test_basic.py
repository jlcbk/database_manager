#!/usr/bin/env python3
"""
基础功能测试
Basic Functionality Test
"""

import os
import sys
import logging
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_imports():
    """测试模块导入"""
    try:
        logger.info("测试基础模块导入...")

        # 测试pandas
        import pandas as pd
        logger.info("✓ pandas 导入成功")

        # 测试openpyxl
        import openpyxl
        logger.info("✓ openpyxl 导入成功")

        # 测试SQLAlchemy
        from sqlalchemy import create_engine
        logger.info("✓ SQLAlchemy 导入成功")

        return True

    except ImportError as e:
        logger.error(f"模块导入失败: {e}")
        return False

def test_database():
    """测试数据库功能"""
    try:
        logger.info("测试数据库功能...")

        from src.database.models import init_database, get_session

        # 初始化数据库
        engine = init_database()
        logger.info("✓ 数据库初始化成功")

        # 测试连接
        session = get_session()
        # 简单测试：创建一个查询来验证连接
        from src.database.models import Vehicle
        vehicles = session.query(Vehicle).limit(1).all()
        session.close()

        logger.info("✓ 数据库连接测试成功")
        return True

    except Exception as e:
        logger.error(f"数据库测试失败: {e}")
        return False

def test_excel_parser():
    """测试Excel解析器"""
    try:
        logger.info("测试Excel解析器...")

        from src.input_parser.excel_parser import ExcelParser

        parser = ExcelParser()
        logger.info("✓ Excel解析器创建成功")

        # 测试配置规则
        if parser.config_rules:
            logger.info(f"✓ 配置规则加载成功，包含 {len(parser.config_rules)} 个规则")
            return True
        else:
            logger.error("✗ 配置规则加载失败")
            return False

    except Exception as e:
        logger.error(f"Excel解析器测试失败: {e}")
        return False

def test_report_generator():
    """测试报告生成器"""
    try:
        logger.info("测试报告生成器...")

        from src.output_generator.report_generator import ReportGenerator

        generator = ReportGenerator()
        logger.info("✓ 报告生成器创建成功")

        # 测试模板列表
        templates = generator.get_template_list()
        logger.info(f"✓ 模板列表获取成功，包含 {len(templates)} 个模板")

        return True

    except Exception as e:
        logger.error(f"报告生成器测试失败: {e}")
        return False

def create_sample_excel():
    """创建示例Excel文件用于测试"""
    try:
        import pandas as pd

        # 创建示例数据
        vehicle_data = pd.DataFrame({
            'VIN码': ['LVSHFAEM1EF123456', 'LVSHFAEM1EF123457'],
            '品牌': ['奥迪', '奥迪'],
            '车型': ['A4L', 'A6L'],
            '年份': [2023, 2023],
            '发动机型号': ['EA888', 'EA888'],
            '排量': [2.0, 2.0],
            '功率': [140, 150]
        })

        # 确保data目录存在
        data_dir = Path('data')
        data_dir.mkdir(exist_ok=True)

        # 保存Excel文件
        excel_path = data_dir / 'sample_vehicles.xlsx'
        vehicle_data.to_excel(excel_path, index=False, sheet_name='车辆信息')

        logger.info(f"✓ 示例Excel文件创建成功: {excel_path}")
        return str(excel_path)

    except Exception as e:
        logger.error(f"创建示例Excel文件失败: {e}")
        return None

def test_excel_parsing():
    """测试Excel文件解析"""
    try:
        # 创建示例文件
        excel_file = create_sample_excel()
        if not excel_file:
            return False

        logger.info("测试Excel文件解析...")

        from src.input_parser.excel_parser import ExcelParser

        parser = ExcelParser()
        result = parser.parse_file(excel_file)

        if result and 'structured_data' in result:
            logger.info("✓ Excel文件解析成功")
            logger.info(f"  解析到 {len(result['structured_data'])} 种结构化数据类型")
            return True
        else:
            logger.error("✗ Excel文件解析失败")
            return False

    except Exception as e:
        logger.error(f"Excel解析测试失败: {e}")
        return False

def main():
    """主测试函数"""
    logger.info("=== 汽车数据处理工具 - 基础功能测试 ===\n")

    tests = [
        ("模块导入", test_imports),
        ("数据库功能", test_database),
        ("Excel解析器", test_excel_parser),
        ("报告生成器", test_report_generator),
        ("Excel文件解析", test_excel_parsing)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        logger.info(f"\n--- {test_name}测试 ---")
        try:
            if test_func():
                passed += 1
                logger.info(f"✓ {test_name}测试通过")
            else:
                logger.error(f"✗ {test_name}测试失败")
        except Exception as e:
            logger.error(f"✗ {test_name}测试异常: {e}")

    logger.info(f"\n=== 测试结果 ===")
    logger.info(f"通过: {passed}/{total}")

    if passed == total:
        logger.info("🎉 所有测试通过！系统基础功能正常。")
        return True
    else:
        logger.warning("⚠️  部分测试失败，请检查错误信息。")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\n测试被用户中断")
        sys.exit(1)
    except Exception as e:
        logger.error(f"测试过程中出现致命错误: {e}")
        sys.exit(1)