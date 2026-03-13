# Pokedex - 第一代宝可梦图鉴

一个展示第一代151只宝可梦的Web应用程序，使用Python 3.10 + FastAPI开发，数据来源于PokeAPI。

## 功能特性

### 宝可梦列表展示
- 网格布局展示全部151只第一代宝可梦
- 每个卡片包含：编号、英文名称、中文名称、官方图片、主要属性
- 响应式设计，支持桌面端、平板和移动设备

### 搜索功能
- 支持中英文名称模糊匹配
- 支持编号精确匹配（如 "25" 或 "025"）
- 实时搜索，输入即时显示结果

### 属性筛选
- 15种属性筛选（火、水、草、电、冰、格斗、毒、地面、飞行、超能力、虫、岩石、幽灵、龙、普通）
- 支持多属性同时筛选（逻辑与）
- 一键清除所有筛选条件

### 宝可梦详情页
- 基本信息：编号、名称、身高、体重
- 能力值：HP、攻击、防御、特攻、特防、速度（带可视化进度条）
- 风味描述：中文描述文本
- 进化链：展示进化阶段和进化条件

### 视觉设计
- 每种属性独特的颜色主题
- 卡片悬停动画效果
- 加载状态动画
- 移动端友好的触摸操作

## 技术栈

- **Python**: 3.10
- **Web框架**: FastAPI
- **HTTP客户端**: httpx (异步)
- **模板引擎**: Jinja2
- **包管理**: uv
- **数据源**: [PokeAPI](https://pokeapi.co/)

## 项目结构

```
pokedex/
├── .python-version          # Python版本锁定
├── pyproject.toml           # 项目配置和依赖
├── uv.lock                  # 依赖锁定文件
├── README.md                # 项目说明
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI应用入口
│   ├── config.py            # 配置管理
│   ├── models/
│   │   ├── __init__.py
│   │   └── pokemon.py       # Pydantic数据模型
│   ├── services/
│   │   ├── __init__.py
│   │   └── pokeapi.py       # PokeAPI客户端
│   ├── routers/
│   │   ├── __init__.py
│   │   └── pokemon.py       # API路由
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # 样式文件
│   │   └── js/
│   │       └── app.js       # 前端JavaScript
│   └── templates/
│       ├── base.html        # 基础模板
│       ├── index.html       # 列表页
│       └── detail.html      # 详情页
```

## 本地部署和运行

### 前置要求

- 已安装 [uv](https://docs.astral.sh/uv/) 包管理器

### 安装uv（如未安装）

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 运行步骤

1. **进入项目目录**
```bash
cd pokedex
```

2. **安装Python 3.10**（如未安装）
```bash
uv python install 3.10
```

3. **同步依赖**
```bash
uv sync
```

4. **启动开发服务器**
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. **访问应用**

打开浏览器访问: http://localhost:8000

## API端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/` | GET | 主页（宝可梦列表） |
| `/pokemon/{id}` | GET | 宝可梦详情页 |
| `/api/pokemon` | GET | 获取所有宝可梦列表JSON |
| `/api/pokemon/{id}` | GET | 获取单个宝可梦详情JSON |
| `/api/types` | GET | 获取属性列表和颜色配置 |

## 属性颜色方案

| 属性 | 英文名 | 颜色 |
|------|--------|------|
| 火 | fire | #F08030 |
| 水 | water | #6890F0 |
| 草 | grass | #78C850 |
| 电 | electric | #F8D030 |
| 冰 | ice | #98D8D8 |
| 格斗 | fighting | #C03028 |
| 毒 | poison | #A040A0 |
| 地面 | ground | #E0C068 |
| 飞行 | flying | #A890F0 |
| 超能力 | psychic | #F85888 |
| 虫 | bug | #A8B820 |
| 岩石 | rock | #B8A038 |
| 幽灵 | ghost | #705898 |
| 龙 | dragon | #7038F8 |
| 普通 | normal | #A8A878 |

## 开发说明

### 添加新依赖
```bash
uv add <package-name>
```

### 运行测试
```bash
uv run pytest
```

### 代码格式化
```bash
uv run ruff format .
```

## 数据来源

本项目使用 [PokeAPI](https://pokeapi.co/) 作为数据源，感谢 PokeAPI 团队提供的免费API服务。

## License

MIT License
