from scipy.optimize import linprog
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# 定義目標函數的係數向量 c
c = [-3, -2, -5]

# 定義不等式限制的係數矩陣 A 和右側常數向量 b
A = [
    [1, 1, 0],
    [2, 0, 1],
    [0, 1, 2]
]
b = [10, 9, 11]

# 定義變數的範圍
x_bounds = (0, None)
y_bounds = (0, None)
z_bounds = (0, None)

# 調用線性規劃求解器
result = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds, z_bounds], method='simplex')

# 輸出結果
print('最大化目標函數值:', -result.fun)  # 因為linprog默認求最小值，所以要取負號
print('達到最大化時的變數取值:')
print('x =', result.x[0])
print('y =', result.x[1])
print('z =', result.x[2])

# 將結果視覺化在3D空間中
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 繪製不等式限制的平面
x = np.linspace(0, 10, 100)
y = np.linspace(0, 10, 100)
X, Y = np.meshgrid(x, y)
Z1 = 10 - X - Y
Z2 = 9 - 2*X
Z3 = 11 - Y - 2*X

ax.plot_surface(X, Y, Z1, alpha=0.5)
ax.plot_surface(X, Y, Z2, alpha=0.5)
ax.plot_surface(X, Y, Z3, alpha=0.5)

# 標記最大化目標函數值的點
ax.scatter(result.x[0], result.x[1], result.x[2], color='red', s=100, label='Max Point')

# 添加最大化值及其座標的標籤
max_value = -result.fun
max_coords = result.x
ax.text(max_coords[0], max_coords[1], max_coords[2], f'Max Value = {max_value:.2f}\n(x, y, z) = ({max_coords[0]:.2f}, {max_coords[1]:.2f}, {max_coords[2]:.2f})',
        color='black', fontsize=12, bbox=dict(facecolor='white', alpha=0.7))

# 設置坐標軸標籤和標題
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('Visualization of Linear Programming Problem')

# 添加圖例
ax.legend()

# 顯示圖形
plt.show()
