import numpy as np

courses = [
    {'teacher': '甲', 'name': '機率', 'hours': 2},
    {'teacher': '甲', 'name': '線代', 'hours': 3},
    {'teacher': '甲', 'name': '離散', 'hours': 3},
    {'teacher': '乙', 'name': '視窗', 'hours': 3},
    {'teacher': '乙', 'name': '科學', 'hours': 3},
    {'teacher': '乙', 'name': '系統', 'hours': 3},
    {'teacher': '乙', 'name': '計概', 'hours': 3},
    {'teacher': '丙', 'name': '軟工', 'hours': 3},
    {'teacher': '丙', 'name': '行動', 'hours': 3},
    {'teacher': '丙', 'name': '網路', 'hours': 3},
    {'teacher': '丁', 'name': '媒體', 'hours': 3},
    {'teacher': '丁', 'name': '工數', 'hours': 3},
    {'teacher': '丁', 'name': '動畫', 'hours': 3},
    {'teacher': '丁', 'name': '電子', 'hours': 4},
    {'teacher': '丁', 'name': '嵌入', 'hours': 3},
    {'teacher': '戊', 'name': '網站', 'hours': 3},
    {'teacher': '戊', 'name': '網頁', 'hours': 3},
    {'teacher': '戊', 'name': '演算', 'hours': 3},
    {'teacher': '戊', 'name': '結構', 'hours': 3},
    {'teacher': '戊', 'name': '智慧', 'hours': 3}
]

teachers = ['甲', '乙', '丙', '丁', '戊']
rooms = ['A', 'B']

slots = [
    'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17',
    'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27',
    'A31', 'A32', 'A33', 'A34', 'A35', 'A36', 'A37',
    'A41', 'A42', 'A43', 'A44', 'A45', 'A46', 'A47',
    'A51', 'A52', 'A53', 'A54', 'A55', 'A56', 'A57',
    'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17',
    'B21', 'B22', 'B23', 'B24', 'B25', 'B26', 'B27',
    'B31', 'B32', 'B33', 'B34', 'B35', 'B36', 'B37',
    'B41', 'B42', 'B43', 'B44', 'B45', 'B46', 'B47',
    'B51', 'B52', 'B53', 'B54', 'B55', 'B56', 'B57',
]

# 生成隨機的課程安排，根據時間槽分配
def generate_random_schedule_with_slots(courses, teachers, rooms, slots):
    schedule = []
    used_slots = set()  # 用於記錄已使用的時間槽
    
    for course in courses:
        teacher = np.random.choice(teachers)
        room = np.random.choice(rooms)
        
        # 從未使用的時間槽中隨機選擇一個
        available_slots = list(set(slots) - used_slots)
        selected_slot = np.random.choice(available_slots)
        
        schedule.append({
            'teacher': teacher,
            'name': course['name'],
            'room': room,
            'slot': selected_slot
        })
        
        used_slots.add(selected_slot)  # 標記此時間槽為已使用
    
    return schedule

# 將課程安排寫入檔案
def write_schedule_to_file(schedule, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for course in schedule:
            f.write(f"課程: {course['name']}, 老師: {course['teacher']}, 教室: {course['room']}, 時間槽: {course['slot']}\n")

if __name__ == "__main__":
    np.random.seed(42)
    random_schedule = generate_random_schedule_with_slots(courses, teachers, rooms, slots)
    write_schedule_to_file(random_schedule, 'output01.txt')
