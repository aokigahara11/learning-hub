// Задание 2: Связывание State Store и MainButton Telegram
// Напиши класс TelegramMainButtonController:

// Тип интерфейса состояния:

// interface IFormState {
//    isSubmitReady: boolean;
//    submitText: string;
// }
// Конструктор: Принимает store: Store<IFormState> (твой класс Store из Модуля 3).

// В конструкторе подписывается на изменения store через store.subscribe(state => this.handleStateChange(state)).

// Метод handleStateChange(state: IFormState): void:

// Проверяет, доступен ли Telegram WebApp (window.Telegram?.WebApp).

// Если state.isSubmitReady === true:

// Устанавливает текст native-кнопки Telegram: window.Telegram.WebApp.MainButton.text = state.submitText.

// Показывает кнопку: window.Telegram.WebApp.MainButton.show().

// Если state.isSubmitReady === false:

// Скрывает кнопку: window.Telegram.WebApp.MainButton.hide().

declare global {
    interface Window {
        Telegram?: {
            WebApp: {
                ready: () => void;
                expand: () => void;
                close: () => void;
                initDataUnsafe: {
                    user?: {
                        id: number;
                        first_name: string;
                        username?: string;
                    };
                };
                MainButton: {
                    text: string;
                    isVisible: boolean;
                    show: () => void;
                    hide: () => void;
                    onClick: (callback: () => void) => void;
                };
            };
        };
    }
}

interface IFormState {
    isSubmitReady: boolean;
    submitText: string;
}

export class Store<T extends object> {
    private state: T;
    private listeners: Array<(state: T) => void> = [];

    constructor(initialState: T) {
        this.state = initialState;
    }

    getState(): Readonly<T> {
        return this.state;
    }

    subscribe(listener: (state: T) => void): () => void {
        this.listeners.push(listener);
        return () => this.unsubscribe(listener);
    }

    unsubscribe(listener: (state: T) => void): void {
        this.listeners = this.listeners.filter(l => l !== listener);
    }

    update(patch: Partial<T>): void {
        this.state = { ...this.state, ...patch };
        this.notify();
    }

    private notify(): void {
        for (const listener of this.listeners) { // оповещаем всех подписчиков через цикл for...of, чтобы избежать проблем с изменением массива во время итерации
            listener(this.state); // вызываем каждого подписчика с новым состоянием
        }
    }

}

class TelegramMainButtonController {
    constructor(store: Store<IFormState>) {
        // Подписываемся на Store: каждый раз при обновлении состояния, вызовется наш метод handleStateChange с новым state
        store.subscribe(state => this.handleStateChange(state));
    }

    public handleStateChange(state: IFormState): void {
        const webApp = window.Telegram?.WebApp;
        if (!webApp) return;

        // Если форма готова к отправке
        if (state.isSubmitReady) {
            webApp.MainButton.text = state.submitText;
            webApp.MainButton.show();
        } else {
            // Если форма не готова
            webApp.MainButton.hide();
        }
    }
}