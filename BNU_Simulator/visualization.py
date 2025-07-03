import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

def plot_player_stats(player_history):
    """绘制玩家属性变化图表"""
    if not player_history:
        # 创建空图表
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, '暂无统计数据', 
               horizontalalignment='center', 
               verticalalignment='center',
               fontsize=15)
        return fig
    
    # 转换为DataFrame
    df = pd.DataFrame(player_history)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # 创建图表
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # 绘制属性值
    ax1.plot(df['timestamp'], df['health'], 'g-', label='健康值', marker='o')
    ax1.plot(df['timestamp'], df['charm'], 'b-', label='魅力值', marker='s')
    ax1.plot(df['timestamp'], df['wisdom'], 'r-', label='智慧值', marker='^')
    ax1.set_xlabel('时间')
    ax1.set_ylabel('属性值 (0-100)')
    ax1.set_ylim(0, 100)
    
    # 创建第二个Y轴用于金钱
    ax2 = ax1.twinx()
    ax2.plot(df['timestamp'], df['money'], 'm--', label='金钱', marker='x')
    ax2.set_ylabel('金钱 (元)')
    
    # 添加阶段标记
    stage_changes = df[df['stage'].diff() != 0]
    for idx, row in stage_changes.iterrows():
        ax1.axvline(x=row['timestamp'], color='k', linestyle='--', alpha=0.3)
        ax1.text(row['timestamp'], 105, f"阶段{int(row['stage'])}", 
                rotation=45, fontsize=9, alpha=0.7)
    
    # 添加图例和标题
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.title('玩家属性变化趋势')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig
