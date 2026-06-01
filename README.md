# t7oolkit

基于 Tkinter 的桌面应用初始项目。

## 项目结构

```
t7oolkit/
├── src/t7oolkit/
│   ├── __init__.py
│   ├── __main__.py      # python -m t7oolkit 入口
│   ├── app.py           # 应用启动逻辑
│   └── ui/
│       ├── __init__.py
│       └── main_window.py
├── pyproject.toml
└── requirements.txt
```

## 运行

```bash
# 安装为可编辑包（可选）
pip install -e .

# 方式一：模块运行
python -m t7oolkit

# 方式二：直接运行 app
python src/t7oolkit/app.py
```

## 说明

- Tkinter 随 Python 标准库提供，无需额外安装。
- UI 组件放在 `src/t7oolkit/ui/` 目录下扩展。
