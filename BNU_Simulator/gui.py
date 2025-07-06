import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from game_engine import GameEngine
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
##
from PIL import Image, ImageTk  
##

class StudySimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.engine = GameEngine()
        self.root.title("BNU-AIer的北师人生")
        self.root.geometry("1000x800")
        
        ## 
        #创建主容器 - 半透明效果
        self.main_container = tk.Frame(self.root, bg='#4871A1', bd=0)
        self.main_container.place(relx=0.5, rely=0.5, anchor='center', width=1000, height=800)  
        ##
        self.setup_ui()
        self.update_status()

    def setup_ui(self):
        
      ##
        #创建样式
        style = ttk.Style()
        style.configure('Custom.TFrame', background='#4871A1', foreground='#333333')  
        style.configure('Custom.TLabelframe', background='#F1F1F1', bordercolor='#2B428B')
        style.configure('Custom.TLabelframe.Label', background='#F1F1F1', foreground='#333333', font=('KaiTi', 10))
        style.configure('TButton', background='#4a90d9', foreground='#333333', font=('KaiTi', 12))
        style.map('TButton', background=[('active', '#2B428B')])

        style.configure("Status.TLabel", 
               background="#4871A1",  # 必须与父框架一致
               foreground="#F5FFFA",
               font=("SimSun", 12),
               padding=5)  # 增加内边距填充空隙
      ##
        
        # 主框架
      ##
        #修改 padding10->5 增加style='Custom.TFrame'
        main_frame = ttk.Frame(self.main_container, padding=5, style='Custom.TFrame')
      ##
        main_frame.pack(fill=tk.BOTH, expand=True)  
        
      ##
        # 配置主框架的列权重
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=0)
      ##

        # 顶部状态栏
        self.status_frame = ttk.Frame(main_frame,style="Custom.TFrame", padding=(5, 2) )# 应用背景色样式
        self.status_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)

        # 中间操作区
        self.action_frame = ttk.LabelFrame(main_frame, text="操作", padding=10, style='Custom.TLabelframe')
        self.action_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # 右侧板块
        self.right_panel = ttk.LabelFrame(main_frame, text="属性展示", padding=10, style='Custom.TLabelframe')
        self.right_panel.grid(row=1, column=1, sticky="ns", padx=5, pady=5, ipadx=0, ipady=0)

        # 右侧板块内容
        self.load_image()
        self.create_attribute_bars()

        # 底部日志区
        log_frame = ttk.LabelFrame(main_frame, text="游戏日志", padding=10, style='Custom.TLabelframe')
        log_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        # 使用KaiTi字体
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, font=("KaiTi", 12))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)

        # 底部按钮区
        btn_frame = ttk.Frame(main_frame,style="Custom.TFrame")
        btn_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)

        # 定义按钮样式 - 使用KaiTi字体
        style.configure("TButton", font=("SimSun", 12), width=14)
        style.configure("Confirm.TButton", font=("KaiTi", 12), width=12)
        style.configure("EventChoice.TButton", font=("KaiTi", 16), width=30)

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
            image_path = "images/bnu.jpg"
            image = Image.open(image_path)
            image = image.resize((150, 150), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)

            image_label = ttk.Label(self.right_panel, image=self.photo)
            image_label.pack(pady=30)
        except Exception as e:
            print(f"加载图片失败: {e}")
            ttk.Label(self.right_panel, text="图片加载失败", font=("KaiTi", 12)).pack(pady=5)

    def create_attribute_bars(self):
        self.attribute_bars = {}
        attributes = ["健康", "魅力", "智慧", "压力"]
        
        attribute_container = ttk.Frame(self.right_panel)
        attribute_container.pack(fill=tk.BOTH, expand=True, pady=(0, 30))

        for attr in attributes:
            frame = ttk.Frame(attribute_container)
            frame.pack(pady=10, fill=tk.X)

            # 使用KaiTi字体
            label = ttk.Label(frame, text=f"{attr}: ", width=5, anchor="e", font=("SimSun", 14))
            label.pack(side=tk.LEFT, padx=(0, 5))

            bar = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=130, mode='determinate')
            bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.attribute_bars[attr] = bar

    def update_status(self):
        for widget in self.status_frame.winfo_children():
            widget.destroy()

        p = self.engine.player
        num_trans = {1: "一", 2: "二", 3: "三", 4: "四"}

        #
        # 创建一个样式对象
        style = ttk.Style()
        style.configure("Status.TLabel", background="#4871A1",foreground='#F5FFFA' ,font=('KaiTi', 13, 'bold'),padding=2)  # 设置背景色和内边距
        
        # 使用KaiTi字体
        ttk.Label(self.status_frame, text=f"学年: 大{num_trans[p.year]}", font=("SimSun", 12),style="Status.TLabel").pack(side=tk.LEFT, padx=10)
        ttk.Label(self.status_frame, text=f"学分: {p.credits}/{self.engine.course_system.total_credits_needed}", font=("SimSun", 12),style="Status.TLabel").pack(side=tk.LEFT, padx=10)
        ttk.Label(self.status_frame, text=f"健康: {p.health}", font=("SimSun", 12),style="Status.TLabel").pack(side=tk.LEFT, padx=10)
        ttk.Label(self.status_frame, text=f"魅力: {p.charm}", font=("SimSun", 12),style="Status.TLabel").pack(side=tk.LEFT, padx=10)
        ttk.Label(self.status_frame, text=f"智慧: {p.wisdom}", font=("SimSun", 12),style="Status.TLabel").pack(side=tk.LEFT, padx=10)
        ttk.Label(self.status_frame, text=f"压力: {p.pressure}", font=("SimSun", 12),style="Status.TLabel").pack(side=tk.LEFT, padx=10)
        ttk.Label(self.status_frame, text=f"状态: {p.relationship}", font=("SimSun", 12),style="Status.TLabel").pack(side=tk.LEFT, padx=10)

        #

        self.update_attribute_bars()

    def update_attribute_bars(self):
        p = self.engine.player
        attributes = {
            "健康": p.health,
            "魅力": p.charm,
            "智慧": p.wisdom,
            "压力": p.pressure
        }

        for attr, value in attributes.items():
            bar = self.attribute_bars[attr]
            bar["value"] = value

    def add_log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.insert(tk.END, "-" * 50 + "\n")
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

        elif self.engine.state == "EVENT_HANDLING":
            self.show_event()

    def clear_action_panel(self):
        for widget in self.action_frame.winfo_children():
            widget.destroy()

    def show_course_selection(self):
        self.clear_action_panel()

        # 使用KaiTi字体
        ttk.Label(self.action_frame, text="选择本学期课程:", font=("SimHei", 14, "bold")).pack(anchor="w", pady=10)

        loading_label = ttk.Label(self.action_frame, text="加载课程中...", font=("SimHei", 12))
        loading_label.pack(pady=10)
        self.root.update()

        available_courses = self.engine.get_available_courses()
        loading_label.destroy()

        if not available_courses:
            ttk.Label(self.action_frame, text="本学期没有可选课程!", font=("SimHei", 12)).pack(pady=10)
            return

        container = ttk.Frame(self.action_frame)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas = tk.Canvas(container, yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=canvas.yview)

        scrollable_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self.course_vars = {}
        for course in available_courses:
            var = tk.BooleanVar()
            frame = ttk.Frame(scrollable_frame, padding=5)
            frame.pack(fill=tk.X, padx=5, pady=5)

            ttk.Checkbutton(frame, variable=var).pack(side=tk.LEFT, padx=5)
            # 使用KaiTi字体
            ttk.Label(frame, text=course['name'], width=25, anchor="w", font=("KaiTi", 12)).pack(side=tk.LEFT)
            ttk.Label(frame, text=f"模块: {course['module']}", font=("KaiTi", 12)).pack(side=tk.LEFT, padx=10)
            ttk.Label(frame, text=f"学分: {course['credit']}", font=("KaiTi", 12)).pack(side=tk.LEFT, padx=5)
            ttk.Label(frame, text=f"压力: {course['pressure']}", font=("KaiTi", 12)).pack(side=tk.LEFT, padx=5)

            self.course_vars[course['id']] = (var, course)

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
        self.show_event()

    def show_event(self):
        self.clear_action_panel()

        event = self.engine.current_event
        if not event:
            self.add_log("本学期没有事件发生")
            self.engine.state = "YEAR_END"
            return

        # 使用KaiTi字体
        ttk.Label(self.action_frame, text="事件:", font=("SimHei", 15, "bold")).pack(anchor="w", pady=10)
        ttk.Label(self.action_frame, text=event['description'], wraplength=500, font=("KaiTi", 14)).pack(anchor="w", pady=5)
        ttk.Label(self.action_frame, text="选择:", font=("SimHei", 15, "bold")).pack(anchor="w", pady=10)

        for i, choice in enumerate(event['choices']):
            btn = ttk.Button(
                self.action_frame,
                text=choice['description'],
                command=lambda idx=i: self.handle_event_choice(idx),
                style="EventChoice.TButton"
            )
            btn.pack(pady=10)

    def handle_event_choice(self, choice_idx):
        self.add_log(self.engine.handle_event_choice(choice_idx))
        self.update_status()

        if self.engine.state == "EVENT_HANDLING":
            self.show_event()
        else:
            self.clear_action_panel()
            self.next_btn.config(state=tk.NORMAL)

    def show_game_over(self):
        self.clear_action_panel()
        # 使用KaiTi字体
        ttk.Label(self.action_frame, text="游戏结束!", font=("SimHei", 16, "bold")).pack(pady=10)
        ttk.Label(self.action_frame, text=self.engine.get_ending(), font=("SimHei", 14)).pack(pady=5)

    def show_plot(self):
        fig = self.engine.plot_attributes()
        if fig:
            plot_window = tk.Toplevel(self.root)
            plot_window.title("成长轨迹")

            canvas = FigureCanvasTkAgg(fig, master=plot_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            ttk.Button(plot_window, text="关闭", command=plot_window.destroy).pack(pady=10)
        else:
            messagebox.showinfo("提示", "暂无数据可展示")
