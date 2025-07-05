import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from game_engine import GameEngine
import matplotlib
matplotlib.use('TkAgg')  # 确保matplotlib使用TkAgg后端
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
'''hahhg'''
class StudySimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.engine = GameEngine()
        self.root.title("大学生活模拟器")
        self.root.geometry("800x600")
        self.setup_ui()
        self.update_status()
    
    def setup_ui(self):
        # 主布局
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 顶部状态栏
        self.status_frame = ttk.Frame(main_frame)
        self.status_frame.pack(fill=tk.X, pady=5)
        
        # 中间操作区
        self.action_frame = ttk.LabelFrame(main_frame, text="操作", padding=10)
        self.action_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 底部日志区
        log_frame = ttk.LabelFrame(main_frame, text="游戏日志", padding=10)
        log_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)
        
        # 底部按钮区
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        self.start_btn = ttk.Button(btn_frame, text="开始游戏", command=self.start_game)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = ttk.Button(btn_frame, text="继续", command=self.next_step, state=tk.DISABLED)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        self.plot_btn = ttk.Button(btn_frame, text="查看成长轨迹", command=self.show_plot, state=tk.DISABLED)
        self.plot_btn.pack(side=tk.RIGHT, padx=5)
    
    def update_status(self):
        """更新状态栏"""
        # 清除状态栏
        for widget in self.status_frame.winfo_children():
            widget.destroy()
        
        # 添加状态信息
        p = self.engine.player
        ttk.Label(self.status_frame, text=f"学年: 大{p.year}").pack(side=tk.LEFT, padx=10)
        ttk.Label(self.status_frame, text=f"学分: {p.credits}/{self.engine.course_system.total_credits_needed}").pack(side=tk.LEFT, padx=10)
        ttk.Label(self.status_frame, text=f"健康: {p.health}").pack(side=tk.LEFT, padx=10)
        ttk.Label(self.status_frame, text=f"魅力: {p.charm}").pack(side=tk.LEFT, padx=10)
        ttk.Label(self.status_frame, text=f"智慧: {p.wisdom}").pack(side=tk.LEFT, padx=10)
        ttk.Label(self.status_frame, text=f"压力: {p.pressure}").pack(side=tk.LEFT, padx=10)
        ttk.Label(self.status_frame, text=f"状态: {p.relationship}").pack(side=tk.LEFT, padx=10)
    
    def add_log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)
    
    def start_game(self):
        self.clear_action_panel()
        self.add_log(self.engine.start_new_game())
        self.update_status()
        self.show_course_selection()
        self.start_btn.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL)
        self.plot_btn.config(state=tk.NORMAL)
    
    def next_step(self):
        if self.engine.state == "YEAR_END":
            self.add_log(self.engine.next_year())
            
            if self.engine.state == "GAME_OVER":
                self.next_btn.config(state=tk.DISABLED)
                self.show_game_over()
            else:
                self.update_status()
                self.show_course_selection()
    
    def clear_action_panel(self):
        for widget in self.action_frame.winfo_children():
            widget.destroy()
    
    def show_course_selection(self):
        self.clear_action_panel()
        
        ttk.Label(self.action_frame, text="选择本学期课程:", font=("", 11, "bold")).pack(anchor="w", pady=5)
        
        # 添加加载提示
        loading_label = ttk.Label(self.action_frame, text="加载课程中...")
        loading_label.pack(pady=10)
        self.root.update()  # 强制刷新界面
        
        available_courses = self.engine.get_available_courses()
        loading_label.destroy()  # 移除加载提示
        
        if not available_courses:
            ttk.Label(self.action_frame, text="本学期没有可选课程!").pack(pady=10)
            return
        
        # 创建滚动区域
        container = ttk.Frame(self.action_frame)
        container.pack(fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建Canvas
        canvas = tk.Canvas(container, yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=canvas.yview)
        
        # 创建内部框架用于放置课程
        scrollable_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # 配置Canvas滚动
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # 添加课程选择
        self.course_vars = {}
        for course in available_courses:
            var = tk.BooleanVar()
            frame = ttk.Frame(scrollable_frame, padding=5)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            ttk.Checkbutton(frame, variable=var).pack(side=tk.LEFT, padx=5)
            ttk.Label(frame, text=course['name'], width=25, anchor="w").pack(side=tk.LEFT)
            ttk.Label(frame, text=f"模块: {course['module']}").pack(side=tk.LEFT, padx=10)
            ttk.Label(frame, text=f"学分: {course['credit']}").pack(side=tk.LEFT, padx=5)
            ttk.Label(frame, text=f"压力: {course['pressure']}").pack(side=tk.LEFT, padx=5)
            
            self.course_vars[course['id']] = (var, course)
        
        # 确认按钮
        ttk.Button(self.action_frame, text="确认选课", command=self.confirm_courses).pack(pady=10)
    
    def confirm_courses(self):
        selected = []
        for _, (var, course) in self.course_vars.items():
            if var.get():
                selected.append(course)
        
        if not selected:
            messagebox.showwarning("警告", "请至少选择一门课程!")
            return
        
        self.add_log(self.engine.select_courses(selected))
        self.update_status()
        self.show_event()
    
    def show_event(self):
        self.clear_action_panel()
        
        event = self.engine.current_event
        if not event:
            self.add_log("本学期没有事件发生")
            self.engine.state = "YEAR_END"
            return
        
        ttk.Label(self.action_frame, text="事件:", font=("", 11, "bold")).pack(anchor="w", pady=5)
        ttk.Label(self.action_frame, text=event['description'], wraplength=500).pack(anchor="w", pady=5)
        
        ttk.Label(self.action_frame, text="选择:", font=("", 11, "bold")).pack(anchor="w", pady=10)
        
        for i, choice in enumerate(event['choices']):
            btn = ttk.Button(
                self.action_frame, 
                text=choice['description'], 
                command=lambda idx=i: self.handle_event_choice(idx),
                width=40
            )
            btn.pack(pady=3)
    
    def handle_event_choice(self, choice_idx):
        self.add_log(self.engine.handle_event_choice(choice_idx))
        self.update_status()
        self.clear_action_panel()
    
    def show_game_over(self):
        self.clear_action_panel()
        ttk.Label(self.action_frame, text="游戏结束!", font=("", 14, "bold")).pack(pady=10)
        ttk.Label(self.action_frame, text=self.engine.get_ending(), font=("", 12)).pack(pady=5)
    
    # 添加缺失的 show_plot 方法
    def show_plot(self):
        fig = self.engine.plot_attributes()
        if fig:
            # 创建新窗口显示图表
            plot_window = tk.Toplevel(self.root)
            plot_window.title("成长轨迹")
            
            canvas = FigureCanvasTkAgg(fig, master=plot_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # 添加关闭按钮
            ttk.Button(plot_window, text="关闭", command=plot_window.destroy).pack(pady=10)
        else:
            messagebox.showinfo("提示", "暂无数据可展示")
