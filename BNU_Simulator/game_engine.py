from course_system import CourseSystem
from event_system import EventSystem
from attribute_system import Player
import matplotlib.pyplot as plt
import random
from llm_api import DeepSeekAPI

print(plt.style.available)
class GameEngine:
    STATES = ["IDLE", "COURSE_SELECTION", "EVENT_HANDLING", "YEAR_END", "GAME_OVER"]

    def __init__(self):
        self.player = Player()
        self.course_system = CourseSystem()
        self.event_system = EventSystem()
        self.state = "IDLE"
        self.current_event = None
        self.attribute_history = []
        self.event_queue = []
        self.llm_generator = DeepSeekAPI()
        print("LLM生成器已初始化")
        
    def start_new_game(self):
        self.player.reset()
        self.state = "COURSE_SELECTION"
        self.attribute_history = []
        self.event_queue = []
        return "欢迎来到BNU-AIer北师人生模拟器! 请选择本学期课程。"
    
    def select_courses(self, selected_courses):
        if not selected_courses:
            return "请至少选择一门课程!"
        
        self.player.selected_courses = selected_courses
        credits_earned = self.course_system.calculate_credits(selected_courses)
        pressure_added = self.course_system.calculate_pressure(selected_courses)
        
        # 更新分类学分
        for course in selected_courses:
            if course['type'] == "必修课":
                self.player.required_credits += course['credit']
            elif course['type'] == "专业选修I":
                self.player.electiveI_credits += course['credit']
            elif course['type'] == "专业选修II":
                self.player.electiveII_credits += course['credit']

        self.player.credits += credits_earned
        self.player.pressure += pressure_added
        self.player.courses_taken.extend([c['id'] for c in selected_courses])
        
        self.event_queue = self.event_system.get_non_repeating_events(self.player.year, 10)

        if self.event_queue:
            self.state = "EVENT_HANDLING"
            self.current_event = self.event_queue.pop(0)  # 取出第一个事件
            self.record_attributes()
            return f"选课完成! 获得学分: {credits_earned}\n本学期将有10个事件需要处理!"
        else:
            self.state = "YEAR_END"
            return f"选课完成! 获得学分: {credits_earned}\n本学期没有事件发生"
    
    def handle_event_choice(self, choice_idx):
        if not self.current_event or choice_idx >= len(self.current_event['choices']):
            return "无效选择!"
        
        event_description = self.current_event['description']
        choice = self.current_event['choices'][choice_idx]

        prev_health = self.player.health
        prev_charm = self.player.charm
        prev_wisdom = self.player.wisdom
        prev_pressure = self.player.pressure

        self.player.apply_effects(choice['effects'])
        self.record_attributes()

        #属性变化数值
        health_change = self.player.health - prev_health
        charm_change = self.player.charm - prev_charm
        wisdom_change = self.player.wisdom - prev_wisdom
        pressure_change = self.player.pressure - prev_pressure
        
        changes = []
        if health_change != 0:
            changes.append(f"健康 {'+' if health_change > 0 else ''}{health_change}")
        if charm_change != 0:
            changes.append(f"魅力 {'+' if charm_change > 0 else ''}{charm_change}")
        if wisdom_change != 0:
            changes.append(f"智慧 {'+' if wisdom_change > 0 else ''}{wisdom_change}")
        if pressure_change != 0:
            changes.append(f"压力 {'+' if pressure_change > 0 else ''}{pressure_change}")
        
        # 关系变化
        if "relationship" in choice['effects']:
            changes.append(f"关系: {self.player.relationship}")
        
        # 格式化消息
        message = f"事件: {event_description}\n"
        message += f"你的选择: {choice['description']}\n"
        if changes:
            message += f"属性变化: {', '.join(changes)}"
        else:
            message += "没有属性变化"
        
        # 检查队列中是否还有事件
        if self.event_queue:
            self.current_event = self.event_queue.pop(0)
        else:
            self.state = "YEAR_END"  # 确保状态正确更新
            message+=f"\n本学期所有事件已处理完毕!"
        
        return message
    
    def check_pressure(self):
        """检查压力值并返回警告级别
        0: 正常
        1: 压力过载（>100）
        2: 压力爆表（>200），游戏结束
        """
        if self.player.pressure > 200:
            return 2
        elif self.player.pressure > 100 and not self.player.pressure_warning_shown:
            self.player.pressure_warning_shown = True  # 标记为已显示
            return 1
        return 0
    
    def next_year(self):
        self.player.next_year()
        self.state = "COURSE_SELECTION" if self.player.year <= 4 else "GAME_OVER"
        
        if self.player.year > 4:
            return self.get_ending()
        
        num_trans = {1:"一",2:"二",3:"三",4:"四"}
        return f"进入大{num_trans[self.player.year]}学年!"
    
    def get_available_courses(self):
        return self.course_system.get_available_courses(
            self.player.year, self.player.courses_taken
        )
    
    def record_attributes(self):
        self.attribute_history.append({
            "year": self.player.year,
            "health": self.player.health,
            "charm": self.player.charm,
            "wisdom": self.player.wisdom,
            "pressure": self.player.pressure,
            "credits": self.player.credits
        })
    
    def determine_outcome_type(self):
        # 检查毕业条件
        required_ok = self.player.required_credits >= self.course_system.required_credits_needed
        electiveI_ok = self.player.electiveI_credits >= self.course_system.electiveI_credits_needed
        electiveII_ok = self.player.electiveII_credits >= self.course_system.electiveII_credits_needed
        total_ok = self.player.credits >= self.course_system.total_credits_needed

        if not total_ok:
            return "学分不足! 未能毕业..."
        if not required_ok:
            return "必修课学分不足! 未能毕业..."
        if not electiveI_ok:
            return "专业选修I学分不足! 未能毕业..."
        if not electiveII_ok:
            return "专业选修II学分不足! 未能毕业..."
        
        message = ""
        if self.player.wisdom >= 85:
            if self.player.charm >=80:
                message += "成就卓越，获得名企offer！"
            else:
                message += "学术成就卓越! 获得保研深造机会"
        elif self.player.wisdom < 60:
            message += "你大学四年几乎没学到什么东西"

        if self.player.relationship == "恋爱中":
            message += "校园爱情圆满! "
        else:
            message += "你还是一个人"

        if self.player.charm >=80:
            message += "你是一个社交达人，成为了校友联络人。"
        elif self.player.charm < 60:
            message += "你很内向，一直喜欢自己一个人"

        if self.player.health >=80:
            message += "你保持了一个健康的体魄。"
        elif self.player.health < 60:
            message += "你不良的生活方式使你体质变差了。"
  
        message += "恭喜! 顺利毕业开启人生新篇章"
        
        return message
    
    def get_ending(self):
        # 确定结局类型
        outcome_type = self.determine_outcome_type()
        
        # 准备玩家数据
        player_data = {
            'year': 4,
            'health': self.player.health,
            'charm': self.player.charm,
            'wisdom': self.player.wisdom,
            'pressure': self.player.pressure,
            'credits': self.player.credits,
            'relationship': self.player.relationship,
            'outcome_type': outcome_type,
            'name': "BNU-AIer" 
        }
        
        try:
            # 尝试生成个性化结局
            return self.llm_generator.generate_ending(player_data)
        except Exception as e:
            print(f"LLM生成失败: {e}")
            # 使用备用结局
            return self.get_fallback_ending(outcome_type)
    
    def get_fallback_ending(self, outcome_type):
        """备用的结局文本"""
        ending = f"""
《银杏见证的成长》

四年前的金秋，你拖着行李箱走过铺满金色落叶的银杏大道，开启了北师大之旅。
在图书馆熬夜写论文的灯光下，在邱季端体育馆挥洒的汗水中，在学五食堂和朋友们谈笑风生的日子里，你度过了充实的四年大学生活。

{outcome_type}

毕业典礼那天，你站在熟悉的银杏树下回望这四年：
- 健康: {self.player.health}/100
- 魅力: {self.player.charm}/100
- 智慧: {self.player.wisdom}/100
- 压力: {self.player.pressure}/100
- 总学分: {self.player.credits}/155

人生如银杏，历经四季方能凝聚金黄；而你的故事，才刚刚开始下一篇章。
"""
        return ending
    
    def plot_attributes(self):
        if not self.attribute_history or len(self.attribute_history) < 2:
            return None

        plt.style.use('seaborn-v0_8-dark')
        fig, ax = plt.subplots(figsize=(8, 5))
        # 准备数据
        d = {1:'一',2:'二',3:'三',4:'四'}
        years = [f"大{d[entry['year']]}" for entry in self.attribute_history]
        health = [e['health'] for e in self.attribute_history]
        charm = [e['charm'] for e in self.attribute_history]
        wisdom = [e['wisdom'] for e in self.attribute_history]
        pressure = [e['pressure'] for e in self.attribute_history]
        credits = [e['credits'] for e in self.attribute_history]
        
        # 绘制属性曲线
        ax.plot(years, health, linewidth=2, markersize=0, label='健康',color = "#99DDF4")
        ax.plot(years, charm, linewidth=2, markersize=0, label='魅力',color = "#99F4D6")
        ax.plot(years, wisdom, linewidth=2, markersize=0, label='智慧',color = "#C899F4")
        ax.plot(years, pressure, linewidth=2, markersize=0, label='压力',color = "#F499A8")

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
        
        # 添加学分柱状图
        ax2 = ax.twinx()
        credit_bars = ax2.bar(years, credits, alpha=0.25, color="#F7ED92", label='累计学分',width= 0.6)
        ax2.set_ylabel('学分', fontsize=12)

        # 设置学分轴范围，避免柱状图过高
        max_credits = max(credits) if credits else 0
        ax2.set_ylim(0, max(155, max_credits * 1.3))  # 留出空间给标签

        # 在柱状图上添加数值标签
        for bar in credit_bars:
            height = bar.get_height()
            ax2.text(
                bar.get_x() + bar.get_width() / 2., 
                height + 3, 
                f'{int(height)}',
                ha='center', 
                va='bottom',
                fontsize=9,
                zorder = 3
            )
        
        # 设置标题和标签
        ax.set_xlabel('学年', fontsize=12)
        ax.set_ylabel('属性值', fontsize=12)
        ax.set_ylim(0, 110)  # 确保属性值有足够空间
        ax.set_title('大学四年成长轨迹', fontsize=14, fontweight='bold')
        
        # 添加图例
        lines, labels = ax.get_legend_handles_labels()
        bars, bar_labels = ax2.get_legend_handles_labels()
        ax.legend(lines + bars, labels + bar_labels, loc='upper left', fontsize=6)
        
        # 设置网格和布局
        ax.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        return fig
