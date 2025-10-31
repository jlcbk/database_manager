#!/usr/bin/env python3
"""
汽车数据处理工具 - PyQt6现代化界面启动器
Car Data Processing Tool - Modern PyQt6 Interface Launcher
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """检查依赖是否已安装"""
    required_packages = [
        'PyQt6',
        'PyQt6.QtWidgets',
        'PyQt6.QtCore',
        'PyQt6.QtGui'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("❌ 缺少以下依赖包:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n请运行以下命令安装依赖:")
        print("pip install PyQt6 PyQt6-tools")
        return False

    return True

def setup_environment():
    """设置环境变量"""
    # 设置高DPI支持
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

    # 设置编码
    if sys.platform == "win32":
        os.environ["PYTHONIOENCODING"] = "utf-8"

def launch_application():
    """启动现代化应用"""
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt

        # 创建应用程序
        app = QApplication(sys.argv)

        # 设置应用程序属性
        app.setApplicationName("汽车数据处理工具")
        app.setApplicationVersion("2.0")
        app.setApplicationDisplayName("Car Data Processor v2.0")
        app.setOrganizationName("CarDataProcessor")

        # 启用高DPI
        app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

        # 禁用帮助按钮
        app.setAttribute(Qt.ApplicationAttribute.AA_DisableWindowContextHelpButtonHint, True)

        print("🚗 正在启动汽车数据处理工具 v2.0 - PyQt6现代化界面...")
        print("✅ PyQt6组件加载成功")

        # 导入并创建主窗口
        from src.modern_main import ModernCarDataProcessor

        # 创建主窗口
        window = ModernCarDataProcessor()

        # 显示窗口
        window.show()

        print("🎨 现代化界面已启动")
        print("💡 提示: 如需使用传统界面，请运行 python src/main.py")

        # 运行应用程序
        return app.exec()

    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保已正确安装PyQt6:")
        print("pip install PyQt6 PyQt6-tools")
        return 1
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("请检查系统环境和依赖安装")
        return 1

def main():
    """主函数"""
    print("=" * 50)
    print("🚗 汽车数据处理工具 - PyQt6现代化界面启动器")
    print("=" * 50)

    # 检查依赖
    if not check_dependencies():
        return 1

    # 设置环境
    setup_environment()

    # 启动应用
    return launch_application()

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 应用程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 启动器运行时出现错误: {e}")
        sys.exit(1)