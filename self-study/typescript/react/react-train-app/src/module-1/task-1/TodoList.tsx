import React, { useState } from 'react'
import { TodoItem, type ITask } from './TodoItem'

export type FilterType = 'all' | 'active' | 'completed'

// Состояние (State) — это специальный JavaScript-объект или значение, управляемое внутри компонента, 
// которое хранит данные, меняющиеся во времени, и автоматически вызывает перерисовку (re-render) интерфейса при своём изменении.

export const TodoList: React.FC = () => {
    // Состояние списка всех задач
    // useState([]) передаётся начальное значение
    // ITask[] означает массив объектов формата ITask.
    const [tasks, setTasks] = useState<ITask[]>([])

    const [inputText, setInputText] = useState('')

    const [filter, setFilter] = useState<FilterType>('all')

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

        setTasks([...tasks, newTask]) // tasks - хранилище, setTasks - функция-сеттер c помощью которой мы обновляем этот массив.
        setInputText('') // Обнуляем ввод, после сохранения задания
    }

    // Переключение статуса задачи (isCompleted: true / false)
    const handleToggleTask = (id: number) => {
        // Используем иммутабельность — создаем абсолютно новый массив и отдаем его в setTasks.
        const updatedTasks = tasks.map((task) => {
            if (task.id === id) {
                // { ...task } — оператор spread скопировал все свойства текущей задачи (id, title, isCompleted).
                // isCompleted: !task.isCompleted — перетирает поле isCompleted на противоположное значение 
                // (!true станет false, а !false станет true).
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
        setTasks(tasks.filter((task) => task.id !== id)) // Удаление путем .filter()
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

    // Определение классов для фильтра через if/else
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