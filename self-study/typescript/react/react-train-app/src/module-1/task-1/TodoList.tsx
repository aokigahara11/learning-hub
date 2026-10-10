import React, { useState, useRef, useEffect } from 'react'
import { TodoItem } from './TodoItem'
import { useTodo } from '../../module-5/task-1/TodoContext'

export type FilterType = 'all' | 'active' | 'completed'

export const TodoList: React.FC = () => {
    const { state, filteredTasks, addTask, toggleTask, deleteTask, setFilter } = useTodo()
    const [inputText, setInputText] = useState('')
    const inputRef = useRef<HTMLInputElement>(null)

    useEffect(() => {
        if (inputRef.current !== null) {
            inputRef.current.focus()
        }
    }, [])

    const handleFormSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        if (!inputText.trim()) {
            return
        }

        addTask(inputText.trim())
        setInputText('')

        if (inputRef.current !== null) {
            inputRef.current.focus()
        }
    }

    // Определение классов для фильтров
    let allFilterClass = 'filter-btn'
    if (state.filter === 'all') {
        allFilterClass = 'filter-btn active'
    }

    let activeFilterClass = 'filter-btn'
    if (state.filter === 'active') {
        activeFilterClass = 'filter-btn active'
    }

    let completedFilterClass = 'filter-btn'
    if (state.filter === 'completed') {
        completedFilterClass = 'filter-btn active'
    }

    let listContent: React.ReactNode
    if (filteredTasks.length === 0) {
        listContent = <li className="todo-empty">Задач нет</li>
    } else {
        listContent = filteredTasks.map((task) => (
            <TodoItem
                key={task.id}
                task={task}
                onToggle={toggleTask}
                onDelete={deleteTask}
            />
        ))
    }

    return (
        <div className="todo-container">
            <h2 className="todo-title">Список задач (Context API)</h2>

            <form className="todo-form" onSubmit={handleFormSubmit}>
                <input
                    ref={inputRef}
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

            <ul className="todo-list">{listContent}</ul>
        </div>
    )
}