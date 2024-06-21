import pandas as pd

# 讀取CSV文件
data = pd.read_csv('training_data.csv')

# 顯示DataFrame的info信息
print(data.info())
