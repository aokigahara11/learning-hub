// Задание 1: Моделирование API Telegram-бота (Interfaces & Unions)
// Создай систему типов для сообщений Telegram-бота:

// Опиши базовый интерфейс BaseMessage с полями: messageId: number, chatId: number, timestamp: number.

// Опиши тип TextMessage, который наследует BaseMessage и добавляет text: string.
    
// Опиши тип PhotoMessage, который наследует BaseMessage и добавляет photoUrl: string и caption?: string.

// Создай Union-тип BotMessage = TextMessage | PhotoMessage.

// Напиши функцию formatMessage(msg: BotMessage): string, которая принимает BotMessage, 
// использует сужение типов (Type Guard) через проверку наличия полей (in или свойство-дискриминант) 
// и возвращает красиво форматированную строку.

interface BaseMessage {
    messageID: number;
    chatID: number;
    timestamp: number;
}

type TextMessage = BaseMessage & { text: string };

// type позволяет складывать нексколько типов в один через &
type PhotoMessage = BaseMessage & { photoUrl: string; caption?: string };
// type умеет выбирать один тип через |
type BotMessage = TextMessage | PhotoMessage;

function formatMessage(msg: BotMessage): string {
    if ('text' in msg) {
        return `Текстовое сообщение [ID: ${msg.messageID}, Чат: ${msg.chatID}, Время: ${new Date(msg.timestamp).toLocaleString()}]: ${msg.text}`;
    } else if ('photoUrl' in msg) {
        const caption = msg.caption ? ` Caption: ${msg.caption}` : '';
        return `Фото сообщение [ID: ${msg.messageID}, Чат: ${msg.chatID}, Время: ${new Date(msg.timestamp).toLocaleString()}]: URL: ${msg.photoUrl}${caption}`;
    }
    return 'Неизвестный тип сообщения';
}