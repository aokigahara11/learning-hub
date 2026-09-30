import tkinter as tk
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Создать программу на Python, которая реализует следующие элементы:  
# 1. Создать окно с кнопками запуска программы и выхода из нее.  
# 2. Нарисовать круг, линию и квадрат, используя класс Canvas библиотеки Tkinter.  
# 3. Реализовать анимацию движения круга по экрану окна.  
# 4. Написать код для рисования случайных геометрических фигур (линии, квадраты,
# треугольники) заданного цвета и размера.  
# 5. Добавить интерактивность — возможность изменения размеров фигуры при
# нажатии кнопки мыши / с помощью слайдера.
# 6. Построить несколько графиков математических функций с использованием библиотеки
# Matplotlib.

class ButtonsAction:
    @staticmethod
    def canvas():
        window = tk.Toplevel()
        window.title("Canvas")

        canvas = tk.Canvas(window, bg="white", width=450, height=350)
        canvas.grid(row=0, column=0, padx=25, pady=20)

        canvas.create_line(30, 50, 200, 50, fill="blue", width=3)
        canvas.create_oval(220, 100, 340, 220, fill="red", width=2)
        canvas.create_rectangle(30, 100, 150, 220, fill="#FF9800", width=2)

    @staticmethod
    def animation():
        window = tk.Toplevel()
        window.title("Анимация")
        
        canvas_width = 450
        canvas_height = 350

        canvas = tk.Canvas(window, bg="white", width=canvas_width, height=canvas_height)
        canvas.grid(row=0, column=0, padx=25, pady=20)

        ball = canvas.create_oval(30, 30, 70, 70, fill="red", outline="black")

        dx = 3
        dy = 2

        def move_ball():
            nonlocal dx, dy

            if not window.winfo_exists():
                return

            canvas.move(ball, dx, dy)

            x1, y1, x2, y2 = canvas.coords(ball)

            if x1 <= 0 or x2 >= canvas_width:
                dx = -dx

            if y1 <= 0 or y2 >= canvas_height:
                dy = -dy

            window.after(16, move_ball)

        move_ball()

    @staticmethod
    def random_figure():
        window = tk.Toplevel()
        window.title("Случайная фигура")

        selected_size = {"value": 60}
        selected_color = {"value": "blue"}

        canvas = tk.Canvas(window, bg="white", width=450, height=350)
        canvas.grid(row=0, column=0, columnspan=7, padx=15, pady=10)

        def draw_shape():
            canvas.delete("all")

            size = selected_size["value"]
            color = selected_color["value"]

            x = random.randint(50, 450 - size - 50)
            y = random.randint(50, 350 - size - 50)

            figures = ["line", "square", "triangle"]
            shape = random.choice(figures)

            match shape:
                case "line":
                    canvas.create_line(x, y, x + size, y + size, fill=color, width=4)

                case "square":
                    canvas.create_rectangle(x, y, x + size, y + size, fill=color, outline="black")

                case "triangle":
                    canvas.create_polygon(
                        x + size / 2, y,
                        x, y + size,
                        x + size, y + size,
                        fill=color, outline="black"
                    )

        def set_size(s):
            selected_size["value"] = s
            draw_shape()

        def set_color(c):
            selected_color["value"] = c
            draw_shape()

        tk.Label(window, text="Размер:", font=("Arial", 9, "bold")).grid(row=1, column=0, padx=5, pady=5)

        btnSmall = tk.Button(window, text="Маленький", command=lambda: set_size(30), bg="#e0e0e0")
        btnSmall.grid(row=1, column=1, padx=2, pady=5)

        btnAverage = tk.Button(window, text="Средний", command=lambda: set_size(60), bg="#e0e0e0")
        btnAverage.grid(row=1, column=2, padx=2, pady=5)

        btnBig = tk.Button(window, text="Большой", command=lambda: set_size(100), bg="#e0e0e0")
        btnBig.grid(row=1, column=3, padx=2, pady=5)

        tk.Label(window, text="Цвет:", font=("Arial", 9, "bold")).grid(row=2, column=0, padx=5, pady=5)

        btnRed = tk.Button(window, text="Красный", command=lambda: set_color("red"), bg="#f8d7da", width=8)
        btnRed.grid(row=2, column=1, padx=2, pady=5)

        btnBlue = tk.Button(window, text="Синий", command=lambda: set_color("blue"), fg="white", bg="#0d6efd", width=8)
        btnBlue.grid(row=2, column=2, padx=2, pady=5)

        btnBlack = tk.Button(window, text="Черный", command=lambda: set_color("black"), fg="white", bg="#212529", width=8)
        btnBlack.grid(row=2, column=3, padx=2, pady=5)

        btnGenerate = tk.Button(window, text="🎲 Сгенерировать снова", command=draw_shape, bg="#198754", fg="white", font=("Arial", 9, "bold"))
        btnGenerate.grid(row=3, column=0, columnspan=4, pady=10)

        draw_shape()

    @staticmethod
    def shape_scaler():
        window = tk.Toplevel()
        window.title("Изменение размера фигуры")

        canvas_width = 450
        canvas_height = 300
        canvas = tk.Canvas(window, bg="white", width=canvas_width, height=canvas_height)
        canvas.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        current_shape = {"type": "circle"}

        def update_shape(val=None):
            canvas.delete("all")
            
            size = slider.get()
            center_x = canvas_width // 2
            center_y = canvas_height // 2

            shape_type = current_shape["type"]

            match shape_type:
                case "circle":
                    canvas.create_oval(
                        center_x - size // 2, center_y - size // 2,
                        center_x + size // 2, center_y + size // 2,
                        fill="#9C27B0", outline="black", width=2
                    )
                case "square":
                    canvas.create_rectangle(
                        center_x - size // 2, center_y - size // 2,
                        center_x + size // 2, center_y + size // 2,
                        fill="#00BCD4", outline="black", width=2
                    )
                case "triangle":
                    h = size * (3**0.5) / 2 
                    top = (center_x, center_y - h / 2)
                    left = (center_x - size / 2, center_y + h / 2)
                    right = (center_x + size / 2, center_y + h / 2)
                    
                    canvas.create_polygon(
                        top[0], top[1], left[0], left[1], right[0], right[1],
                        fill="#FF9800", outline="black", width=2
                    )

        def set_shape_type(shape_name):
            current_shape["type"] = shape_name
            update_shape()

        frame_buttons = tk.Frame(window)
        frame_buttons.grid(row=1, column=0, columnspan=2, pady=5)

        tk.Button(frame_buttons, text="Круг", command=lambda: set_shape_type("circle"), width=10).pack(side="left", padx=5)
        tk.Button(frame_buttons, text="Квадрат", command=lambda: set_shape_type("square"), width=10).pack(side="left", padx=5)
        tk.Button(frame_buttons, text="Треугольник", command=lambda: set_shape_type("triangle"), width=10).pack(side="left", padx=5)

        tk.Label(window, text="Размер фигуры:", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=10, pady=10)

        slider = tk.Scale(
            window, 
            from_=20, 
            to=220, 
            orient="horizontal", 
            command=update_shape,  # Вызывает функцию при движении ползунка
            length=250
        )
        slider.set(80)
        slider.grid(row=2, column=1, padx=10, pady=10)

        update_shape()

    @staticmethod
    def schedule():
        window = tk.Toplevel()
        window.title("Графики математических функций")
        window.geometry("600x550")

        x = np.linspace(-10, 10, 400)

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        
        show_sin = tk.BooleanVar(value=True)
        show_cos = tk.BooleanVar(value=True)
        show_sq = tk.BooleanVar(value=False)

        def update_plot():
            ax.clear()

            ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
            ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
            ax.grid(True, linestyle=':', alpha=0.6)
            ax.set_title("Математические функции", fontsize=12, fontweight='bold')
            ax.set_xlabel("X")
            ax.set_ylabel("Y")

            if show_sin.get():
                ax.plot(x, np.sin(x), label="y = sin(x)", color="blue", linewidth=2)

            if show_cos.get():
                ax.plot(x, np.cos(x), label="y = cos(x)", color="red", linewidth=2)

            if show_sq.get():
                ax.set_ylim(-2, 10) 
                ax.plot(x, x**2, label="y = x²", color="green", linewidth=2)

            if show_sin.get() or show_cos.get() or show_sq.get():
                ax.legend(loc="upper right")

            canvas_matplotlib.draw()

        canvas_matplotlib = FigureCanvasTkAgg(fig, master=window)
        canvas_widget = canvas_matplotlib.get_tk_widget()
        canvas_widget.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        chk_sin = tk.Checkbutton(
            window, 
            text="y = sin(x)", 
            variable=show_sin, 
            command=update_plot, 
            font=("Arial", 10, "bold"),
            fg="blue"
        )
        chk_sin.grid(row=1, column=0, padx=10, pady=10)

        chk_cos = tk.Checkbutton(
            window, 
            text="y = cos(x)", 
            variable=show_cos, 
            command=update_plot, 
            font=("Arial", 10, "bold"),
            fg="red"
        )
        chk_cos.grid(row=1, column=1, padx=10, pady=10)

        chk_sq = tk.Checkbutton(
            window, 
            text="y = x²", 
            variable=show_sq, 
            command=update_plot, 
            font=("Arial", 10, "bold"),
            fg="green"
        )
        chk_sq.grid(row=1, column=2, padx=10, pady=10)

        update_plot()


