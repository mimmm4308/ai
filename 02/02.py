import random
import matplotlib.pyplot as plt

# 定義城市座標
citys = [
    (0, 3), (0, 0),
    (0, 2), (0, 1),
    (1, 0), (1, 3),
    (2, 0), (2, 3),
    (3, 0), (3, 3),
    (3, 1), (3, 2)
]

# 計算兩個城市之間的距離
def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

# 計算路徑長度
def pathLength(p):
    dist = 0
    for i in range(len(p)):
        city1 = citys[p[i]]
        city2 = citys[p[(i + 1) % len(p)]]
        dist += distance(city1, city2)
    return dist

# 初始隨機路徑
num_cities = len(citys)
initial_path = random.sample(range(num_cities), num_cities)
print("初始隨機路徑:", initial_path)
print("初始路徑長度:", pathLength(initial_path))

# 爬山演算法求解TSP
def hillClimbingTSP(num_iter):
    current_path = initial_path[:]
    current_length = pathLength(current_path)
    
    for _ in range(num_iter):
        # 隨機選擇兩個位置進行交換
        idx1, idx2 = random.sample(range(num_cities), 2)
        new_path = current_path[:]
        new_path[idx1], new_path[idx2] = new_path[idx2], new_path[idx1]
        
        new_length = pathLength(new_path)
        
        # 如果新路徑更短，接受它作為新的當前路徑
        if new_length < current_length:
            current_path = new_path
            current_length = new_length
    
    return current_path, current_length

# 執行爬山演算法，設定迭代次數
num_iterations = 10000
best_path, shortest_length = hillClimbingTSP(num_iterations)

print(f"最短路徑: {best_path}")
print(f"最短路徑長度: {shortest_length}")

# 繪製初始路徑和最佳路徑圖表
def plotPaths(initial_path, best_path, city_coords):
    # 將城市坐標分離成x和y座標列表
    x_initial = [city_coords[i][0] for i in initial_path]
    y_initial = [city_coords[i][1] for i in initial_path]
    x_best = [city_coords[i][0] for i in best_path]
    y_best = [city_coords[i][1] for i in best_path]
    
    # 添加起始城市到路徑的末尾以形成一個迴圈
    x_initial.append(x_initial[0])
    y_initial.append(y_initial[0])
    x_best.append(x_best[0])
    y_best.append(y_best[0])
    
    # 繪製城市和路徑
    plt.figure(figsize=(12, 6))
    
    # 繪製初始路徑
    plt.subplot(1, 2, 1)
    plt.plot(x_initial, y_initial, marker='o', markerfacecolor='blue', markersize=10, linestyle='-')
    plt.title('Original Path')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    for i, (xi, yi) in enumerate(city_coords):
        plt.text(xi, yi, str(i), fontsize=12, ha='center', va='bottom')
    plt.grid(True)
    
    # 繪製最佳路徑
    plt.subplot(1, 2, 2)
    plt.plot(x_best, y_best, marker='o', markerfacecolor='red', markersize=10, linestyle='-')
    plt.title('Best Path')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    for i, (xi, yi) in enumerate(city_coords):
        plt.text(xi, yi, str(i), fontsize=12, ha='center', va='bottom')
    plt.grid(True)
    
    # 調整布局
    plt.tight_layout()
    plt.show()

# 繪製初始路徑和最佳路徑的圖表
plotPaths(initial_path, best_path, citys)
