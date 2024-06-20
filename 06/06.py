import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

# 假設已經定義了名為 `macrograd` 的模型
# 並且它適用於 MNIST 數據集

# 定義模型架構
class MacroGradModel(nn.Module):
    def __init__(self):
        super(MacroGradModel, self).__init__()
        # 在這裡定義模型層
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 10)  # 假設 MNIST 有 10 個輸出類別

    def forward(self, x):
        x = x.view(-1, 784)  # 展平輸入張量
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 初始化模型
macrograd = MacroGradModel()

# 加入 CrossEntropyLoss 層
criterion = nn.CrossEntropyLoss()

# 載入 MNIST 數據集
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

train_dataset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_dataset = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# 定義優化器（例如 SGD）
optimizer = torch.optim.SGD(macrograd.parameters(), lr=0.01)

# 訓練循環
def train_model(model, criterion, optimizer, train_loader, num_epochs=5):
    model.train()
    for epoch in range(num_epochs):
        for batch_idx, (images, labels) in enumerate(train_loader):
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            if (batch_idx+1) % 100 == 0:
                print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'
                      .format(epoch+1, num_epochs, batch_idx+1, len(train_loader), loss.item()))

# 測試循環
def test_model(model, criterion, test_loader):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    accuracy = 100 * correct / total
    print('測試集準確率: {:.2f}%'.format(accuracy))

# 訓練模型
train_model(macrograd, criterion, optimizer, train_loader, num_epochs=5)

# 測試模型
test_model(macrograd, criterion, test_loader)
