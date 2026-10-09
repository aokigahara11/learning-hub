import React, { useState, useEffect } from 'react'
import { TodoItem } from '../../module-1/task-1/TodoItem'

/* Обработай 3 состояния: данные (tasks), загрузка (isLoading), ошибка (error).

Используй конструкцию try / catch / finally.

Форматирование данных с сервера:

Сервер JSONPlaceholder возвращает объекты с полем completed (true/false).

Преобразуй их в наш интерфейс ITask, где поле называется isCompleted.

Обработка состояний загрузки и ошибок:

Пока идет запрос, отобрази текст или плашку: "Загрузка задач с сервера...".

Если произошла ошибка сети, выведи сообщение об ошибке.

Форматирование и стиль:

Сохраняй отступы в 4 пробела.

Используй if / else блоки вместо тернарных операторов.

Напиши комментарии к каждому шагу асинхронной логики. */

const BASE_URL = 'https://jsonplaceholder.typicode.com/todos?_limit=5'

export type FilterType = 'all' | 'active' | 'completed'

export interface ITask {
    id: number
    title: string
    isCompleted: boolean
}

export const TodoList: React.FC = () => {
    // State
    const [tasks, setTasks] = useState<ITask[]>([])
    const [inputText, setInputText] = useState('')
    const [filter, setFilter] = useState<FilterType>('all')
    const [isLoading, setIsLoading] = useState<boolean>(true)
    const [error, setError] = useState<string | null>(null)

    // useEffect - это хук, который выполняет побочные действия (side effects) после того, 
    // как React завершил отрисовку (рендеринг) компонента на экране.
    
    // useEffect для загрузки компонентов сайтов
    useEffect(() => {
        const fetchTasks = async () => {
            try {
                const response = await fetch(BASE_URL)

                if (!response.ok) {
                    throw new Error('Не удалось загрузить список задач')
                }

                const data = await response.json()

                const formattedTasks: ITask[] = data.map((item: any) => {
                    return {
                        id: item.id,
                        title: item.title,
                        isCompleted: item.completed,
                    }
                })

                setTasks(formattedTasks)
            } catch (err) {
                if (err instanceof Error) {
                    setError(err.message)
                } else {
                    setError('Произошла неизвестная ошибка')
                }
            } finally {
                setIsLoading(false)
            }
        }

        fetchTasks()
    }, []) // Пустой массив зависимостей, так как запуск 1 раз

    // Добавление новой задачи
    const handleAddTask = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()

        if (!inputText.trim()) {
            return
        }

        const newTask: ITask = {
            id: Date.now(),
            title: inputText.trim(),
            isCompleted: false,
        }

        setTasks([...tasks, newTask])
        setInputText('')
    }

    // Переключение статуса задачи
    const handleToggleTask = (id: number) => {
        const updatedTasks = tasks.map((task) => {
            if (task.id === id) {
                return {
                    ...task,
                    isCompleted: !task.isCompleted,
                }
            } else {
                return task
            }
        })

        setTasks(updatedTasks)
    }

    // Удаление задачи
    const handleDeleteTask = (id: number) => {
        setTasks(tasks.filter((task) => task.id !== id))
    }

    // Фильтрация задач
    const filteredTasks = tasks.filter((task) => {
        if (filter === 'active') {
            return !task.isCompleted
        }
        if (filter === 'completed') {
            return task.isCompleted
        }
        return true
    })

    // Отрисовка состояний загрузки
    if (isLoading) {
        return <div className="todo-container">Загрузка задач с сервера...</div>
    }

    if (error) {
        return <div className="todo-container error">Ошибка: {error}</div>
    }

    // Отрисовка фильтров
    let allFilterClass = 'filter-btn'
    if (filter === 'all') {
        allFilterClass = 'filter-btn active'
    }

    let activeFilterClass = 'filter-btn'
    if (filter === 'active') {
        activeFilterClass = 'filter-btn active'
    }

    let completedFilterClass = 'filter-btn'
    if (filter === 'completed') {
        completedFilterClass = 'filter-btn active'
    }

    // Отрисовка списка
    let listContent: React.ReactNode
    if (filteredTasks.length === 0) {
        listContent = <li className="todo-empty">Задач нет</li>
    } else {
        listContent = filteredTasks.map((task) => (
            <TodoItem
                key={task.id}
                task={task}
                onToggle={handleToggleTask}
                onDelete={handleDeleteTask}
            />
        ))
    }

    return (
        <div className="todo-container">
            <h2 className="todo-title">Список задач</h2>

            <form className="todo-form" onSubmit={handleAddTask}>
                <input
                    type="text"
                    className="todo-input"
                    placeholder="Что нужно сделать?"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                />
                <button type="submit" className="todo-add-btn">
                    Добавить
                </button>
            </form>

            <div className="todo-filters">
                <button
                    type="button"
                    className={allFilterClass}
                    onClick={() => setFilter('all')}
                >
                    Все
                </button>
                <button
                    type="button"
                    className={activeFilterClass}
                    onClick={() => setFilter('active')}
                >
                    Активные
                </button>
                <button
                    type="button"
                    className={completedFilterClass}
                    onClick={() => setFilter('completed')}
                >
                    Завершенные
                </button>
            </div>

            <ul className="todo-list">
                {listContent}
            </ul>
        </div>
    )
}