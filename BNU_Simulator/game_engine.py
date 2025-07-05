from course_system import CourseSystem
from event_system import EventSystem
from attribute_system import Player
import matplotlib.pyplot as plt
import random

class GameEngine:
    STATES = ["IDLE", "COURSE_SELECTION", "EVENT_HANDLING", "YEAR_END", "GAME_OVER"]
    
    def __init__(self):
        self.player = Player()
        self.course_system = CourseSystem()
        self.event_system = EventSystem()
        self.state = "IDLE"
        self.current_event = None
        self.attribute_history = []
        
    def start_new_game(self):
        self.player.reset()
        self.state = "COURSE_SELECTION"
        self.attribute_history = []
        return "欢迎来到大学生活模拟器! 请选择本学期课程。"
    
    def select_courses(self, selected_courses):
        if not selected_courses:
            return "请至少选择一门课程!"
        
        self.player.selected_courses = selected_courses
        credits_earned = self.course_system.calculate_credits(selected_courses)
        pressure_added = self.course_system.calculate_pressure(selected_courses)
        
        self.player.credits += credits_earned
        self.player.pressure += pressure_added
        self.player.courses_taken.extend([c['id'] for c in selected_courses])
        
        self.state = "EVENT_HANDLING"
        self.current_event = self.event_system.get_random_event(self.player.year)
        self.record_attributes()
        
        return f"选课完成! 获得学分: {credits_earned}"
    
    def handle_event_choice(self, choice_idx):
        if not self.current_event or choice_idx >= len(self.current_event['choices']):
            return "无效选择!"
        
        choice = self.current_event['choices'][choice_idx]
        self.player.apply_effects(choice['effects'])
        self.record_attributes()
        
        self.state = "YEAR_END"
        return f"事件处理完成: {choice['description']}"
    
    def next_year(self):
        self.player.next_year()
        self.state = "COURSE_SELECTION" if self.player.year <= 4 else "GAME_OVER"
        
        if self.player.year > 4:
            return self.get_ending()
        return f"进入大{self.player.year}学年!"
    
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
    
    def get_ending(self):
        if self.player.credits < self.course_system.total_credits_needed:
            return "学分不足! 未能毕业..."
        
        if self.player.wisdom >= 90:
            return "学术成就卓越! 获得奖学金深造"
        
        if self.player.relationship == "恋爱中" and self.player.charm >= 80:
            return "校园爱情圆满! 与恋人共同毕业"
        
        return "恭喜! 顺利毕业开启人生新篇章"
    
    def plot_attributes(self):
        if not self.attribute_history or len(self.attribute_history) < 2:
            return None
            
        fig, ax = plt.subplots(figsize=(8, 5))
        years = [f"大{entry['year']}" for entry in self.attribute_history]
        
        # 绘制属性曲线
        ax.plot(years, [e['health'] for e in self.attribute_history], 'g-', label='健康')
        ax.plot(years, [e['charm'] for e in self.attribute_history], 'b-', label='魅力')
        ax.plot(years, [e['wisdom'] for e in self.attribute_history], 'r-', label='智慧')
        ax.plot(years, [e['pressure'] for e in self.attribute_history], 'y-', label='压力')
        
        # 添加学分柱状图
        ax2 = ax.twinx()
        credits = [e['credits'] for e in self.attribute_history]
        ax2.bar(years, credits, alpha=0.3, color='purple', label='累计学分')
        ax2.set_ylabel('学分')
        
        ax.set_xlabel('学年')
        ax.set_ylabel('属性值')
        ax.set_title('大学四年成长轨迹')
        ax.legend(loc='upper left')
        ax.grid(True)
        
        return fig