import json
import os
import random


def generate_synthetic_data(
    num_samples: int = 2000,
) -> tuple[list[list[float]], list[float]]:
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


def generate_and_save() -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "dataset.json")

    features, targets = generate_synthetic_data(num_samples=2500)
    dataset = [
        {
            "clear_time_sec": feature[0],
            "spells_cast": int(feature[1]),
            "mistakes": int(feature[2]),
            "target_hp": round(target, 1),
        }
        for feature, target in zip(features, targets)
    ]

    with open(json_path, "w", encoding="utf-8") as dataset_file:
        json.dump(dataset, dataset_file, indent=4, ensure_ascii=False)

    print(f"Датасет сохранен в '{json_path}'.")


if __name__ == "__main__":
    generate_and_save()
