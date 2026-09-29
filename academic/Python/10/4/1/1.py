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
            step_x = int(dx / abs(dx))  # Перемещаемся горизонтально 
            step_y = 0 
        else: 
            step_x = 0 
            step_y = int(dy / abs(dy))  # Перемещаемся вертикально 
             
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
        self.energy -= 1  # Каждый ход тратится энергия 
     
    def hunt(self, prey_pos): 
        """Основная логика охоты""" 
        while True: 
            distance_to_prey = ((prey_pos[0] - self.pos_x) ** 2 + 
                                (prey_pos[1] - self.pos_y) ** 2) ** 0.5 
             
            if distance_to_prey < 5: 
                print("Охотник настиг добычу!") 
                break 
                 
            elif self.is_exhausted(): 
                self.rest_and_recover_energy() 
                continue 
            next_move = self.move_towards_prey(prey_pos) 
            self.update_position(next_move) 
            print(f"Охотник переместился в точку ({next_move})") 

# Начальные настройки
pos_x_hunter = random.randint(0, 100)
pos_y_hunter = random.randint(0, 100)
energy = random.randint(0, 100)

hunter = Hunter(pos_x_hunter, pos_y_hunter, energy) 

pos_x_prey = random.randint(0, 100)
pos_y_prey = random.randint(0, 100)

prey_pos = (pos_x_prey, pos_y_prey)

print(f"""Тест номер №10
Изначальная позиция охотника: (({pos_x_hunter}, {pos_y_hunter})).
Энегрия охотника: {energy}
Изначальная позиция жертвы: (({pos_x_prey}, {pos_y_prey}))
""")

# Начинаем охоту 
hunter.hunt(prey_pos)