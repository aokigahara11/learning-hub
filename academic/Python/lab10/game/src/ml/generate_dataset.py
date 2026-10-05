# game/src/ml/generate_dataset.py
import json
import os
import random
import torch
import torch.nn as nn
import torch.optim as optim

class HPRegressionModel(nn.Module):
    def __init__(self, input_dim: int = 3):
        super(HPRegressionModel, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)

def generate_synthetic_data(num_samples: int = 2000) -> tuple[list[list[float]], list[float]]:
    rng = random.Random(42)
    features = []
    targets = []

    for _ in range(num_samples):
        clear_time = round(rng.uniform(3.0, 25.0), 2)
        spells_cast = rng.randint(2, 12)
        mistakes = rng.randint(0, 5)

        target_hp = (
            2300.0
            + (14.0 - clear_time) * 20.0
            + (spells_cast - 7) * 20.0
            - (mistakes - 2.5) * 80.0
            + rng.uniform(-75.0, 75.0)
        )

        features.append([clear_time, float(spells_cast), float(mistakes)])
        targets.append(target_hp)

    return features, targets

def train_and_save():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "dataset.json")
    model_path = os.path.join(current_dir, "hp_model.pt")

    features, targets = generate_synthetic_data(num_samples=2500)

    dataset = []
    for f, t in zip(features, targets):
        dataset.append({
            "clear_time_sec": f[0],
            "spells_cast": int(f[1]),
            "mistakes": int(f[2]),
            "target_hp": round(t, 1)
        })

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

    torch.manual_seed(42)
    x_tensor = torch.tensor(features, dtype=torch.float32)
    y_tensor = torch.tensor(targets, dtype=torch.float32).unsqueeze(1)
    indices = torch.randperm(len(x_tensor))
    train_size = int(len(indices) * 0.7)
    validation_size = int(len(indices) * 0.15)
    train_indices = indices[:train_size]
    validation_indices = indices[train_size:train_size + validation_size]
    test_indices = indices[train_size + validation_size:]

    x_min = x_tensor[train_indices].min(dim=0, keepdim=True)[0]
    x_max = x_tensor[train_indices].max(dim=0, keepdim=True)[0]
    x_norm = (x_tensor - x_min) / (x_max - x_min + 1e-8)
    y_min = y_tensor[train_indices].min()
    y_max = y_tensor[train_indices].max()
    y_norm = (y_tensor - y_min) / (y_max - y_min + 1e-8)

    model = HPRegressionModel(input_dim=3)
    criterion = nn.MSELoss()
    optimizer = optim.AdamW(model.parameters(), lr=0.003)
    best_validation_rmse = float("inf")
    best_state = None

    model.train()
    for epoch in range(1, 501):
        optimizer.zero_grad()
        predictions = model(x_norm[train_indices])
        loss = criterion(predictions, y_norm[train_indices])
        loss.backward()
        optimizer.step()

        model.eval()
        with torch.no_grad():
            validation_predictions = model(x_norm[validation_indices])
            validation_rmse = (
                criterion(validation_predictions, y_norm[validation_indices]).sqrt()
                * (y_max - y_min)
            ).item()
        if validation_rmse < best_validation_rmse:
            best_validation_rmse = validation_rmse
            best_state = {key: value.clone() for key, value in model.state_dict().items()}
        model.train()

        if epoch % 100 == 0:
            train_rmse = loss.sqrt().item() * (y_max - y_min).item()
            print(f"Epoch {epoch}/500 | Train RMSE: {train_rmse:.2f} HP | Validation RMSE: {validation_rmse:.2f} HP")

    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        test_predictions = model(x_norm[test_indices])
        test_rmse = (
            criterion(test_predictions, y_norm[test_indices]).sqrt() * (y_max - y_min)
        ).item()

    checkpoint = {
        "model_state": model.state_dict(),
        "x_min": x_min,
        "x_max": x_max,
        "y_min": y_min,
        "y_max": y_max,
    }
    
    torch.save(checkpoint, model_path)
    print(
        f"\nМодель сохранена в '{model_path}'. "
        f"Validation RMSE: {best_validation_rmse:.2f} HP | "
        f"Test RMSE: {test_rmse:.2f} HP"
    )


if __name__ == "__main__":
    train_and_save()