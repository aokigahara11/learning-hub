import React, { useState, useEffect, useRef } from 'react'
import { TodoItem, type ITask } from './TodoItem'
import { useLocalStorage } from '../../module-3/task-1/useLocalStorage'

export type FilterType = 'all' | 'active' | 'completed'

export const TodoList: React.FC = () => {
    // 1. Заменяем обычный useState на кастомный хук useLocalStorage.
    // Интерфейс идентичен, но данные теперь автоматически синхронизируются с localStorage.
    const [tasks, setTasks] = useLocalStorage<ITask[]>('todo_tasks', [])

    const [inputText, setInputText] = useState('')
    const [filter, setFilter] = useState<FilterType>('all')

    // 2. Создаем ссылку на DOM-элемент инпута
    const inputRef = useRef<HTMLInputElement>(null)

    // 3. Автофокус на инпут при монтировании компонента (первой загрузке страницы)
    useEffect(() => {
        if (inputRef.current !== null) {
            inputRef.current.focus()
        }
    }, [])

    // Добавление новой задачи
    const handleAddTask = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()

        // Проверка на пустоту
        if (!inputText.trim()) {
            return
        }

        // Создание новой задачи
        const newTask: ITask = {
            id: Date.now(),
            title: inputText.trim(),
            isCompleted: false,
        }

        setTasks([...tasks, newTask])
        setInputText('')

        // 4. Возвращаем фокус на поле ввода после добавления задачи
        if (inputRef.current !== null) {
            inputRef.current.focus()
        }
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

    // Удаление задачи из массива по ID
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

    // Определение классов для фильтра
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

    // Отрисовка пустого списка или задач через if/else
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
                    ref={inputRef} // Привязываем ссылку к инпуту
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