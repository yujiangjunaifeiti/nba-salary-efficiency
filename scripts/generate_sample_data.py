"""
样本数据生成器 (Fallback)
当 NBA API 不可用时，基于真实薪资数据和合理的统计分布生成可分析的数据集

数据来源说明：
- 薪资数据：ESPN / HoopsHype / Spotrac 公开数据
- 场上数据：基于 2023-24 赛季公开统计的合理模拟
- 仅供学习和分析方法展示使用
"""

import pandas as pd
import numpy as np
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# 设置随机种子，确保结果可复现
np.random.seed(42)


def generate_player_data():
    """
    基于 2023-24 赛季真实薪资数据 + 公开统计信息生成球员数据集

    薪资数据来源：ESPN 2023-24 NBA Player Salaries
    场上数据参考：2023-24 NBA Regular Season 公开统计
    """
    # ==========================================
    # 2023-24 赛季球员数据（薪资为真实数据，场上数据为合理估算）
    # 数据参考：NBA.com/stats, Basketball-Reference.com
    # ==========================================

    players = [
        # 超巨 (>4000万)
        {"name": "Stephen Curry", "team": "GSW", "age": 35, "gp": 74, "min": 32.7,
         "pts": 26.4, "reb": 4.5, "ast": 5.1, "stl": 0.7, "blk": 0.4,
         "fg_pct": 0.450, "fg3_pct": 0.408, "ft_pct": 0.923, "plus_minus": 3.2,
         "salary": 51910000},
        {"name": "Kevin Durant", "team": "PHX", "age": 35, "gp": 75, "min": 37.2,
         "pts": 27.1, "reb": 6.6, "ast": 5.0, "stl": 0.9, "blk": 1.2,
         "fg_pct": 0.523, "fg3_pct": 0.413, "ft_pct": 0.856, "plus_minus": 4.1,
         "salary": 47650000},
        {"name": "Nikola Jokic", "team": "DEN", "age": 29, "gp": 79, "min": 34.6,
         "pts": 26.4, "reb": 12.4, "ast": 9.0, "stl": 1.4, "blk": 0.9,
         "fg_pct": 0.583, "fg3_pct": 0.359, "ft_pct": 0.817, "plus_minus": 8.7,
         "salary": 47600000},
        {"name": "Joel Embiid", "team": "PHI", "age": 30, "gp": 39, "min": 33.6,
         "pts": 34.7, "reb": 11.0, "ast": 5.6, "stl": 1.2, "blk": 1.7,
         "fg_pct": 0.529, "fg3_pct": 0.388, "ft_pct": 0.883, "plus_minus": 6.8,
         "salary": 47600000},
        {"name": "Giannis Antetokounmpo", "team": "MIL", "age": 29, "gp": 73, "min": 35.2,
         "pts": 30.4, "reb": 11.5, "ast": 6.5, "stl": 1.2, "blk": 1.1,
         "fg_pct": 0.611, "fg3_pct": 0.274, "ft_pct": 0.657, "plus_minus": 5.4,
         "salary": 45640000},
        {"name": "Damian Lillard", "team": "MIL", "age": 33, "gp": 73, "min": 35.3,
         "pts": 24.3, "reb": 4.4, "ast": 7.0, "stl": 1.0, "blk": 0.2,
         "fg_pct": 0.424, "fg3_pct": 0.354, "ft_pct": 0.920, "plus_minus": 2.8,
         "salary": 45640000},
        {"name": "Kawhi Leonard", "team": "LAC", "age": 32, "gp": 68, "min": 34.3,
         "pts": 23.7, "reb": 6.1, "ast": 3.6, "stl": 1.6, "blk": 0.5,
         "fg_pct": 0.525, "fg3_pct": 0.417, "ft_pct": 0.885, "plus_minus": 3.5,
         "salary": 45640000},
        {"name": "Paul George", "team": "LAC", "age": 33, "gp": 74, "min": 33.8,
         "pts": 22.6, "reb": 5.2, "ast": 3.5, "stl": 1.5, "blk": 0.5,
         "fg_pct": 0.471, "fg3_pct": 0.413, "ft_pct": 0.907, "plus_minus": 2.1,
         "salary": 45640000},

        # 明星级 (2000-4000万)
        {"name": "Jayson Tatum", "team": "BOS", "age": 26, "gp": 74, "min": 35.7,
         "pts": 26.9, "reb": 8.1, "ast": 4.9, "stl": 1.0, "blk": 0.6,
         "fg_pct": 0.471, "fg3_pct": 0.376, "ft_pct": 0.833, "plus_minus": 6.5,
         "salary": 32600000},
        {"name": "Luka Doncic", "team": "DAL", "age": 25, "gp": 70, "min": 37.5,
         "pts": 33.9, "reb": 9.2, "ast": 9.8, "stl": 1.4, "blk": 0.5,
         "fg_pct": 0.487, "fg3_pct": 0.382, "ft_pct": 0.786, "plus_minus": 5.1,
         "salary": 40060000},
        {"name": "Anthony Davis", "team": "LAL", "age": 31, "gp": 76, "min": 35.5,
         "pts": 24.7, "reb": 12.6, "ast": 3.5, "stl": 1.2, "blk": 2.3,
         "fg_pct": 0.545, "fg3_pct": 0.271, "ft_pct": 0.816, "plus_minus": 2.9,
         "salary": 40600000},
        {"name": "Devin Booker", "team": "PHX", "age": 27, "gp": 68, "min": 36.0,
         "pts": 27.1, "reb": 4.5, "ast": 6.9, "stl": 0.9, "blk": 0.4,
         "fg_pct": 0.492, "fg3_pct": 0.364, "ft_pct": 0.886, "plus_minus": 3.2,
         "salary": 36010000},
        {"name": "Karl-Anthony Towns", "team": "MIN", "age": 28, "gp": 62, "min": 32.7,
         "pts": 21.8, "reb": 8.3, "ast": 3.0, "stl": 0.7, "blk": 0.7,
         "fg_pct": 0.504, "fg3_pct": 0.416, "ft_pct": 0.873, "plus_minus": 2.0,
         "salary": 36010000},
        {"name": "Shai Gilgeous-Alexander", "team": "OKC", "age": 25, "gp": 75, "min": 34.0,
         "pts": 30.1, "reb": 5.5, "ast": 6.2, "stl": 2.0, "blk": 0.9,
         "fg_pct": 0.535, "fg3_pct": 0.353, "ft_pct": 0.874, "plus_minus": 8.1,
         "salary": 33850000},
        {"name": "Ja Morant", "team": "MEM", "age": 24, "gp": 9, "min": 35.3,
         "pts": 25.1, "reb": 5.6, "ast": 8.1, "stl": 0.8, "blk": 0.6,
         "fg_pct": 0.471, "fg3_pct": 0.275, "ft_pct": 0.813, "plus_minus": -2.4,
         "salary": 33850000},
        {"name": "Jaylen Brown", "team": "BOS", "age": 27, "gp": 70, "min": 33.5,
         "pts": 23.0, "reb": 5.5, "ast": 3.6, "stl": 1.2, "blk": 0.5,
         "fg_pct": 0.497, "fg3_pct": 0.354, "ft_pct": 0.703, "plus_minus": 4.6,
         "salary": 31830000},
        {"name": "Donovan Mitchell", "team": "CLE", "age": 27, "gp": 55, "min": 35.3,
         "pts": 26.6, "reb": 5.1, "ast": 6.1, "stl": 1.8, "blk": 0.5,
         "fg_pct": 0.462, "fg3_pct": 0.368, "ft_pct": 0.865, "plus_minus": 5.4,
         "salary": 32600000},
        {"name": "Bam Adebayo", "team": "MIA", "age": 26, "gp": 71, "min": 34.0,
         "pts": 19.3, "reb": 10.4, "ast": 3.9, "stl": 1.1, "blk": 0.9,
         "fg_pct": 0.521, "fg3_pct": 0.0, "ft_pct": 0.755, "plus_minus": 2.4,
         "salary": 32600000},
        {"name": "De'Aaron Fox", "team": "SAC", "age": 26, "gp": 74, "min": 35.9,
         "pts": 26.6, "reb": 4.6, "ast": 5.6, "stl": 2.0, "blk": 0.4,
         "fg_pct": 0.465, "fg3_pct": 0.369, "ft_pct": 0.738, "plus_minus": -0.1,
         "salary": 32600000},
        {"name": "Pascal Siakam", "team": "IND", "age": 30, "gp": 80, "min": 33.2,
         "pts": 21.7, "reb": 7.1, "ast": 4.3, "stl": 0.8, "blk": 0.3,
         "fg_pct": 0.536, "fg3_pct": 0.346, "ft_pct": 0.732, "plus_minus": 1.2,
         "salary": 37890000},
        {"name": "Kyrie Irving", "team": "DAL", "age": 32, "gp": 58, "min": 35.0,
         "pts": 25.6, "reb": 5.0, "ast": 5.2, "stl": 1.3, "blk": 0.5,
         "fg_pct": 0.497, "fg3_pct": 0.411, "ft_pct": 0.905, "plus_minus": 2.3,
         "salary": 37800000},
        {"name": "Jamal Murray", "team": "DEN", "age": 27, "gp": 59, "min": 31.5,
         "pts": 21.2, "reb": 4.1, "ast": 6.5, "stl": 1.0, "blk": 0.7,
         "fg_pct": 0.481, "fg3_pct": 0.425, "ft_pct": 0.853, "plus_minus": 2.8,
         "salary": 33750000},
        {"name": "Brandon Ingram", "team": "NOP", "age": 26, "gp": 64, "min": 34.2,
         "pts": 20.8, "reb": 5.1, "ast": 5.7, "stl": 0.8, "blk": 0.6,
         "fg_pct": 0.492, "fg3_pct": 0.355, "ft_pct": 0.801, "plus_minus": 0.5,
         "salary": 33830000},

        # 主力级 (1000-2000万)
        {"name": "Jalen Brunson", "team": "NYK", "age": 27, "gp": 77, "min": 35.4,
         "pts": 28.7, "reb": 3.6, "ast": 6.7, "stl": 0.9, "blk": 0.2,
         "fg_pct": 0.479, "fg3_pct": 0.401, "ft_pct": 0.847, "plus_minus": 6.4,
         "salary": 26340000},
        {"name": "Tyrese Haliburton", "team": "IND", "age": 24, "gp": 69, "min": 32.2,
         "pts": 20.1, "reb": 3.9, "ast": 10.9, "stl": 1.2, "blk": 0.7,
         "fg_pct": 0.477, "fg3_pct": 0.364, "ft_pct": 0.855, "plus_minus": 3.5,
         "salary": 5800000},
        {"name": "Mikal Bridges", "team": "BKN", "age": 27, "gp": 82, "min": 34.8,
         "pts": 19.6, "reb": 4.5, "ast": 3.6, "stl": 1.0, "blk": 0.4,
         "fg_pct": 0.436, "fg3_pct": 0.372, "ft_pct": 0.814, "plus_minus": -3.2,
         "salary": 21700000},
        {"name": "Myles Turner", "team": "IND", "age": 28, "gp": 77, "min": 27.0,
         "pts": 17.1, "reb": 6.9, "ast": 1.3, "stl": 0.5, "blk": 1.9,
         "fg_pct": 0.524, "fg3_pct": 0.358, "ft_pct": 0.773, "plus_minus": 2.8,
         "salary": 20970000},
        {"name": "Clint Capela", "team": "ATL", "age": 30, "gp": 73, "min": 25.8,
         "pts": 11.5, "reb": 10.6, "ast": 1.2, "stl": 0.6, "blk": 1.5,
         "fg_pct": 0.571, "fg3_pct": 0.0, "ft_pct": 0.631, "plus_minus": -1.2,
         "salary": 20610000},
        {"name": "Jarrett Allen", "team": "CLE", "age": 26, "gp": 77, "min": 31.7,
         "pts": 16.5, "reb": 10.5, "ast": 2.7, "stl": 0.7, "blk": 1.1,
         "fg_pct": 0.634, "fg3_pct": 0.0, "ft_pct": 0.742, "plus_minus": 4.3,
         "salary": 20000000},
        {"name": "Jerami Grant", "team": "POR", "age": 30, "gp": 54, "min": 33.9,
         "pts": 21.0, "reb": 3.5, "ast": 2.8, "stl": 0.8, "blk": 0.6,
         "fg_pct": 0.451, "fg3_pct": 0.402, "ft_pct": 0.817, "plus_minus": -7.4,
         "salary": 27580000},
        {"name": "Kyle Kuzma", "team": "WAS", "age": 28, "gp": 70, "min": 32.6,
         "pts": 22.2, "reb": 6.6, "ast": 4.2, "stl": 0.5, "blk": 0.7,
         "fg_pct": 0.463, "fg3_pct": 0.336, "ft_pct": 0.775, "plus_minus": -9.5,
         "salary": 25560000},
        {"name": "Jonas Valanciunas", "team": "NOP", "age": 32, "gp": 82, "min": 23.5,
         "pts": 12.2, "reb": 8.8, "ast": 2.1, "stl": 0.4, "blk": 0.8,
         "fg_pct": 0.559, "fg3_pct": 0.308, "ft_pct": 0.785, "plus_minus": -2.2,
         "salary": 15430000},

        # 新秀合同/潜力股 (<1000万)
        {"name": "Anthony Edwards", "team": "MIN", "age": 22, "gp": 79, "min": 35.1,
         "pts": 25.9, "reb": 5.4, "ast": 5.1, "stl": 1.3, "blk": 0.5,
         "fg_pct": 0.461, "fg3_pct": 0.357, "ft_pct": 0.836, "plus_minus": 5.8,
         "salary": 9000000},
        {"name": "Tyrese Maxey", "team": "PHI", "age": 23, "gp": 70, "min": 37.5,
         "pts": 25.9, "reb": 3.7, "ast": 6.2, "stl": 1.0, "blk": 0.5,
         "fg_pct": 0.450, "fg3_pct": 0.373, "ft_pct": 0.868, "plus_minus": 4.2,
         "salary": 4340000},
        {"name": "Alperen Sengun", "team": "HOU", "age": 21, "gp": 63, "min": 32.5,
         "pts": 21.1, "reb": 9.3, "ast": 5.0, "stl": 1.2, "blk": 0.7,
         "fg_pct": 0.537, "fg3_pct": 0.297, "ft_pct": 0.693, "plus_minus": 2.1,
         "salary": 3640000},
        {"name": "Victor Wembanyama", "team": "SAS", "age": 20, "gp": 71, "min": 29.7,
         "pts": 21.4, "reb": 10.6, "ast": 3.9, "stl": 1.2, "blk": 3.6,
         "fg_pct": 0.465, "fg3_pct": 0.325, "ft_pct": 0.796, "plus_minus": -1.5,
         "salary": 12160000},
        {"name": "Chet Holmgren", "team": "OKC", "age": 22, "gp": 82, "min": 29.4,
         "pts": 16.5, "reb": 7.9, "ast": 2.4, "stl": 0.6, "blk": 2.3,
         "fg_pct": 0.530, "fg3_pct": 0.370, "ft_pct": 0.793, "plus_minus": 4.0,
         "salary": 10380000},
        {"name": "Paolo Banchero", "team": "ORL", "age": 21, "gp": 80, "min": 35.0,
         "pts": 22.6, "reb": 6.9, "ast": 5.4, "stl": 0.9, "blk": 0.6,
         "fg_pct": 0.455, "fg3_pct": 0.339, "ft_pct": 0.725, "plus_minus": 1.8,
         "salary": 11600000},
        {"name": "Scottie Barnes", "team": "TOR", "age": 22, "gp": 60, "min": 34.9,
         "pts": 19.9, "reb": 8.2, "ast": 6.1, "stl": 1.3, "blk": 1.5,
         "fg_pct": 0.475, "fg3_pct": 0.341, "ft_pct": 0.781, "plus_minus": -3.1,
         "salary": 8180000},
        {"name": "Jalen Williams", "team": "OKC", "age": 23, "gp": 71, "min": 31.3,
         "pts": 19.1, "reb": 4.0, "ast": 4.5, "stl": 1.1, "blk": 0.6,
         "fg_pct": 0.540, "fg3_pct": 0.427, "ft_pct": 0.814, "plus_minus": 5.6,
         "salary": 4770000},
        {"name": "Desmond Bane", "team": "MEM", "age": 25, "gp": 42, "min": 34.4,
         "pts": 23.7, "reb": 4.4, "ast": 5.5, "stl": 1.0, "blk": 0.5,
         "fg_pct": 0.464, "fg3_pct": 0.381, "ft_pct": 0.870, "plus_minus": -5.2,
         "salary": 3900000},
        {"name": "Austin Reaves", "team": "LAL", "age": 25, "gp": 82, "min": 32.1,
         "pts": 15.9, "reb": 4.3, "ast": 5.5, "stl": 0.8, "blk": 0.3,
         "fg_pct": 0.486, "fg3_pct": 0.367, "ft_pct": 0.853, "plus_minus": -1.1,
         "salary": 12000000},

        # 底薪/老将
        {"name": "Russell Westbrook", "team": "LAC", "age": 35, "gp": 68, "min": 22.5,
         "pts": 11.1, "reb": 5.0, "ast": 4.5, "stl": 1.1, "blk": 0.3,
         "fg_pct": 0.454, "fg3_pct": 0.273, "ft_pct": 0.688, "plus_minus": -0.8,
         "salary": 3840000},
        {"name": "Chris Paul", "team": "GSW", "age": 39, "gp": 58, "min": 26.4,
         "pts": 9.2, "reb": 3.9, "ast": 6.8, "stl": 1.2, "blk": 0.1,
         "fg_pct": 0.441, "fg3_pct": 0.371, "ft_pct": 0.827, "plus_minus": 0.5,
         "salary": 30800000},
        {"name": "Klay Thompson", "team": "GSW", "age": 34, "gp": 77, "min": 29.7,
         "pts": 17.9, "reb": 3.3, "ast": 2.3, "stl": 0.6, "blk": 0.5,
         "fg_pct": 0.432, "fg3_pct": 0.387, "ft_pct": 0.927, "plus_minus": -0.2,
         "salary": 43210000},
        {"name": "Draymond Green", "team": "GSW", "age": 34, "gp": 55, "min": 27.1,
         "pts": 8.6, "reb": 7.2, "ast": 6.0, "stl": 1.0, "blk": 0.9,
         "fg_pct": 0.497, "fg3_pct": 0.395, "ft_pct": 0.730, "plus_minus": 2.7,
         "salary": 22310000},
        {"name": "Jordan Poole", "team": "WAS", "age": 24, "gp": 78, "min": 30.1,
         "pts": 17.4, "reb": 2.7, "ast": 4.4, "stl": 1.1, "blk": 0.3,
         "fg_pct": 0.413, "fg3_pct": 0.326, "ft_pct": 0.877, "plus_minus": -8.5,
         "salary": 28700000},
    ]

    df = pd.DataFrame(players)

    # 添加衍生指标
    df["GP"] = df["gp"]
    df["MIN"] = df["min"]
    df["PTS"] = df["pts"]
    df["REB"] = df["reb"]
    df["AST"] = df["ast"]
    df["STL"] = df["stl"]
    df["BLK"] = df["blk"]
    df["FG_PCT"] = df["fg_pct"]
    df["FG3_PCT"] = df["fg3_pct"]
    df["FT_PCT"] = df["ft_pct"]
    df["PLUS_MINUS"] = df["plus_minus"]
    df["SALARY"] = df["salary"]
    df["PLAYER_NAME"] = df["name"]
    df["TEAM_ABBREVIATION"] = df["team"]
    df["AGE"] = df["age"]

    # 计算效率值 (简化版 PER)
    df["EFF"] = (
        df["PTS"] + df["REB"] + df["AST"] + df["STL"] + df["BLK"]
        - (df["MIN"] * 0.1)  # 出场时间惩罚项
    ).round(1)

    # 假设计算真实命中率 TS%
    df["TS_PCT"] = (
        df["PTS"] / (2 * (df["PTS"] / (df["FG_PCT"] * 2 + df["FT_PCT"] * 0.44 + 0.001)))
    ).clip(0.4, 0.75).round(3)

    # 使用率估算
    df["USG_PCT"] = (
        (df["PTS"] + df["AST"] * 1.5 + df["STL"] * 0.5) / (df["MIN"] * 1.2)
    ).clip(0.1, 0.45).round(3)

    # 薪资等级
    salary_m = df["SALARY"] / 10000
    df["SALARY_LEVEL"] = pd.cut(
        salary_m,
        bins=[0, 500, 1000, 2000, 3000, 6000],
        labels=["底薪 (<500万)", "中产 (500-1000万)", "主力 (1000-2000万)",
                "明星 (2000-3000万)", "超巨 (>3000万)"]
    )

    # 效率得分
    metrics = {"PTS": 0.25, "REB": 0.15, "AST": 0.15, "STL": 0.075, "BLK": 0.075}
    contribution = np.zeros(len(df))
    for col, w in metrics.items():
        col_min, col_max = df[col].min(), df[col].max()
        contribution += (df[col] - col_min) / (col_max - col_min + 1e-8) * w
    df["CONTRIBUTION"] = contribution

    salary_norm = (df["SALARY"] - df["SALARY"].min()) / (df["SALARY"].max() - df["SALARY"].min())
    df["EFFICIENCY"] = (contribution / (salary_norm + 0.1)).round(4)
    df["PTS_PER_MILLION"] = (df["PTS"] / (df["SALARY"] / 1_000_000)).round(2)
    df["HAS_SALARY"] = True
    df["SEASON"] = "2023-24"

    return df


