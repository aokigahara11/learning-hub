// Задание 2: Полноценный Drag & Drop движок (DndEngine)
// Напиши класс DndEngine, который сделает любой HTML-элемент плавно перетаскиваемым:
// Конструктор: Принимает element: HTMLElement.

// Приватное состояние:
// isDragging: boolean = false
// startX: number = 0, startY: number = 0 (точка первого касания/клика)
// currentX: number = 0, currentY: number = 0 (накопленное смещение элемента)

// Обработчики событий (навешиваются в конструкторе):

// pointerdown:
// Рассчитывает стартовые координаты относительно уже имеющегося смещения: startX = event.clientX - currentX, 
// startY = event.clientY - currentY.

// Устанавливает isDragging = true.
// Вызывает this.element.setPointerCapture(event.pointerId).

// pointermove:
// Если !isDragging, мгновенно выходить из метода (return).
// Рассчитывает текущее смещение: currentX = event.clientX - startX, currentY = event.clientY - startY.
// Применяет GPU-ускоренную трансформацию: this.element.style.transform = \translate3d(${this.currentX}px, ${this.currentY}px, 0)``.

// pointerup и pointercancel:
// Сбрасывает isDragging = false.
// Освобождает указатель через this.element.releasePointerCapture(event.pointerId).

class DndEngine {
    private isDragging: boolean = false;
    private startX: number = 0;
    private startY: number = 0;
    private currentX: number = 0;
    private currentY: number = 0;

    constructor(private element: HTMLElement) {
        // Навешиваем слушатели событий через addEventListener
        this.element.addEventListener("pointerdown", this.onPointerDown);
        this.element.addEventListener("pointermove", this.onPointerMove);
        this.element.addEventListener("pointerup", this.onPointerUp);
        this.element.addEventListener("pointercancel", this.onPointerUp);
    }

    // Стрелочные функции автоматически привязывают контекст `this` к классу
    private onPointerDown = (event: PointerEvent): void => {
        this.startX = event.clientX - this.currentX;
        this.startY = event.clientY - this.currentY;
        this.isDragging = true;
        this.element.setPointerCapture(event.pointerId);
    };

    private onPointerMove = (event: PointerEvent): void => {
        if (!this.isDragging) return;
        this.currentX = event.clientX - this.startX;
        this.currentY = event.clientY - this.startY;
        this.element.style.transform = `translate3d(${this.currentX}px, ${this.currentY}px, 0)`;
    };

    private onPointerUp = (event: PointerEvent): void => {
        if (!this.isDragging) return;
        this.isDragging = false;
        this.element.releasePointerCapture(event.pointerId);
    };
}