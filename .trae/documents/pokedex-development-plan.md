# 宝可梦图鉴网站开发计划

## 项目概述
开发一个第一代151只宝可梦的图鉴网站，使用Python 3.10 + FastAPI + uv工具链，数据源采用PokeAPI。

## 技术栈确认

### uv 支持情况
- ✅ uv 支持 Python 3.10 及以上版本
- 可通过 `uv python install 3.10` 安装指定版本
- 支持项目管理、虚拟环境、依赖锁定等完整功能

### PokeAPI 端点
- `GET /api/v2/pokemon/{id}` - 宝可梦基本信息（图片、属性、身高体重、能力值）
- `GET /api/v2/pokemon-species/{id}` - 物种信息（名称、描述、进化链ID）
- `GET /api/v2/evolution-chain/{id}` - 进化链信息
- `GET /api/v2/type` - 属性列表

## 项目结构

```
pokedex/
├── .python-version          # Python版本锁定文件
├── pyproject.toml           # 项目配置和依赖
├── uv.lock                  # 依赖锁定文件
├── README.md                # 项目说明文档
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI应用入口
│   ├── config.py            # 配置管理
│   ├── models/
│   │   ├── __init__.py
│   │   └── pokemon.py       # Pydantic数据模型
│   ├── services/
│   │   ├── __init__.py
│   │   └── pokeapi.py       # PokeAPI客户端服务
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
└── tests/
    └── test_api.py          # API测试
```

## 实现步骤

### 第一阶段：项目初始化
1. 使用 `uv init` 初始化项目
2. 设置 Python 3.10 版本 (`uv python pin 3.10`)
3. 添加项目依赖：
   - fastapi
   - uvicorn[standard]
   - httpx (异步HTTP客户端)
   - jinja2 (模板引擎)
   - python-multipart (表单支持)

### 第二阶段：后端API开发
1. **创建PokeAPI客户端服务**
   - 实现异步HTTP请求获取宝可梦数据
   - 实现数据缓存机制（内存缓存，避免重复请求）
   - 错误处理和重试逻辑

2. **定义数据模型**
   - PokemonBasic: 基础信息模型（编号、名称、图片、属性）
   - PokemonDetail: 详细信息模型（身高、体重、能力值、描述）
   - PokemonSpecies: 物种信息模型（中英文名称、风味描述）
   - EvolutionChain: 进化链模型

3. **实现API路由**
   - `GET /` - 渲染主页
   - `GET /pokemon/{id}` - 渲染详情页
   - `GET /api/pokemon` - 获取宝可梦列表JSON
   - `GET /api/pokemon/{id}` - 获取单个宝可梦详情JSON
   - `GET /api/types` - 获取属性列表

### 第三阶段：前端开发
1. **主页列表展示**
   - 网格布局展示151只宝可梦
   - 响应式设计（CSS Grid + Media Queries）
   - 卡片组件（编号、名称、图片、属性标签）

2. **搜索功能**
   - 实时搜索输入框
   - 名称模糊匹配（支持中英文）
   - 编号精确匹配
   - 搜索结果即时更新

3. **属性筛选**
   - 15种属性筛选按钮
   - 多选支持（逻辑与）
   - 已选状态视觉反馈
   - 清除筛选按钮

4. **详情页**
   - 宝可梦大图展示
   - 基本信息卡片（编号、名称、身高、体重）
   - 能力值雷达图/进度条
   - 风味描述文本
   - 进化链可视化
   - 返回按钮

### 第四阶段：视觉优化
1. **属性颜色主题**
   - 为15种属性定义独特颜色
   - 应用于卡片背景、边框、标签

2. **动画效果**
   - 卡片悬停放大效果
   - 阴影变化动画
   - 加载状态骨架屏/Spinner

3. **移动端适配**
   - 触摸友好的交互
   - 小屏幕布局优化
   - 底部导航（可选）

### 第五阶段：测试与文档
1. 编写API单元测试
2. 编写本地部署说明
3. 整理代码结构文档

## 属性颜色方案

| 属性 | 英文名 | 颜色代码 |
|------|--------|----------|
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

## 依赖清单

```toml
[project]
name = "pokedex"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "httpx>=0.26.0",
    "jinja2>=3.1.0",
    "python-multipart>=0.0.6",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.23.0",
]
```

## 启动命令

```bash
# 安装uv（如未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 进入项目目录
cd pokedex

# 安装Python 3.10
uv python install 3.10

# 锁定Python版本
uv python pin 3.10

# 同步依赖
uv sync

# 启动开发服务器
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 关键实现细节

### 1. PokeAPI数据获取策略
- 首次启动时预加载所有151只宝可梦的基础数据
- 使用内存缓存存储已获取的数据
- 异步并发请求提高加载速度

### 2. 中文名称获取
- PokeAPI的 `pokemon-species` 端点包含多语言名称
- 过滤 `names` 数组中 `language.name == "zh-Hans"` 的条目

### 3. 搜索实现
- 前端JavaScript实现实时过滤
- 支持中英文名称和编号的模糊/精确匹配
- 使用防抖（debounce）优化输入性能

### 4. 进化链展示
- 从 `evolution-chain` 端点获取完整进化链
- 递归解析进化链结构
- 展示进化条件和触发方式

## 预期交付物

1. ✅ 完整的项目源代码
2. ✅ pyproject.toml 和 uv.lock 依赖文件
3. ✅ README.md 包含：
   - 项目介绍
   - 本地部署步骤
   - 项目结构说明
   - 功能特性列表