if __name__ == "__main__":
    print("🏀 生成 NBA 球员分析数据集...")
    print("数据来源说明：薪资为 ESPN/HoopsHype 公开数据，场上数据为参考公开统计的估算值")
    print("仅供学习和分析方法展示\n")

    df = generate_player_data()

    # 保存
    df.to_csv(os.path.join(RAW_DIR, "player_stats.csv"), index=False)
    df.to_csv(os.path.join(PROCESSED_DIR, "nba_stats_salary_2023_24.csv"), index=False)
    df.to_csv(os.path.join(PROCESSED_DIR, "nba_clean_2023_24.csv"), index=False)

    print(f"✅ 数据集已生成!")
    print(f"   球员数: {len(df)}")
    print(f"   薪资范围: ${df['SALARY'].min()/10000:.0f}万 ~ ${df['SALARY'].max()/10000:.0f}万")
    print(f"   数据文件:")
    print(f"     data/raw/player_stats.csv")
    print(f"     data/processed/nba_stats_salary_2023_24.csv")
    print(f"     data/processed/nba_clean_2023_24.csv")
    print(f"\n💡 提示: NBA API 在国内被墙，这个脚本生成的数据基于真实薪资和合理的统计分布")
    print(f"   如果你能使用代理访问 stats.nba.com，请运行: python scripts/fetch_nba_data.py")
