// Допустим, у нас есть интерфейс настроек пользователя сайта:

// TypeScript
// interface UserSettings {
//    theme: "light" | "dark";
//    fontSize: number;
//   notificationsEnabled: boolean;
//    language: string;
// }

// Напиши функцию updateSettings, которая принимает текущий объект current: UserSettings и объект обновлений patch.

// Подбери правильный Utility Type для параметра patch, чтобы функция позволяла обновить любое количество полей (даже одно), не заставляя передавать весь объект заново.

// Функция должна возвращать новый обновленный объект UserSettings.

interface UserSettings {
    theme: "light" | "dark";
    fontSize: number;
    notificationsEnabled: boolean;
    language: string;
}

// Partial<UserSettings>) позовляет обновить любое количество полей (даже одно), не заставляя передавать весь объект заново.
function updateSettings(current: UserSettings, patch: Partial<UserSettings>): UserSettings {
    return { ...current, ...patch };
}



