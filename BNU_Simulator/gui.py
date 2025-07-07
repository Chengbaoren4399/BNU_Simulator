import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from game_engine import GameEngine
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image,ImageTk,ImageEnhance 

class StudySimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.engine = GameEngine()
        self.root.title("BNU-AIer的北师人生")
        self.root.geometry("1000x800")
        self.main_container = tk.Frame(self.root, bg='#4871A1', bd=0)
        self.main_container.place(relx=0.5, rely=0.5, anchor='center', width=1000, height=800)  
        self.setup_ui()
        self.update_status()
    
    def setup_ui(self):
        # 创建样式
        style = ttk.Style()
        style.configure('Custom.TFrame', background='#4871A1', foreground='#333333')  
        style.configure('Custom.TLabelframe', background='#F1F1F1', bordercolor='#2B428B')
        style.configure('Custom.TLabelframe.Label', background='#F1F1F1', foreground='#333333', font=('Simhei', 10))
        style.configure('TButton', background='#4a90d9', foreground='#333333', font=('Simhei', 12))
        style.map('TButton', background=[('active', '#2B428B')])

        style.configure("Status.TLabel", 
               background="#4871A1",
               foreground="#F5FFFA",
               font=("Simhei", 12),
               padding=5)

        # 主框架
        main_frame = ttk.Frame(self.main_container, padding=5, style='Custom.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        # 配置主框架的列权重
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=0)
        
        # 学分进度条框架
        self.credits_frame = ttk.LabelFrame(main_frame, text="学分进度", padding=10)
        self.credits_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # 顶部状态栏
        self.status_frame = ttk.Frame(main_frame, style="Custom.TFrame", padding=(5, 2))
        self.status_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=2)
        
        # 中间操作区
        self.action_frame = ttk.LabelFrame(main_frame, text="操作", padding=10, style='Custom.TLabelframe')
        self.action_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        
        # 右侧板块
        self.right_panel = ttk.LabelFrame(main_frame, text="属性展示", padding=10, style='Custom.TLabelframe')
        self.right_panel.grid(row=2, column=1, sticky="ns", padx=5, pady=5, ipadx=0, ipady=0)
        
        # 底部日志区
        log_frame = ttk.LabelFrame(main_frame, text="游戏日志", padding=10, style='Custom.TLabelframe')
        log_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        # 底部按钮区
        btn_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        btn_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)
        
        # 右侧板块内容
        self.load_image()
        self.create_attribute_bars()

        # 使用Simhei字体
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, font=("Simhei", 12))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)
        
        self.start_btn = ttk.Button(btn_frame, text="开始游戏", command=self.start_game, style="TButton")
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = ttk.Button(btn_frame, text="继续", command=self.next_step, state=tk.DISABLED, style="TButton")
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        self.plot_btn = ttk.Button(btn_frame, text="查看成长轨迹", command=self.show_plot, state=tk.DISABLED, style="TButton")
        self.plot_btn.pack(side=tk.RIGHT, padx=5)

        # 配置主窗口的行和列权重
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

    def load_image(self):
        try:
            image_path = "images/AI.jpg"
        
            # 加载并处理图像
            image = Image.open(image_path)
            image = image.convert("RGB")
            image = image.resize((150, 150), Image.LANCZOS)
        
            # 增加亮度
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.5)
        
            # 根据智慧值调整
            adjusted_image = self.adjust_image(image, self.engine.player.wisdom)
        
            # 更新或创建图像标签
            if hasattr(self, 'photo_label'):
            # 更新现有标签
                new_photo = ImageTk.PhotoImage(adjusted_image)
                self.photo_label.configure(image=new_photo)
                self.photo_label.image = new_photo  # 保持引用
            else:
                # 首次创建标签
                self.photo = ImageTk.PhotoImage(adjusted_image)
                self.photo_label = ttk.Label(self.right_panel, image=self.photo)
                self.photo_label.image = self.photo  # 保持引用
                self.photo_label.pack(pady=30)
        
            # 强制刷新UI
            self.right_panel.update_idletasks()
        
        except Exception as e:
            print(f"加载图片失败: {e}")
            if hasattr(self, 'photo_label'):
                self.photo_label.destroy()
            ttk.Label(self.right_panel, text=f"图片错误: {str(e)}", font=("KaiTi", 10)).pack(pady=5)

    def adjust_image(self, image, wisdom):
        wisdom = max(0, min(wisdom, 100))

        image_path = "images/sos.png"
        sos = Image.open(image_path)
        sos = sos.convert("RGBA")
        sos = sos.resize((150, 150), Image.LANCZOS)
    
        # 创建覆盖层
        overlay = Image.new('RGB', image.size, (39, 64, 143))
    
        # 计算透明度
        if wisdom <= 30:
            new_image = sos
        elif 30 < wisdom <= 50:
            new_image = overlay
        elif wisdom >= 90:
            new_image = Image.blend(overlay, image, 1)  # 原图显现
        else:
            # 50-90区间线性渐变
            alpha = (wisdom - 50) / 40.0
            new_image = Image.blend(overlay, image, alpha)

        return new_image

    #生成属性进度条
    def create_attribute_bars(self):
        self.attribute_bars = {}
        attributes = ["健康", "魅力", "智慧", "压力"]
        
        attribute_container = ttk.Frame(self.right_panel)
        attribute_container.pack(fill=tk.BOTH, expand=True, pady=(0, 30))

        for attr in attributes:
            frame = ttk.Frame(attribute_container)
            frame.pack(pady=10, fill=tk.X)

            label = ttk.Label(frame, text=f"{attr}: ", width=5, anchor="e", font=("Simhei", 12))
            label.pack(side=tk.LEFT, padx=(0, 5))

            bar = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=130, mode='determinate')
            bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.attribute_bars[attr] = bar
    
    def update_status(self):
        """更新状态栏和学分进度"""
        # 清除状态栏
        for widget in self.status_frame.winfo_children():
            widget.destroy()
    
        # 添加状态信息
        p = self.engine.player
        num_trans = {1:"一",2:"二",3:"三",4:"四"}

        # 创建一个样式对象
        style = ttk.Style()
        style.configure("Status.TLabel", background="#4871A1", foreground='#F5FFFA', 
                        font=('Simhei', 12), padding=2)
        
        ttk.Label(self.status_frame, text=f"学年: 大{num_trans[p.year]}", style="Status.TLabel").pack(side=tk.LEFT, padx=10)
        ttk.Label(self.status_frame, text=f"学分: {p.credits}/{self.engine.course_system.total_credits_needed}", style="Status.TLabel").pack(side=tk.LEFT, padx=10)
        ttk.Label(self.status_frame, text=f"健康: {p.health}", style="Status.TLabel").pack(side=tk.LEFT, padx=10)
        ttk.Label(self.status_frame, text=f"魅力: {p.charm}", style="Status.TLabel").pack(side=tk.LEFT, padx=10)
        ttk.Label(self.status_frame, text=f"智慧: {p.wisdom}", style="Status.TLabel").pack(side=tk.LEFT, padx=10)
        ttk.Label(self.status_frame, text=f"压力: {p.pressure}", style="Status.TLabel").pack(side=tk.LEFT, padx=10)
        ttk.Label(self.status_frame, text=f"状态: {p.relationship}", style="Status.TLabel").pack(side=tk.LEFT, padx=10)

        self.update_attribute_bars()

        # 更新学分进度条
        for widget in self.credits_frame.winfo_children():
            widget.destroy()
            
        # 必修课进度
        ttk.Label(self.credits_frame, text="必修课:", font=("Simhei", 10)).grid(row=0, column=0, sticky="w", padx=5)
        required_progress = ttk.Progressbar(
            self.credits_frame, 
            length=200, 
            mode='determinate',
            maximum=self.engine.course_system.required_credits_needed
        )
        required_progress.grid(row=0, column=1, padx=5)
        required_progress['value'] = p.required_credits
        ttk.Label(self.credits_frame, 
                 text=f"{p.required_credits}/{self.engine.course_system.required_credits_needed}",
                 font=("Simhei", 10)).grid(row=0, column=2, padx=5)
        
        # 专业选修I进度
        ttk.Label(self.credits_frame, text="专业选修I:", font=("Simhei", 10)).grid(row=0, column=3, sticky="w", padx=5)
        electiveI_progress = ttk.Progressbar(
            self.credits_frame, 
            length=150, 
            mode='determinate',
            maximum=self.engine.course_system.electiveI_credits_needed
        )
        electiveI_progress.grid(row=0, column=4, padx=5)
        electiveI_progress['value'] = p.electiveI_credits
        ttk.Label(self.credits_frame, 
                 text=f"{p.electiveI_credits}/{self.engine.course_system.electiveI_credits_needed}",
                 font=("Simhei", 10)).grid(row=0, column=5, padx=5)
        
        # 专业选修II进度
        ttk.Label(self.credits_frame, text="专业选修II:", font=("Simhei", 10)).grid(row=0, column=6, sticky="w", padx=5)
        electiveII_progress = ttk.Progressbar(
            self.credits_frame, 
            length=150, 
            mode='determinate',
            maximum=self.engine.course_system.electiveII_credits_needed
        )
        electiveII_progress.grid(row=0, column=7, padx=5)
        electiveII_progress['value'] = p.electiveII_credits
        ttk.Label(self.credits_frame, 
                 text=f"{p.electiveII_credits}/{self.engine.course_system.electiveII_credits_needed}",
                 font=("Simhei", 10)).grid(row=0, column=8, padx=5)
        self.load_image()

    def show_pressure_warning(self, level):
        """显示压力警告窗口"""
        if level == 1:
            messagebox.showwarning("压力过载", 
                "你的压力值过高！\n\n"
                "请注意调节学习与生活平衡，合理安排时间。\n"
                "可以考虑参加一些放松活动或减少课程负担。")
        elif level == 2:
            messagebox.showerror("游戏结束", 
                "压力值超过200！你已无法正常生活。\n\n"
                "大学四年生活压力过大导致你身心俱疲，无法继续学业。\n"
                "游戏将重新开始。")
            self.restart_game()
        
    def update_attribute_bars(self):
        p = self.engine.player
        attributes = {
            "健康": p.health,
            "魅力": p.charm,
            "智慧": p.wisdom,
            "压力": p.pressure
        }

        max_values = {
        "健康": 100,
        "魅力": 100,
        "智慧": 100,
        "压力": 200  # 压力最大值为200
        }

        for attr, value in attributes.items():
            bar = self.attribute_bars[attr]
            bar["maximum"] = max_values[attr]
            bar["value"] = min(value, max_values[attr])#不超过最大值
        
    def add_log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.insert(tk.END, "-"*50 + "\n")
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
            self.engine.player.pressure_warning_shown = False
            
            if self.engine.state == "GAME_OVER":
                self.next_btn.config(state=tk.DISABLED)
                self.show_game_over()
            else:
                self.update_status()
                self.show_course_selection()
        
        elif self.engine.state == "EVENT_HANDLING":
            self.show_event()
    
    def clear_action_panel(self):
        for widget in self.action_frame.winfo_children():
            widget.destroy()
    
    def show_course_selection(self):
        self.clear_action_panel()
        
        # 使用Simhei字体
        ttk.Label(self.action_frame, text="选择本学年课程:", font=("KaiTi", 14, "bold")).pack(anchor="w", pady=10)

        loading_label = ttk.Label(self.action_frame, text="加载课程中...", font=("KaiTi", 12))
        loading_label.pack(pady=10)
        self.root.update()  # 刷新界面
        
        available_courses = self.engine.get_available_courses()
        loading_label.destroy()  # 移除加载提示
        
        if not available_courses:
            ttk.Label(self.action_frame, text="本学期没有可选课程!", font=("KaiTi", 12)).pack(pady=10)
            return
        
        # 创建滚动区域
        container = ttk.Frame(self.action_frame)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
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
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self.course_vars = {}
        for course in available_courses:
            var = tk.BooleanVar()
            frame = ttk.Frame(scrollable_frame, padding=5)
            frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Checkbutton(frame, variable=var).pack(side=tk.LEFT, padx=5)
            ttk.Label(frame, text=course['name'], width=25, anchor="w", font=("KaiTi", 8)).pack(side=tk.LEFT)
            
            # 显示课程类型
            type_color = {
                "必修课": "red",
                "专业选修I": "blue",
                "专业选修II": "green"
            }
            type_label = ttk.Label(frame, text=course['type'], font=("KaiTi", 8),width=10,
                                  foreground=type_color.get(course['type'], "black"))
            type_label.pack(side=tk.LEFT, padx=10)

            ttk.Label(frame, text=f"模块: {course['module']}", font=("KaiTi", 8),width=23).pack(side=tk.LEFT, padx=10)
            years = ', '.join(map(str, course['year_available']))
            ttk.Label(frame, text=f"开课学年: {years}", width=15, font=("KaiTi", 8)).pack(side=tk.LEFT, padx=5)
            ttk.Label(frame, text=f"学分: {course['credit']}", font=("KaiTi", 8)).pack(side=tk.LEFT, padx=5)
            ttk.Label(frame, text=f"压力: {course['pressure']}", font=("KaiTi", 8)).pack(side=tk.LEFT, padx=5)
            
            self.course_vars[course['id']] = (var, course)
        
        # 确认按钮
        confirm_btn_frame = ttk.Frame(self.action_frame)
        confirm_btn_frame.pack(pady=10, fill=tk.X)
        ttk.Button(confirm_btn_frame, text="确认选课", command=self.confirm_courses, 
                  style="Confirm.TButton").pack(side=tk.RIGHT)
    
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

        # 检查压力状态
        pressure_status = self.engine.check_pressure()
        if pressure_status > 0:
            self.show_pressure_warning(pressure_status)
            
            # 如果压力爆表，不需要再显示事件
            if pressure_status == 2:
                return
        
        self.show_event()
    
    def show_event(self):
        self.clear_action_panel()
        
        event = self.engine.current_event
        if not event:
            self.add_log("本学期没有事件发生")
            self.engine.state = "YEAR_END"
            return
        
        ttk.Label(self.action_frame, text="事件:", font=("KaiTi", 12, "bold")).pack(anchor="w", pady=10)
        ttk.Label(self.action_frame, text=event['description'], wraplength=500, 
                 font=("KaiTi", 12)).pack(anchor="w", pady=5)
        ttk.Label(self.action_frame, text="选择:", font=("KaiTi", 12, "bold")).pack(anchor="w", pady=10)

        for i, choice in enumerate(event['choices']):
            btn = ttk.Button(
                self.action_frame, 
                text=choice['description'], 
                command=lambda idx=i: self.handle_event_choice(idx),
                style="EventChoice.TButton"
            )
            btn.pack(pady=10, fill=tk.X)
    
    def handle_event_choice(self, choice_idx):
        self.add_log(self.engine.handle_event_choice(choice_idx))
        self.update_status()
        
        # 检查压力状态
        pressure_status = self.engine.check_pressure()
        if pressure_status > 0:
            self.show_pressure_warning(pressure_status)
            
            # 如果压力爆表，不需要再显示事件
            if pressure_status == 2:
                self.clear_action_panel()
                self.next_btn.config(state=tk.NORMAL)
                return
        
        if self.engine.state == "EVENT_HANDLING":
            self.show_event()
        else:
            self.clear_action_panel()
            self.next_btn.config(state=tk.NORMAL)
    
    def show_game_over(self):
        self.clear_action_panel()
        ttk.Label(self.action_frame, text="游戏结束!", font=("KaiTi", 16, "bold")).pack(pady=10)
        ending_text = self.engine.get_ending()
        frame = ttk.Frame(self.action_frame)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        ending_textbox = tk.Text(
            frame, 
            wrap=tk.WORD, 
            font=("KaiTi", 12),
            yscrollcommand=scrollbar.set,
            padx=10,
            pady=10,
            height=15
        )
        ending_textbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=ending_textbox.yview)
        
        # 插入结局文本
        ending_textbox.insert(tk.END, ending_text)
        ending_textbox.config(state=tk.DISABLED) 
        
        # 添加重新开始按钮
        ttk.Button(
            self.action_frame, 
            text="重新开始游戏", 
            command=self.restart_game,
            style="TButton"
        ).pack(pady=10)
    
    # 展示成长轨迹图
    # 展示成长轨迹图
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
            ttk.Button(plot_window, text="关闭", command=plot_window.destroy, style="TButton").pack(pady=10)
        else:
            messagebox.showinfo("提示", "暂无数据可展示")

    def restart_game(self):
        """重新开始游戏"""
        self.start_btn.config(state=tk.NORMAL)
        self.next_btn.config(state=tk.DISABLED)
        self.plot_btn.config(state=tk.DISABLED)
        self.start_game()