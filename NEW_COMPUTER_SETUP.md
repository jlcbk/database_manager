# 新电脑开发环境设置清单

## ✅ 安装检查清单

### 基础软件安装
- [ ] Python 3.9+ (从 python.org 下载)
- [ ] Git (从 git-scm.com 下载)
- [ ] VS Code 或其他代码编辑器 (可选)

### 环境配置
- [ ] 克隆GitHub仓库
- [ ] 创建虚拟环境
- [ ] 安装项目依赖
- [ ] 配置Git用户信息
- [ ] 测试项目运行

## 🚀 快速设置命令

```bash
# 1. 克隆项目
git clone https://github.com/jlcbk/database_manager.git
cd database_manager

# 2. 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. 安装依赖
pip install --upgrade pip
pip install -r requirements.txt

# 4. 配置Git
git config --global user.name "您的名字"
git config --global user.email "您的邮箱@example.com"

# 5. 测试运行
python test_basic.py
python run_demo.py
python src/main.py
```

## 🔧 常见问题解决

### 问题1：pip安装失败
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 问题2：虚拟环境激活失败
```bash
# Windows PowerShell执行策略
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 或使用CMD而不是PowerShell
```

### 问题3：GUI界面无法启动
```bash
# 安装tkinter (Python自带的GUI库)
# 如果出现问题，可能需要重新安装Python
```

## 📱 推荐开发工具

### VS Code 扩展
- Python
- GitLens
- Pylance
- Python Docstring Generator

### 其他有用工具
- Git Desktop (Git图形界面工具)
- GitHub Desktop (GitHub官方工具)

## 🔄 同步工作流程

### 从GitHub获取最新代码
```bash
git pull origin main
```

### 本地更改推送到GitHub
```bash
git add .
git commit -m "描述您的更改"
git push origin main
```

### 查看项目状态
```bash
git status
git log --oneline -10
```

---

💡 **提示**: 将这个文档保存在您的GitHub仓库中，方便在任何新电脑上快速设置开发环境！