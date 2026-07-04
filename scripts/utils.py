"""
工具函数模块
包含项目常用的数据处理和可视化辅助函数
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import os

# 设置中文字体
matplotlib.rcParams["font.sans-serif"] = ["Arial Unicode MS", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False

# 设置绘图风格
plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("husl")

# 项目路径
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(ROOT_DIR, "data", "processed")
CHARTS_DIR = os.path.join(ROOT_DIR, "charts")


def load_data():
    """加载处理后的数据集"""
    filepath = os.path.join(PROCESSED_DIR, "nba_stats_salary_2023_24.csv")
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"数据文件不存在：{filepath}\n"
            "请先运行: python scripts/fetch_nba_data.py"
        )
    return pd.read_csv(filepath)


def calculate_efficiency_score(df):
    """
    计算球员综合效率得分

    公式：效率得分 = 综合场上贡献 / 薪资（标准化后）

    综合贡献权重：
    - 得分 25%
    - 篮板 15%
    - 助攻 15%
    - 抢断+盖帽 15%
    - 效率值 20%
    - 出勤率 10%
    """
    df = df.copy()

    # 只分析有薪资且有足够出场时间的球员
    mask = df["HAS_SALARY"] & (df["GP"] >= 20)
    df_eval = df[mask].copy()

    # 标准化各项指标（Min-Max 归一化）
    metrics = {
        "PTS": 0.25,    # 得分权重
        "REB": 0.15,    # 篮板权重
        "AST": 0.15,    # 助攻权重
        "STL": 0.075,   # 抢断权重
        "BLK": 0.075,   # 盖帽权重
    }

    contribution = np.zeros(len(df_eval))
    for col, weight in metrics.items():
        if col in df_eval.columns:
            normalized = (df_eval[col] - df_eval[col].min()) / (
                df_eval[col].max() - df_eval[col].min() + 1e-8
            )
            contribution += normalized * weight

    df_eval["CONTRIBUTION_SCORE"] = contribution

    # 效率得分 = 贡献 / 薪资（归一化）
    salary_norm = (df_eval["SALARY"] - df_eval["SALARY"].min()) / (
        df_eval["SALARY"].max() - df_eval["SALARY"].min() + 1e-8
    )
    df_eval["EFFICIENCY_SCORE"] = contribution / (salary_norm + 0.1)

    return df_eval


def get_top_bargains(df, top_n=20):
    """获取性价比最高的球员（低薪高能）"""
    df_eval = calculate_efficiency_score(df)
    bargains = df_eval.nlargest(top_n, "EFFICIENCY_SCORE")[
        [
            "PLAYER_NAME", "TEAM_ABBREVIATION", "PTS", "REB", "AST",
            "SALARY", "CONTRIBUTION_SCORE", "EFFICIENCY_SCORE"
        ]
    ]
    return bargains


def get_worst_contracts(df, top_n=20):
    """获取性价比最低的球员（高薪低能）"""
    df_eval = calculate_efficiency_score(df)
    worst = df_eval.nsmallest(top_n, "EFFICIENCY_SCORE")[
        [
            "PLAYER_NAME", "TEAM_ABBREVIATION", "PTS", "REB", "AST",
            "SALARY", "CONTRIBUTION_SCORE", "EFFICIENCY_SCORE"
        ]
    ]
    return worst


def save_chart(fig, filename):
    """保存图表到 charts 目录"""
    filepath = os.path.join(CHARTS_DIR, filename)
    fig.savefig(filepath, dpi=150, bbox_inches="tight", facecolor="white")
    print(f"📊 图表已保存: charts/{filename}")
    return filepath
