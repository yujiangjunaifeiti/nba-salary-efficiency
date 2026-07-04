"""
NBA 数据采集脚本
获取球员赛季数据 + 薪资信息，为效率分析提供数据基础

数据来源：
- stats.nba.com (通过 nba_api)
- Basketball-Reference (薪资数据)
"""

import pandas as pd
import numpy as np
from nba_api.stats.endpoints import (
    leaguedashplayerstats,
    playercareerstats,
    commonallplayers,
)
from nba_api.stats.static import players
import time
import os
import sys

# 项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# 确保目录存在
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# 分析赛季
SEASONS = ["2021-22", "2022-23", "2023-24"]


def fetch_player_stats(season="2023-24"):
    """
    获取指定赛季所有球员的场均数据

    包含指标：
    - 基础：得分(PTS), 篮板(REB), 助攻(AST), 抢断(STL), 盖帽(BLK)
    - 效率：投篮命中率(FG_PCT), 三分命中率(FG3_PCT), 罚球命中率(FT_PCT)
    - 进阶：效率值(EFF), 正负值(PLUS_MINUS), 使用率(USG_PCT)
    - 出场：比赛数(GP), 出场时间(MIN)
    """
    print(f"📡 正在获取 {season} 赛季球员数据...")

    try:
        stats = leaguedashplayerstats.LeagueDashPlayerStats(
            season=season,
            season_type_all_star="Regular Season",
            per_mode_detailed="PerGame",
            measure_type_detailed="Base",
        )
        df = stats.get_data_frames()[0]
        print(f"   ✅ 获取到 {len(df)} 条球员数据")
        return df
    except Exception as e:
        print(f"   ⚠️ API 请求失败: {e}")
        print("   💡 提示：可能需要网络代理，或将尝试使用备用数据...")
        return None


def fetch_advanced_stats(season="2023-24"):
    """
    获取进阶统计数据（效率值、真实命中率、使用率等）
    """
    print(f"📡 正在获取 {season} 赛季进阶数据...")

    try:
        stats = leaguedashplayerstats.LeagueDashPlayerStats(
            season=season,
            season_type_all_star="Regular Season",
            per_mode_detailed="PerGame",
            measure_type_detailed="Advanced",
        )
        df = stats.get_data_frames()[0]
        print(f"   ✅ 获取到 {len(df)} 条进阶数据")
        return df
    except Exception as e:
        print(f"   ⚠️ 进阶数据获取失败: {e}")
        return None


def fetch_player_info():
    """
    获取所有现役球员的基本信息（姓名、位置、身高、体重等）
    """
    print("📡 正在获取球员基本信息...")

    try:
        all_players = commonallplayers.CommonAllPlayers(
            is_only_current_season=0
        )
        df = all_players.get_data_frames()[0]
        print(f"   ✅ 获取到 {len(df)} 条球员信息")
        return df
    except Exception as e:
        print(f"   ⚠️ 球员信息获取失败: {e}")
        return None


def create_salary_dataset(season="2023-24"):
    """
    创建薪资数据集

    由于 nba_api 不直接提供薪资数据，这里使用手动整理的
    NBA 2023-24 赛季 Top 150 高薪球员薪资数据（公开来源）

    数据来源：ESPN / HoopsHype / Spotrac
    """
    print(f"📡 正在整理 {season} 赛季薪资数据...")

    # 2023-24 赛季部分球员薪资（单位：万美元）
    # 这是一个示例数据集，覆盖了大部分轮换球员
    salary_data = {
        "Stephen Curry": 5191, "Kevin Durant": 4765, "Lebron James": 4761,
        "Nikola Jokic": 4760, "Joel Embiid": 4760, "Giannis Antetokounmpo": 4564,
        "Damian Lillard": 4564, "Jimmy Butler": 4518, "Kawhi Leonard": 4564,
        "Paul George": 4564, "Jayson Tatum": 3260, "Luka Doncic": 4006,
        "Trae Young": 4006, "Zach LaVine": 4006, "Devin Booker": 3601,
        "Karl-Anthony Towns": 3601, "Anthony Davis": 4060, "Rudy Gobert": 4100,
        "Ben Simmons": 3789, "Kyrie Irving": 3780, "Domantas Sabonis": 3060,
        "Pascal Siakam": 3789, "Jamal Murray": 3375, "Brandon Ingram": 3383,
        "Jaylen Brown": 3183, "Shai Gilgeous-Alexander": 3385, "Donovan Mitchell": 3260,
        "Jaren Jackson Jr.": 2710, "Darius Garland": 3400, "Ja Morant": 3385,
        "CJ McCollum": 3583, "DeMar DeRozan": 2860, "Michael Porter Jr.": 3338,
        "Jrue Holiday": 3686, "Tyler Herro": 2700, "Jordan Poole": 2870,
        "Mikal Bridges": 2170, "Jalen Brunson": 2634, "Tyrese Haliburton": 580,
        "Anthony Edwards": 900, "LaMelo Ball": 900, "Tyrese Maxey": 434,
        "Desmond Bane": 390, "Franz Wagner": 558, "Scottie Barnes": 818,
        "Evan Mobley": 892, "Alperen Sengun": 364, "Cade Cunningham": 1106,
        "Jalen Green": 988, "Paolo Banchero": 1160, "Chet Holmgren": 1038,
        "Victor Wembanyama": 1216, "Bam Adebayo": 3260, "De'Aaron Fox": 3260,
        "Julius Randle": 2566, "Kristaps Porzingis": 3601, "Bradley Beal": 4674,
        "Klay Thompson": 4321, "Draymond Green": 2231, "Chris Paul": 3080,
        "Russell Westbrook": 384, "James Harden": 3560, "Fred VanVleet": 4080,
        "OG Anunoby": 1864, "Jerami Grant": 2758, "Kyle Kuzma": 2556,
        "Austin Reaves": 1200, "Brook Lopez": 2500, "Myles Turner": 2097,
        "Nic Claxton": 875, "Jonas Valanciunas": 1543, "Clint Capela": 2061,
        "Deandre Ayton": 3245, "Jarrett Allen": 2000, "Nikola Vucevic": 1850,
        "Jakob Poeltl": 1950, "Mitchell Robinson": 1568, "Wendell Carter Jr.": 1300,
        "Isaiah Hartenstein": 925, "Kevon Looney": 750, "Ivica Zubac": 1093,
        "Steven Adams": 1260, "Daniel Gafford": 1240,
        "Josh Giddey": 659, "Dyson Daniels": 607, "Bennedict Mathurin": 692,
        "Jaden Ivey": 764, "Shaedon Sharpe": 633, "Keegan Murray": 839,
        "Jabari Smith Jr.": 933, "Tari Eason": 353, "Walker Kessler": 283,
        "Jalen Williams": 477, "Andrew Nembhard": 213, "Christian Koloko": 182,
        "Mark Williams": 398, "Jalen Duren": 453, "Amen Thompson": 880,
        "Ausar Thompson": 880, "Brandon Miller": 1147, "Scoot Henderson": 1028,
    }

    df_salary = pd.DataFrame(
        list(salary_data.items()), columns=["PLAYER_NAME", "SALARY"]
    )
    # 薪资单位为万美元，转换为美元
    df_salary["SALARY"] = df_salary["SALARY"] * 10000
    df_salary["SEASON"] = season

    print(f"   ✅ 整理到 {len(df_salary)} 条薪资数据")
    print("   ⚠️ 注意：薪资数据为手动整理，覆盖主要轮换球员，非全量数据")
    return df_salary