def MainMenu():
    root = tk.Tk() 
    root.title("Главное меню")
    root.geometry("400x400")
    
    root.columnconfigure(0, weight=1)

    title_label = tk.Label(
        root, 
        text="Лабораторная работа Tkinter", 
        font=("Arial", 14, "bold")
    )
    title_label.grid(row=0, column=0, pady=(15, 10))

    btnCanvas = tk.Button(
        root,
        text="1. Фигуры Canvas (Круг, Линия, Квадрат)",
        command=ButtonsAction.canvas,
        bg="#626463",
        fg="white", 
        font=("Arial", 10, "bold"),
        width=35
    )
    btnCanvas.grid(row=1, column=0, pady=4, padx=20)

    btnAnimation = tk.Button(
        root,
        text="2. Анимация круга",
        command=ButtonsAction.animation,
        bg="#626463",
        fg="white", 
        font=("Arial", 10, "bold"),
        width=35
    )
    btnAnimation.grid(row=2, column=0, pady=4, padx=20)

    btnRandom = tk.Button(
        root,
        text="3. Рандомные и интерактивные фигуры",
        command=ButtonsAction.random_figure,
        bg="#626463",
        fg="white", 
        font=("Arial", 10, "bold"),
        width=35
    )
    btnRandom.grid(row=3, column=0, pady=4, padx=20)

    btnScaler = tk.Button(
        root,
        text="4. Фигура с редактированием размера",
        command=ButtonsAction.shape_scaler,
        bg="#626463",
        fg="white", 
        font=("Arial", 10, "bold"),
        width=35
    )
    btnScaler.grid(row=4, column=0, pady=4, padx=20)

    btnMathSchedule = tk.Button(
        root,
        text="5. Графики функций (Matplotlib)",
        command=ButtonsAction.schedule,
        bg="#626463",
        fg="white", 
        font=("Arial", 10, "bold"),
        width=35
    )
    btnMathSchedule.grid(row=5, column=0, pady=4, padx=20)

    btnExit = tk.Button(
        root,
        text="Выход",
        command=root.destroy,
        bg="#d9534f",
        fg="white", 
        font=("Arial", 10, "bold"),
        width=35
    )
    btnExit.grid(row=6, column=0, pady=(15, 10), padx=20)

    root.mainloop()


if __name__ == "__main__":
    MainMenu()