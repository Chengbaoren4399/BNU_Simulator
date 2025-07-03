# 北师大求学模拟器

## 项目简介
这是一个模拟北师大校园生活的文字冒险游戏，玩家将体验从入学到毕业的全过程。

## 运行方法
1. 安装依赖：`pip install -r requirements.txt`
2. 运行游戏：`python main.py`

## 小组分工
- cbr：游戏逻辑开发
- yyf：GUI界面开发
- xzq：数据可视化开发

## 项目结构
BNU_Simulator/
├── data/                  # 数据存储目录
│   ├── events.json        # 事件数据库
│   ├── save_game.json     # 游戏存档
│   └── stats.csv          # 游戏统计
├── images/                # 图片资源
│   └── campus.jpg
├── main.py                # 主程序
├── game_logic.py          # 游戏逻辑模块
├── visualization.py       # 数据可视化模块
└── requirements.txt       # 依赖库