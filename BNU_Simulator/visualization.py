import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np #

class Visualization:
    def __init__(self):
        self.history = {
            "year": [],
            "health": [],
            "charm": [],
            "wisdom": [],
            "pressure": [],
            "credits": []
        }
    
    def update_history(self, player):
        """更新历史记录"""
        self.history["year"].append(player.year)
        self.history["health"].append(player.health)
        self.history["charm"].append(player.charm)
        self.history["wisdom"].append(player.wisdom)
        self.history["pressure"].append(player.pressure)
        self.history["credits"].append(player.credits)
    
    def plot_attributes(self):
        """绘制属性变化图"""
        try:
            plt.figure(figsize=(10, 6))
            for attr in ["health", "charm", "wisdom", "pressure"]:
                plt.plot(self.history["year"], self.history[attr], label=attr)
            
            plt.xlabel('学年')
            plt.ylabel('属性值')
            plt.title('大学四年属性变化')
            plt.legend()
            plt.grid(True)
            plt.show()
        except Exception as e:
            print(f"绘图失败: {e}")
    
    def predict_outcome(self, player):
        """预测结局（使用模拟数据）"""
        try:
            # 创建模拟数据集
            data = {
                'health': np.random.randint(40, 100, 100),
                'charm': np.random.randint(30, 95, 100),
                'wisdom': np.random.randint(50, 100, 100),
                'pressure': np.random.randint(20, 90, 100),
                'credits': np.random.randint(120, 160, 100),
                'outcome': np.random.choice(['顺利毕业', '保研深造', '退学重开', '创业成功'], 100)
            }
            df = pd.DataFrame(data)
            
            # 训练模型
            X = df[['health', 'charm', 'wisdom', 'pressure', 'credits']]
            y = df['outcome']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
            
            model = RandomForestClassifier()
            model.fit(X_train, y_train)
            
            # 预测当前玩家结局
            player_data = [[
                player.health, player.charm, player.wisdom, 
                player.pressure, player.credits
            ]]
            prediction = model.predict(player_data)[0]
            probability = max(model.predict_proba(player_data)[0])
            
            return prediction, probability
        except Exception as e:
            print(f"预测失败: {e}")
            return "未知结局", 0.0
