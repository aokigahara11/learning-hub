// Задание 1: Безопасный Telegram SDK Wrapper
// Напиши класс TelegramSDK:

// Приватное поле: private webApp = window.Telegram?.WebApp;

// Метод isAvailable(): boolean:

// Возвращает true, если приложение запущено внутри Telegram (т.е. this.webApp не undefined), и false, если открыто в обычном браузере.

// Метод init(): void:

// Если isAvailable() равен true, вызывает this.webApp?.ready() и this.webApp?.expand().

// Метод getUser(): TelegramUser | null:

// Создай интерфейс TelegramUser с полями id: number, first_name: string, username?: string.

// Возвращает объект пользователя из this.webApp?.initDataUnsafe.user или null, если данных нет / открыто вне Telegram.

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

interface TelegramUser {
    id: number;
    first_name: string;
    username?: string;
}

export class TelegramSDK {
    private webApp = window.Telegram?.WebApp;

    public isAvailable(): boolean {
        return this.webApp !== undefined;
    }

    public init(): void {
        if (this.isAvailable()) {
            this.webApp?.ready();
            this.webApp?.expand();
        }
    }

    public getUser(): TelegramUser | null {
        return this.webApp?.initDataUnsafe.user ?? null;
    }
}