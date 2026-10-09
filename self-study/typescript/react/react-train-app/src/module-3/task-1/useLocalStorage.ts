import { useState, useEffect } from 'react'

/* 1. Создать файл src/module-3/task-3/useLocalStorage.ts:

Написать универсальный дженерик-хук useLocalStorage<T>(key: string, initialValue: T).

Для считывания из localStorage при первом рендере использовать ленивую инициализацию useState(() => { ... }).

Добавить обработку ошибок через try/catch при работе с JSON.parse и localStorage.

Автоматически обновлять localStorage при изменении значений через useEffect.

Написать явные управляющие конструкции if/else (без тернарных операторов).

2. Обновить компонент TodoList.tsx:

Заменить локальный useState задач на useLocalStorage<ITask[]>('todo_tasks', []).

Добавить ссылку на инпут через useRef<HTMLInputElement>(null).

Устанавливать фокус на инпут при завершении первичной загрузки и сразу после добавления новой задачи. */

/**
 * @param key Ключ в localStorage
 * @param initialValue Значение по умолчанию
 */

export function useLocalStorage<T>(key: string, initialValue: T) {
    // Инициализация состояния
    const [storedValue, setStoredValue] = useState<T>(() => {
        try {
            // Получаем информацию из локальной памяти
            const item = window.localStorage.getItem(key)

            if (item !== null) {
                return JSON.parse(item)
            } else {
                return initialValue
            }
        } catch (error) {
            console.error(`Ошибка считывания ключа "${key}" из localStorage:`, error)
            return initialValue
        }
    })

    useEffect(() => {
        try {
            window.localStorage.setItem(key, JSON.stringify(storedValue))
        } catch (error) {
            console.error(`Ошибка записи ключа "${key}" в localStorage:`, error)
        }
    }, [key, storedValue])

    return [storedValue, setStoredValue] as const
}