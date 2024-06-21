import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import ModelCheckpoint

# 加載訓練數據
data = pd.read_csv('training_data.csv')

# 提取特徵和目標
X = data.iloc[:, :-2].values  # 所有列，排除最後兩列（棋盤狀態和動作）
y = data.iloc[:, -1].values   # 最後一列是結果

# 將特徵進行標準化
scaler = StandardScaler()
X = scaler.fit_transform(X)

# 切分數據集為訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 建立神經網絡模型
model = Sequential([
    Dense(64, activation='relu', input_dim=X.shape[1]),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])

# 編譯模型
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 設置模型檢查點以保存最佳模型
checkpoint = ModelCheckpoint('connect4_model.keras', monitor='val_accuracy', save_best_only=True, mode='max', verbose=1)

# 訓練模型
history = model.fit(X_train, y_train, validation_split=0.2, epochs=20, batch_size=32, callbacks=[checkpoint])

# 評估模型
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test accuracy: {accuracy}')

# 保存模型
model.save('connect4_model_final.h5')
