class Player:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.health = 80
        self.charm = 50
        self.wisdom = 50
        self.pressure = 30
        self.credits = 0
        self.year = 1
        self.relationship = "单身"
        self.courses_taken = []
        self.selected_courses = []
        self.required_credits = 0  # 必修课学分
        self.electiveI_credits = 0  # 专业选修I学分
        self.electiveII_credits = 0  # 专业选修II学分
        # 添加压力警告标志
        self.pressure_warning_shown = False
        
    def apply_effects(self, effects):
        for attr, value in effects.items():
            if hasattr(self, attr):
                current = getattr(self, attr)
                if attr == "relationship":
                    setattr(self, attr, value)
                else:
                    setattr(self, attr, max(0, min(100, current + value)))
    
    def check_overload(self):
        return self.pressure >= 85
    
    def next_year(self):
        self.year += 1
        self.pressure = max(30, self.pressure - 20)
        self.selected_courses = []
