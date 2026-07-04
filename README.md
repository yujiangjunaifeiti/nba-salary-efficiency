# 🏀 NBA 球员薪资效率分析

> **用数据回答一个商业问题：一个球员拿的工资，值不值？**

在线查看完整分析报告：[View Analysis Report](#) （待部署）

---

## 📊 项目概览

如果你是 NBA 球队总经理（GM），薪资帽限制下每一分钱都要花在刀刃上。本项目通过数据分析 + 机器学习，构建球员薪资效率评估模型，帮助回答三个核心商业问题：

1. **哪些球员是高薪低能？** → 识别溢价与折价合同
2. **球员的合理薪资是多少？** → 基于场上表现预测市场公允价格
3. **如何用有限预算组建阵容？** → 以效率为导向的球员推荐策略

## 🎯 亮点（让面试官眼前一亮的点）

- 🔄 **完整数据管道**：API 实时拉取 → 清洗 → 特征工程 → 建模 → 可视化
- 📈 **经济学视角**：引入「消费者剩余」概念类比球员薪资溢价
- 🤖 **机器学习建模**：用随机森林 + XGBoost 构建薪资预测模型
- 📊 **交互式可视化**：Plotly 生成可交互图表，比静态图更直观
- 💼 **商业决策导向**：不止于分析，每个环节都落到「如果你是 GM 该怎么做」

## 🗂️ 项目结构

```
nba-salary-efficiency/
├── README.md                   # 项目说明 + 分析报告
├── requirements.txt            # Python 依赖
├── data/                       # 数据文件夹
│   ├── raw/                    # 原始数据（API 拉取）
│   └── processed/              # 清洗后的数据
├── notebooks/                  # Jupyter 分析笔记
│   ├── 01_data_collection.ipynb    # 数据获取
│   ├── 02_data_cleaning.ipynb      # 数据清洗
│   ├── 03_eda.ipynb                # 探索性分析
│   └── 04_modeling.ipynb           # 建模与结论
├── scripts/                    # Python 脚本
│   ├── fetch_nba_data.py       # 数据获取脚本
│   └── utils.py                # 工具函数
└── charts/                     # 导出的图表
```

## 🚀 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/yujiangjunaifeiti/nba-salary-efficiency.git
cd nba-salary-efficiency

# 2. 安装依赖
pip install -r requirements.txt

# 3. 拉取数据
python scripts/fetch_nba_data.py

# 4. 启动 Jupyter 分析
jupyter notebook notebooks/
```

## 🧠 技能栈

| 环节 | 技术 |
|---|---|
| 数据获取 | `nba_api`, `requests` |
| 数据处理 | `Pandas`, `NumPy` |
| 可视化 | `Matplotlib`, `Seaborn`, `Plotly` |
| 建模 | `scikit-learn`, `XGBoost` |
| 统计方法 | 多元线性回归、随机森林、特征重要性分析 |

## 📝 分析框架

### 核心指标定义

```
效率得分 = 综合场上贡献 / 薪资

其中：
- 综合场上贡献 = f(得分, 篮板, 助攻, 抢断, 盖帽, 效率值, 出勤率, 正负值)
- 薪资 = 当赛季工资
```

### 分析方法

1. **描述统计**：薪资分布、位置差异、年龄曲线
2. **聚类分析**：识别不同类型的球员（得分型/全能型/防守型）
3. **回归预测**：基于表现预测合理薪资
4. **效率排名**：性价比 TOP 20 和最差合同 TOP 20

---

## 👤 关于作者

- **专业背景**：数字经济本科 → 应用统计（数据科学方向）硕士备考中
- **技能**：Python, SQL, Tableau, 数据分析
- **GitHub**：[yujiangjunaifeiti](https://github.com/yujiangjunaifeiti)

---

*"In God we trust. All others must bring data." — W. Edwards Deming*