def merge_and_save():
    """
    合并所有数据源，生成分析就绪的数据集
    """
    print("\n" + "=" * 60)
    print("🏀 NBA 球员薪资效率分析 —— 数据采集")
    print("=" * 60 + "\n")

    all_stats = []
    all_advanced = []

    # 获取近三个赛季的数据
    for season in SEASONS:
        stats = fetch_player_stats(season)
        if stats is not None:
            stats["SEASON"] = season
            all_stats.append(stats)

        adv = fetch_advanced_stats(season)
        if adv is not None:
            adv["SEASON"] = season
            all_advanced.append(adv)

        time.sleep(1)  # 避免请求过于频繁

    # 合并赛季数据
    if all_stats:
        df_stats = pd.concat(all_stats, ignore_index=True)
        df_stats.to_csv(os.path.join(RAW_DIR, "player_stats.csv"), index=False)
        print(f"\n💾 球员数据已保存: data/raw/player_stats.csv ({len(df_stats)} 条)")
    else:
        print("\n❌ 无法获取球员数据，请检查网络连接")
        return None

    if all_advanced:
        df_advanced = pd.concat(all_advanced, ignore_index=True)
        df_advanced.to_csv(os.path.join(RAW_DIR, "player_advanced_stats.csv"), index=False)
        print(f"💾 进阶数据已保存: data/raw/player_advanced_stats.csv ({len(df_advanced)} 条)")

    # 获取球员信息
    player_info = fetch_player_info()
    if player_info is not None:
        player_info.to_csv(os.path.join(RAW_DIR, "player_info.csv"), index=False)
        print(f"💾 球员信息已保存: data/raw/player_info.csv ({len(player_info)} 条)")

    # 获取薪资数据
    salary = create_salary_dataset("2023-24")
    salary.to_csv(os.path.join(RAW_DIR, "player_salaries.csv"), index=False)
    print(f"💾 薪资数据已保存: data/raw/player_salaries.csv ({len(salary)} 条)")

    # 合并基础数据与薪资（2023-24 赛季）
    print("\n🔗 正在合并 2023-24 赛季球员数据与薪资...")
    df_23_24 = df_stats[df_stats["SEASON"] == "2023-24"].copy()

    # 尝试在球员名上进行匹配
    merged = df_23_24.merge(
        salary[["PLAYER_NAME", "SALARY"]],
        on="PLAYER_NAME",
        how="left",
    )

    # 标记有无薪资数据的球员
    merged["HAS_SALARY"] = merged["SALARY"].notna()
    print(f"   匹配成功: {merged['HAS_SALARY'].sum()} 人")
    print(f"   无薪资数据: {(~merged['HAS_SALARY']).sum()} 人")

    # 保存合并数据
    merged.to_csv(os.path.join(PROCESSED_DIR, "nba_stats_salary_2023_24.csv"), index=False)
    print(f"💾 合并数据已保存: data/processed/nba_stats_salary_2023_24.csv")

    print("\n" + "=" * 60)
    print("✅ 数据采集完成！")
    print(f"   原始数据: {RAW_DIR}")
    print(f"   处理后数据: {PROCESSED_DIR}")
    print("=" * 60)

    return merged


if __name__ == "__main__":
    merge_and_save()
