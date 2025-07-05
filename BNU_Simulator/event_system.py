import json
import random
import os

class EventSystem:
    def __init__(self, filename="data/events.json"):
        self.events = self.load_events(filename)
    
    def load_events(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载事件数据失败: {e}")
            return []
    
    def get_random_event(self, year):
        # 过滤出适用于当前学年的事件
        applicable_events = [e for e in self.events if 'years' in e and year in e['years']]
        
        if not applicable_events:
            print(f"没有找到适用于学年 {year} 的事件")
            return None
            
        return random.choice(applicable_events)