import csv
import ast

class CourseSystem:
    def __init__(self, filename="data/courses.csv"):
        self.courses = self.load_courses(filename)
        self.total_credits_needed = 155
        print(f"成功加载 {len(self.courses)} 门课程")
    
    def load_courses(self, filename):
        courses = []
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # 确保 year_available 是列表
                    year_available = row['year_available'].strip()
                    
                    # 尝试解析为列表
                    try:
                        if year_available.startswith('[') and year_available.endswith(']'):
                            year_list = ast.literal_eval(year_available)
                        else:
                            # 尝试转换为列表
                            year_list = [int(year_available)]
                    except:
                        # 如果解析失败，创建空列表
                        year_list = []
                    
                    # 确保所有元素都是整数
                    year_list = [int(y) for y in year_list if str(y).isdigit()]
                    
                    courses.append({
                        'id': row['course_id'],
                        'name': row['name'],
                        'module': row['module'],
                        'credit': float(row['credit']),
                        'pressure': int(row['pressure']),
                        'year_available': year_list  # 确保是整数列表
                    })
            print(f"加载了 {len(courses)} 门课程")
        except Exception as e:
            print(f"课程加载错误: {e}")
            # 打印详细错误信息
            import traceback
            traceback.print_exc()
        return courses
    
    def get_available_courses(self, year, taken_courses):
        available = []
        taken_ids = set(taken_courses)
        
        print(f"当前学年: {year}, 已修课程数: {len(taken_courses)}")
        
        for course in self.courses:
            # 添加调试信息
            print(f"检查课程: {course['name']}, 可开设学年: {course['year_available']}")
            
            # 检查课程是否可开设在当前学年
            if year in course['year_available'] and course['id'] not in taken_ids:
                available.append(course)
        
        print(f"学年 {year} 可选课程: {len(available)} 门")
        return available
    
    def calculate_credits(self, selected_courses):
        return sum(c['credit'] for c in selected_courses)
    
    def calculate_pressure(self, selected_courses):
        return sum(c['pressure'] for c in selected_courses)