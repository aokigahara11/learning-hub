// Задание 3: ООП-компонент интерактивного блока (Pointer Events & Transform)
// Напиши класс DraggableCard, который будет управлять позиционированием элемента на странице.

// Требования:

// Класс принимает в конструктор element: HTMLElement.

// Хранит приватное состояние x: number и y: number (текущее смещение).

// Имеет приватный метод clamp(value: number, min: number, max: number): number, который ограничивает значение в заданном диапазоне 
// (аналог std::clamp в C++).

// Имеет публичный метод move(dx: number, dy: number): void, который:

// Прибавляет dx и dy к текущим x и y.

// Ограничивает координаты x и y в диапазоне от -300 до 300 с помощью clamp.

// Обновляет позицию элемента на странице через CSS transform: element.style.transform = \translate(${this.x}px, ${this.y}px)``.

// Имеет метод reset(): void, который сбрасывает x = 0, y = 0 и обновляет transform.

class DraggableCard {
    private x: number;
    private y: number;

    constructor(private element: HTMLElement) {
        this.x = 0;
        this.y = 0;
    }

    private clamp(value: number, min: number = -300, max: number = 300): number {
        return Math.max(min, Math.min(max, value));
    }

    public move(dx: number, dy: number): void {
        this.x = this.clamp(this.x + dx);
        this.y = this.clamp(this.y + dy);
        this.updateTransform();
    }

    private updateTransform(): void {
        this.element.style.transform = `translate(${this.x}px, ${this.y}px)`;
    }

    public reset(): void {
        this.x = 0;
        this.y = 0;
        this.updateTransform();
    }
}