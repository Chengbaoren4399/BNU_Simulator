import json
import os
import random
import csv
from datetime import datetime

class GameLogic:
    def __init__(self):
        # 游戏阶段定义
        self.stages = {
            0: "刚入学", 1: "大一", 2: "大二", 3: "大三",
            4: "大四", 5: "研究生", 6: "博士生", 7: "毕业"
        }
        
        # 初始化玩家属性
        self.player = {
            'name': "北师大学子",
            'health': 80,
            'charm': 60,
            'wisdom': 70,
            'money': 2000,
            'stage': 0  # 当前阶段
        }
        
        # 加载事件数据
        self.events = self.load_events()
        self.current_event = None
        self.player_history = []
        self.event_history = []
        
        # 初始化游戏
        self.load_game()  # 尝试加载存档
        if not self.current_event:
            self.get_next_event()
        
        # 记录初始状态
        self.record_stats()
    
    def load_events(self):
        # 从JSON文件加载事件数据
        events_path = os.path.join('data', 'events.json')
        if os.path.exists(events_path):
            with open(events_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 如果文件不存在，创建示例事件
            return self.create_sample_events()
    
    def create_sample_events(self):
        # 创建示例事件数据
        events = [
            {
                "id": 1,
                "title": "开学第一课",
                "description": "作为北师大AI学院的新生，你迎来了开学第一课——人工智能导论。教授提出了一个挑战性问题。",
                "stage": 0,
                "type": "学业",
                "options": [
                    {"text": "积极举手回答", "effect": {"wisdom": 5, "charm": 3}},
                    {"text": "课后单独请教教授", "effect": {"wisdom": 8}},
                    {"text": "装作没听懂", "effect": {"health": 2}}
                ]
            },
            {
                "id": 2,
                "title": "社团招新",
                "description": "百团大战开始了！AI协会和街舞社同时向你发出了邀请。",
                "stage": 0,
                "type": "社交",
                "options": [
                    {"text": "加入AI协会", "effect": {"wisdom": 7, "charm": -2}},
                    {"text": "加入街舞社", "effect": {"charm": 8, "health": -3}},
                    {"text": "两个都参加", "effect": {"charm": 5, "wisdom": 5, "health": -5}}
                ]
            },
            {
                "id": 3,
                "title": "食堂选择",
                "description": "午餐时间到了，新乐群食堂有特价套餐，但学五食堂有你最爱的麻辣香锅。",
                "stage": 0,
                "type": "生活",
                "options": [
                    {"text": "新乐群特价套餐", "effect": {"money": 50, "health": 3}},
                    {"text": "学五麻辣香锅", "effect": {"money": -100, "health": 5, "charm": 2}},
                    {"text": "便利店随便吃点", "effect": {"money": 30, "health": -2}}
                ]
            },
            {
                "id": 4,
                "title": "图书馆偶遇",
                "description": "在图书馆自习时，一位同学向你请教Python问题，他/她看起来很有魅力。",
                "stage": 1,
                "type": "恋爱",
                "options": [
                    {"text": "耐心讲解", "effect": {"charm": 8, "wisdom": 3}},
                    {"text": "推荐参考书", "effect": {"wisdom": 5}},
                    {"text": "假装很忙", "effect": {"charm": -3}}
                ]
            }
        ]
        
        # 确保数据目录存在
        os.makedirs('data', exist_ok=True)
        
        # 保存示例事件
        with open(os.path.join('data', 'events.json'), 'w', encoding='utf-8') as f:
            json.dump(events, f, ensure_ascii=False, indent=2)
        
        return events
    
    def get_next_event(self):
        # 获取当前阶段可用的事件
        stage_events = [e for e in self.events if e['stage'] == self.player['stage']]
        
        if stage_events:
            # 随机选择一个事件
            self.current_event = random.choice(stage_events)
        else:
            # 如果没有事件，推进到下一阶段
            self.advance_stage()
            self.get_next_event()
    
    def process_choice(self, option_idx):
        # 应用选择效果
        option = self.current_event['options'][option_idx]
        for attr, value in option['effect'].items():
            self.player[attr] = max(0, min(100, self.player[attr] + value))
        
        # 记录事件历史
        self.event_history.append({
            'event_id': self.current_event['id'],
            'choice': option_idx,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # 记录玩家状态
        self.record_stats()
        
        # 获取新事件
        self.get_next_event()
    
    def advance_stage(self):
        # 推进到下一阶段
        if self.player['stage'] < 7:
            self.player['stage'] += 1
            # 阶段转换奖励
            self.player['health'] = min(100, self.player['health'] + 10)
            self.player['wisdom'] = min(100, self.player['wisdom'] + 15)
    
    def check_game_over(self):
        # 检查是否达到毕业阶段
        return self.player['stage'] == 7
    
    def get_ending(self):
        # 根据最终属性确定结局
        wisdom = self.player['wisdom']
        charm = self.player['charm']
        
        if wisdom >= 90 and charm >= 80:
            return "恭喜！你成为AI领域的杰出学者，获得国际知名企业的高薪offer！"
        elif wisdom >= 80:
            return "你以优异成绩毕业，进入顶尖研究机构继续深造。"
        elif charm >= 80:
            return "你凭借出色的社交能力，成功创业并获得了天使投资。"
        else:
            return "你顺利毕业，进入知名企业成为一名AI工程师。"
    
    def save_game(self):
        # 保存游戏状态
        save_data = {
            'player': self.player,
            'event_history': self.event_history,
            'player_history': self.player_history,
            'current_event': self.current_event
        }
        
        with open(os.path.join('data', 'save_game.json'), 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
    
    def load_game(self):
        # 加载游戏存档
        save_path = os.path.join('data', 'save_game.json')
        if os.path.exists(save_path):
            try:
                with open(save_path, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)
                    self.player = save_data['player']
                    self.event_history = save_data['event_history']
                    self.player_history = save_data['player_history']
                    self.current_event = save_data['current_event']
            except:
                # 如果加载失败，重新开始
                self.__init__()
    
    def record_stats(self):
        # 记录当前玩家状态
        self.player_history.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'health': self.player['health'],
            'charm': self.player['charm'],
            'wisdom': self.player['wisdom'],
            'money': self.player['money'],
            'stage': self.player['stage']
        })
        
        # 保存到CSV文件
        csv_path = os.path.join('data', 'stats.csv')
        headers = ['timestamp', 'health', 'charm', 'wisdom', 'money', 'stage']
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(self.player_history)S