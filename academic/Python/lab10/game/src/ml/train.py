import json
import os

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


def train_and_save() -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "dataset.json")
    model_path = os.path.join(current_dir, "hp_model.pt")

    with open(json_path, "r", encoding="utf-8") as dataset_file:
        dataset = json.load(dataset_file)

    features = [
        [
            sample["clear_time_sec"],
            float(sample["spells_cast"]),
            float(sample["mistakes"]),
        ]
        for sample in dataset
    ]
    targets = [sample["target_hp"] for sample in dataset]

    torch.manual_seed(42)
    x_tensor = torch.tensor(features, dtype=torch.float32)
    y_tensor = torch.tensor(targets, dtype=torch.float32).unsqueeze(1)
    indices = torch.randperm(len(x_tensor))
    train_size = int(len(indices) * 0.7)
    validation_size = int(len(indices) * 0.15)
    train_indices = indices[:train_size]
    validation_indices = indices[train_size : train_size + validation_size]
    test_indices = indices[train_size + validation_size :]

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
            best_state = {
                key: value.clone() for key, value in model.state_dict().items()
            }
        model.train()

        if epoch % 100 == 0:
            train_rmse = loss.sqrt().item() * (y_max - y_min).item()
            print(
                f"Epoch {epoch}/500 | Train RMSE: {train_rmse:.2f} HP | "
                f"Validation RMSE: {validation_rmse:.2f} HP"
            )

    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        test_predictions = model(x_norm[test_indices])
        test_rmse = (
            criterion(test_predictions, y_norm[test_indices]).sqrt()
            * (y_max - y_min)
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
