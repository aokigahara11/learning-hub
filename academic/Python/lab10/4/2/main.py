import os
import random
import torch
import torch.nn as nn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pth")

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


class AIHunter:
    """Охотник, использующий предсказания уже загруженной .pth модели."""
    def __init__(self, pos_x, pos_y, energy, ai_model):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.energy = energy
        self.ai_model = ai_model

    def move_towards_prey(self, prey_pos):
        dx = prey_pos[0] - self.pos_x
        dy = prey_pos[1] - self.pos_y
        
        if abs(dx) > abs(dy):
            step_x = int(dx / abs(dx)) if dx != 0 else 0
            step_y = 0
        else:
            step_x = 0
            step_y = int(dy / abs(dy)) if dy != 0 else 0
            
        return (self.pos_x + step_x, self.pos_y + step_y)

    def rest_and_recover_energy(self):
        self.energy += 10
        print("Охотник восстанавливает силы (+10 энергии).")

    def update_position(self, new_pos):
        self.pos_x, self.pos_y = new_pos
        self.energy -= 1

    def hunt_with_ai(self, prey_pos):
        steps = 0
        while True:
            steps += 1
            distance = ((prey_pos[0] - self.pos_x) ** 2 + (prey_pos[1] - self.pos_y) ** 2) ** 0.5
            
            if distance < 5:
                print(f"\nОхотник настиг добычу за {steps} шагов!")
                break

            dx = prey_pos[0] - self.pos_x
            dy = prey_pos[1] - self.pos_y
            state_features = torch.tensor([[self.pos_x, self.pos_y, prey_pos[0], prey_pos[1], self.energy, dx, dy]], dtype=torch.float32)

            with torch.no_grad():
                logits = self.ai_model(state_features)
                predicted_action = torch.argmax(logits, dim=1).item()

            if predicted_action == 0:
                self.rest_and_recover_energy()
            else:
                next_move = self.move_towards_prey(prey_pos)
                self.update_position(next_move)
                print(f"Охотник переместился в {next_move}. Энергия: {self.energy}")

            if steps > 200:
                print("\nСимуляция остановлена.")
                break


def main():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Файл {MODEL_PATH} не найден! Сначала выполните train_model.py.")

    model = HunterBrainPyTorch(input_dim=7, num_classes=2)

    model.load_state_dict(torch.load(MODEL_PATH, weights_only=True))
    model.eval()

    print("--- Запуск игровой симуляции с загруженной моделью PyTorch ---")
    
    start_hunter_x = random.randint(0, 100)
    start_hunter_y = random.randint(0, 100)
    start_energy = random.randint(0, 50)

    prey_x = random.randint(0, 100)
    prey_y = random.randint(0, 100)
    prey_position = (prey_x, prey_y)

    print(f"Старт: Охотник({start_hunter_x}, {start_hunter_y}), Энергия: {start_energy}. Добыча: {prey_position}\n")

    ai_hunter = AIHunter(start_hunter_x, start_hunter_y, start_energy, model)
    ai_hunter.hunt_with_ai(prey_position)


if __name__ == "__main__":
    main()