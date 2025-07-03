import tkinter as tk
from tkinter import ttk, messagebox
import json
import game_logic as gl
import visualization as vis
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("北师大求学模拟器")
        self.root.geometry("900x600")
        self.root.configure(bg='#f0f8ff')
        
        # 初始化游戏逻辑
        self.game = gl.GameLogic()
        
        # 创建主框架
        self.create_widgets()
        self.update_display()
        
    def create_widgets(self):
        # 顶部标题
        title_frame = tk.Frame(self.root, bg='#1e3c72', height=80)
        title_frame.pack(fill='x')
        
        title_label = tk.Label(title_frame, text="北京师范大学人工智能学院求学模拟器", 
                              font=("Microsoft YaHei", 18, "bold"), 
                              fg='white', bg='#1e3c72')
        title_label.pack(pady=20)
        
        # 主体框架
        main_frame = tk.Frame(self.root, bg='#f0f8ff')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # 左侧属性面板
        left_frame = tk.Frame(main_frame, bg='#e6f7ff', bd=2, relief='groove')
        left_frame.pack(side='left', fill='y', padx=(0, 10), pady=10)
        
        # 属性显示
        attr_frame = tk.LabelFrame(left_frame, text="学生属性", font=("Microsoft YaHei", 10), 
                                 bg='#e6f7ff', padx=10, pady=10)
        attr_frame.pack(padx=10, pady=5, fill='x')
        
        self.health_var = tk.StringVar()
        self.charm_var = tk.StringVar()
        self.wisdom_var = tk.StringVar()
        self.money_var = tk.StringVar()
        self.stage_var = tk.StringVar()
        
        tk.Label(attr_frame, text="健康值:", bg='#e6f7ff').grid(row=0, column=0, sticky='w')
        tk.Label(attr_frame, textvariable=self.health_var, bg='#e6f7ff').grid(row=0, column=1, sticky='w')
        
        tk.Label(attr_frame, text="魅力值:", bg='#e6f7ff').grid(row=1, column=0, sticky='w')
        tk.Label(attr_frame, textvariable=self.charm_var, bg='#e6f7ff').grid(row=1, column=1, sticky='w')
        
        tk.Label(attr_frame, text="智慧值:", bg='#e6f7ff').grid(row=2, column=0, sticky='w')
        tk.Label(attr_frame, textvariable=self.wisdom_var, bg='#e6f7ff').grid(row=2, column=1, sticky='w')
        
        tk.Label(attr_frame, text="经济状况:", bg='#e6f7ff').grid(row=3, column=0, sticky='w')
        tk.Label(attr_frame, textvariable=self.money_var, bg='#e6f7ff').grid(row=3, column=1, sticky='w')
        
        tk.Label(attr_frame, text="当前阶段:", bg='#e6f7ff').grid(row=4, column=0, sticky='w')
        tk.Label(attr_frame, textvariable=self.stage_var, bg='#e6f7ff').grid(row=4, column=1, sticky='w')
        
        # 属性可视化
        vis_frame = tk.LabelFrame(left_frame, text="属性变化", font=("Microsoft YaHei", 10), 
                                bg='#e6f7ff', padx=10, pady=10)
        vis_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        self.fig, self.ax = plt.subplots(figsize=(4, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=vis_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # 右侧事件面板
        right_frame = tk.Frame(main_frame, bg='#f0f8ff')
        right_frame.pack(side='right', fill='both', expand=True)
        
        # 事件描述
        event_frame = tk.LabelFrame(right_frame, text="校园事件", font=("Microsoft YaHei", 10), 
                                   bg='#e6f7ff', padx=10, pady=10)
        event_frame.pack(fill='both', expand=True, padx=(10, 0), pady=(0, 10))
        
        self.event_text = tk.Text(event_frame, height=8, width=50, font=("Microsoft YaHei", 10), 
                                 wrap='word', padx=10, pady=10)
        self.event_text.pack(fill='both', expand=True)
        self.event_text.config(state='disabled')
        
        # 选项按钮
        self.option_buttons = []
        for i in range(3):
            btn = tk.Button(event_frame, text="", font=("Microsoft YaHei", 9), 
                           command=lambda idx=i: self.select_option(idx),
                           bg='#4a86e8', fg='white', height=2, width=30)
            btn.pack(pady=5, fill='x')
            self.option_buttons.append(btn)
        
        # 控制按钮
        control_frame = tk.Frame(right_frame, bg='#f0f8ff')
        control_frame.pack(fill='x', padx=(10, 0), pady=(10, 0))
        
        tk.Button(control_frame, text="保存游戏", command=self.save_game, 
                 bg='#5cb85c', fg='white').pack(side='left', padx=5)
        tk.Button(control_frame, text="加载游戏", command=self.load_game, 
                 bg='#5bc0de', fg='white').pack(side='left', padx=5)
        tk.Button(control_frame, text="查看统计", command=self.show_stats, 
                 bg='#f0ad4e', fg='white').pack(side='left', padx=5)
        tk.Button(control_frame, text="退出游戏", command=self.root.quit, 
                 bg='#d9534f', fg='white').pack(side='right', padx=5)
    
    def update_display(self):
        # 更新属性显示
        self.health_var.set(f"{self.game.player['health']}/100")
        self.charm_var.set(f"{self.game.player['charm']}/100")
        self.wisdom_var.set(f"{self.game.player['wisdom']}/100")
        self.money_var.set(f"¥{self.game.player['money']}")
        self.stage_var.set(self.game.stages[self.game.player['stage']])
        
        # 更新事件显示
        self.event_text.config(state='normal')
        self.event_text.delete(1.0, tk.END)
        self.event_text.insert(tk.END, f"【{self.game.current_event['title']}】\n\n")
        self.event_text.insert(tk.END, self.game.current_event['description'])
        self.event_text.config(state='disabled')
        
        # 更新选项按钮
        for i, option in enumerate(self.game.current_event['options']):
            self.option_buttons[i].config(text=option['text'])
        
        # 更新可视化
        self.update_visualization()
    
    def update_visualization(self):
        # 清除之前的绘图
        self.ax.clear()
        
        # 绘制雷达图
        attributes = ['健康值', '魅力值', '智慧值', '经济状况']
        values = [
            self.game.player['health'],
            self.game.player['charm'],
            self.game.player['wisdom'],
            self.game.player['money'] / 100  # 缩放经济值以匹配其他属性
        ]
        
        # 雷达图需要闭合数据
        values += values[:1]
        attributes += attributes[:1]
        
        # 设置角度
        angles = [n / float(len(attributes)-1) * 2 * 3.14159 for n in range(len(attributes))]
        
        # 绘制雷达图
        self.ax = plt.subplot(111, polar=True)
        self.ax.plot(angles, values, 'o-', linewidth=2)
        self.ax.fill(angles, values, alpha=0.25)
        self.ax.set_xticks(angles[:-1])
        self.ax.set_xticklabels(attributes[:-1])
        self.ax.set_ylim(0, 100)
        self.ax.set_title('属性状态', size=12)
        
        self.canvas.draw()
    
    def select_option(self, option_idx):
        # 处理玩家选择
        self.game.process_choice(option_idx)
        
        # 检查游戏是否结束
        if self.game.check_game_over():
            messagebox.showinfo("游戏结束", self.game.get_ending())
            self.root.quit()
            return
        
        # 更新显示
        self.update_display()
    
    def save_game(self):
        self.game.save_game()
        messagebox.showinfo("保存成功", "游戏进度已保存！")
    
    def load_game(self):
        self.game.load_game()
        self.update_display()
        messagebox.showinfo("加载成功", "游戏进度已加载！")
    
    def show_stats(self):
        # 创建统计窗口
        stats_window = tk.Toplevel(self.root)
        stats_window.title("游戏统计")
        stats_window.geometry("600x400")
        
        # 添加统计图表
        fig = vis.plot_player_stats(self.game.player_history)
        canvas = FigureCanvasTkAgg(fig, master=stats_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # 添加事件统计
        event_frame = tk.Frame(stats_window)
        event_frame.pack(fill='x', padx=10, pady=5)
        
        event_types = ["学业", "社交", "生活", "恋爱"]
        event_counts = [0, 0, 0, 0]
        
        for event in self.game.event_history:
            if event['type'] == "学业":
                event_counts[0] += 1
            elif event['type'] == "社交":
                event_counts[1] += 1
            elif event['type'] == "生活":
                event_counts[2] += 1
            elif event['type'] == "恋爱":
                event_counts[3] += 1
        
        fig2 = plt.figure(figsize=(5, 3))
        ax2 = fig2.add_subplot(111)
        ax2.bar(event_types, event_counts, color=['#4c72b0', '#55a868', '#c44e52', '#8172b2'])
        ax2.set_title('事件类型统计')
        ax2.set_ylabel('发生次数')
        
        canvas2 = FigureCanvasTkAgg(fig2, master=stats_window)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill='x', padx=10, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()