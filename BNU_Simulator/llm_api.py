import os
import requests
import json
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class DeepSeekAPI:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_ending(self, player_data):
        prompt = self._build_prompt(player_data)
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一个擅长创作游戏结局的作家"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"DeepSeek API错误: {e}")
            return self._fallback_ending(player_data)
    
    def _build_prompt(self, player_data):
        return f"""
你是一个大学生活模拟游戏的结局生成器。请根据玩家数据创作一个200字左右的结局故事。

玩家信息:
- 学年: {player_data['year']}
- 健康: {player_data['health']}/100
- 魅力: {player_data['charm']}/100
- 智慧: {player_data['wisdom']}/100
- 压力: {player_data['pressure']}/100
- 学分: {player_data['credits']}/155
- 感情状态: {player_data['relationship']}
- 结局类型: {player_data['outcome_type']}

要求:
1. 200字左右的完整故事性结局
2. 体现玩家在大学生活中的成长轨迹
3. 融入北师大校园元素（如邱季端体育馆、学五食堂、银杏大道等）
4. 根据结局类型调整语气
5. 结尾添加一句富有哲理的总结
6. 使用中文创作
"""
    
    def _fallback_ending(self, player_data):
        """备选方案：当API不可用时使用"""
        return f"{player_data['name']}在北师大度过了{player_data['year']}年时光。最终结局: {player_data['outcome_type']}。"