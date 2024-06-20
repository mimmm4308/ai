import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

# 載入 MNIST 資料集
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 正規化圖像資料
x_train, x_test = x_train / 255.0, x_test / 255.0

# 將目標變數轉為 one-hot 編碼
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# 建立神經網路模型
model = Sequential([
    Flatten(input_shape=(28, 28)),  # 將 28x28 的圖像展平成 784 的向量
    Dense(128, activation='relu'),  # 第一個隱藏層，128 個神經元，ReLU 激活函數
    Dense(128, activation='relu'),  # 第二個隱藏層，128 個神經元，ReLU 激活函數
    Dense(10, activation='softmax') # 輸出層，10 個神經元，使用 softmax 激活函數
])

# 編譯模型
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# 訓練模型
history = model.fit(x_train, y_train, epochs=10, batch_size=32, validation_data=(x_test, y_test))

# 評估模型
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'Test accuracy: {test_acc * 100:.2f}%')

# 1. 繪製損失函數和準確率曲線
plt.figure(figsize=(12, 10))

# 損失函數曲線
plt.subplot(2, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and Validation Loss')
plt.legend()

# 準確率曲線
plt.subplot(2, 2, 2)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Training and Validation Accuracy')
plt.legend()

# 2. 繪製混淆矩陣
# 預測測試集
y_pred = model.predict(x_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = np.argmax(y_test, axis=1)

# 計算混淆矩陣
conf_matrix = confusion_matrix(y_true, y_pred_classes)

# 繪製混淆矩陣
plt.subplot(2, 2, 3)
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')

# 3. 錯誤分析
# 找出預測錯誤的圖像
incorrect_indices = np.where(y_pred_classes != y_true)[0]
print(f'Number of incorrect predictions: {len(incorrect_indices)}')

# 隨機挑選一些錯誤的圖像進行顯示
plt.subplot(2, 2, 4)
for i, incorrect in enumerate(np.random.choice(incorrect_indices, size=10, replace=False)):
    plt.imshow(x_test[incorrect], cmap='gray')
    plt.title(f'True: {y_true[incorrect]} | Predicted: {y_pred_classes[incorrect]}')
    plt.axis('off')
    if i == 0:
        plt.colorbar()

plt.tight_layout()
plt.show()
