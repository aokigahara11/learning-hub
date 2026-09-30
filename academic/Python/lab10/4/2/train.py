import os
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset.json")
MODEL_PATH = os.path.join(BASE_DIR, "model.pth")

class HunterDataset(Dataset):
    """Данные для загрузки сохраненной статистики из dataset.json."""
    def __init__(self, json_path):
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Файл {json_path} не найден! Сначала запустите generate_dataset.py.")
        
        with open(json_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        features_list = []
        labels_list = []

        for entry in raw_data:
            features_list.append(entry["features"])
            labels_list.append(entry["targets"]["action_type"])

        self.X = torch.tensor(features_list, dtype=torch.float32)
        self.Y = torch.tensor(labels_list, dtype=torch.long)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.Y[idx]


class HunterBrainPyTorch(nn.Module):
    """Архитектура нейронной сети охотника."""
    def __init__(self, input_dim=7, num_classes=2):
        super(HunterBrainPyTorch, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, num_classes)
        )

    def forward(self, x):
        return self.network(x)


def train():
    dataset = HunterDataset(DATASET_PATH)
    train_loader = DataLoader(dataset, batch_size=32, shuffle=True)
    print(f"Загружено примеров: {len(dataset)}")

    model = HunterBrainPyTorch(input_dim=7, num_classes=2)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.005)

    epochs = 20
    model.train()

    for epoch in range(1, epochs + 1):
        total_loss = 0.0
        for batch_X, batch_Y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_Y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        if epoch % 5 == 0 or epoch == 1:
            avg_loss = total_loss / len(train_loader)
            print(f"Эпоха [{epoch}/{epochs}] - Loss: {avg_loss:.4f}")

    torch.save(model.state_dict(), MODEL_PATH)
    print(f"\n[УСПЕХ] Модель успешно обучена и сохранена в: {MODEL_PATH}")

if __name__ == "__main__":
    train()