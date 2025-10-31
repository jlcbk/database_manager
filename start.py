#!/usr/bin/env python3
"""
汽车数据处理工具 - 快速启动脚本
Car Data Processing Tool - Quick Start Script
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 9):
        logger.error("需要Python 3.9或更高版本")
        return False
    logger.info(f"Python版本检查通过: {sys.version}")
    return True

def create_directories():
    """创建必要的目录"""
    directories = [
        'database_manager/logs',
        'database_manager/data',
        'database_manager/templates',
        'database_manager/assets',
        'database_manager/tests',
        'database_manager/docs'
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"确保目录存在: {directory}")

def install_dependencies():
    """安装依赖包"""
    try:
        logger.info("正在安装依赖包...")
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r',
            'database_manager/requirements.txt'
        ])
        logger.info("依赖包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"依赖包安装失败: {e}")
        return False

def init_database():
    """初始化数据库"""
    try:
        from src.database.models import init_database
        logger.info("正在初始化数据库...")
        engine = init_database()
        logger.info("数据库初始化完成")
        return True
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        return False

def start_application():
    """启动应用程序"""
    try:
        logger.info("正在启动汽车数据处理工具...")
        from src.main import main
        main()
    except Exception as e:
        logger.error(f"启动应用程序失败: {e}")
        return False

def quick_setup():
    """快速设置"""
    logger.info("=== 汽车数据处理工具 - 快速设置 ===")

    # 检查Python版本
    if not check_python_version():
        return False

    # 创建目录
    create_directories()

    # 询问是否安装依赖
    install_deps = input("是否安装依赖包? (y/n): ").lower().strip()
    if install_deps == 'y':
        if not install_dependencies():
            logger.warning("依赖包安装失败，但可以继续尝试运行")

    # 初始化数据库
    if not init_database():
        logger.warning("数据库初始化失败，应用程序可能会出错")

    logger.info("设置完成！")
    return True

def main():
    """主函数"""
    # 检查是否是首次运行
    flag_file = Path("database_manager/.setup_complete")

    if not flag_file.exists():
        print("=== 欢迎使用汽车数据处理工具 ===")
        print("首次运行需要快速设置...")

        if quick_setup():
            flag_file.touch()
            print("\n设置完成！")
        else:
            print("\n设置过程中出现错误，但可以尝试运行应用程序")

    # 启动应用程序
    start_application()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        logger.error(f"程序运行时出现致命错误: {e}")
        sys.exit(1)