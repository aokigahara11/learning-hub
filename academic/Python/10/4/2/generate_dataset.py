import os
import json
import random

class Hunter: 
    def __init__(self, pos_x, pos_y, energy): 
        """ 
        Конструктор объекта Hunter. 
         
        Параметры: 
        pos_x, pos_y - начальные координаты охотника 
        energy - запас энергии охотника 
        """ 
        self.pos_x = pos_x 
        self.pos_y = pos_y 
        self.energy = energy 
     
    def move_towards_prey(self, prey_pos): 
        """ 
        Метод перемещения охотника к добыче. 
         
        Параметр: 
        prey_pos - позиция добычи (координаты) 
        """ 
        dx = prey_pos[0] - self.pos_x 
        dy = prey_pos[1] - self.pos_y 
         
        if abs(dx) > abs(dy): 
            step_x = int(dx / abs(dx))
            step_y = 0 
        else: 
            step_x = 0 
            step_y = int(dy / abs(dy)) 
             
        new_pos = (self.pos_x + step_x, self.pos_y + step_y) 
        return new_pos 
     
    def rest_and_recover_energy(self): 
        """Метод восстановления энергии""" 
        self.energy += 10 
        print("Охотник восстанавливает силы.") 
     
    def is_exhausted(self): 
        """Проверка усталости охотника""" 
        return self.energy <= 0 
     
    def update_position(self, new_pos): 
        """Обновление координат охотника""" 
        self.pos_x, self.pos_y = new_pos 
        self.energy -= 1
     
    def hunt(self, prey_pos): 
        """ 
        Основная логика записью данных для обучения нейросети.
        Возвращает список собранных данных.
        """ 
        episode_history = []
        
        while True: 
            distance_to_prey = ((prey_pos[0] - self.pos_x) ** 2 + 
                                (prey_pos[1] - self.pos_y) ** 2) ** 0.5 
             
            if distance_to_prey < 5: 
                print("Охотник настиг добычу!") 
                break 
                 
            current_state = {
                "features": [
                    self.pos_x,
                    self.pos_y,
                    prey_pos[0],
                    prey_pos[1],
                    self.energy,
                    prey_pos[0] - self.pos_x,  # dx
                    prey_pos[1] - self.pos_y   # dy
                ]
            }

            if self.is_exhausted(): 
                self.rest_and_recover_energy() 
                # Фиксируем действие "отдых"
                current_state["targets"] = {
                    "action_type": 0,  # 0 = rest
                    "step_x": 0,
                    "step_y": 0,
                    "next_hunter_x": self.pos_x,
                    "next_hunter_y": self.pos_y
                }
                episode_history.append(current_state)
                continue 

            next_move = self.move_towards_prey(prey_pos) 
            step_x = next_move[0] - self.pos_x
            step_y = next_move[1] - self.pos_y

            # Фиксируем действие "шаг"
            current_state["targets"] = {
                "action_type": 1,  # 1 = move
                "step_x": step_x,
                "step_y": step_y,
                "next_hunter_x": next_move[0],
                "next_hunter_y": next_move[1]
            }
            episode_history.append(current_state)

            self.update_position(next_move) 
            print(f"Охотник переместился в точку ({next_move})") 

        return episode_history

NUM_EPISODES = 100
full_dataset = []

for episode_idx in range(1, NUM_EPISODES + 1):
    pos_x_hunter = random.randint(0, 100)
    pos_y_hunter = random.randint(0, 100)
    energy = random.randint(0, 100)

    hunter = Hunter(pos_x_hunter, pos_y_hunter, energy) 

    pos_x_prey = random.randint(0, 100)
    pos_y_prey = random.randint(0, 100)
    prey_pos = (pos_x_prey, pos_y_prey)

    print(f"\n--- Эпизод №{episode_idx} ---")
    print(f"Охотник: ({pos_x_hunter}, {pos_y_hunter}), Энергия: {energy}, Жертва: ({pos_x_prey}, {pos_y_prey})")

    history = hunter.hunt(prey_pos)
    full_dataset.extend(history)

script_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_dir, "dataset.json")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(full_dataset, f, ensure_ascii=False, indent=2)

print(f"\n[УСПЕХ] Датасет из {len(full_dataset)} записей успешно сохранен по адресу: {output_file}")