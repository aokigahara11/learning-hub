import React, { useState, useEffect, useRef, useMemo, useCallback } from 'react'
import { TodoItem, type ITask } from './TodoItem'
import { useLocalStorage } from '../../module-3/task-1/useLocalStorage'

export type FilterType = 'all' | 'active' | 'completed'

export const TodoList: React.FC = () => {
    const [tasks, setTasks] = useLocalStorage<ITask[]>('todo_tasks', [])
    const [inputText, setInputText] = useState('')
    const [filter, setFilter] = useState<FilterType>('all')

    const inputRef = useRef<HTMLInputElement>(null)

    useEffect(() => {
        if (inputRef.current !== null) {
            inputRef.current.focus()
        }
    }, [])

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

        if (inputRef.current !== null) {
            inputRef.current.focus()
        }
    }

    // Оптимизируем обработчики с помощью useCallback и функционального обновления состояния
    const handleToggleTask = useCallback((id: number) => {
        setTasks((prevTasks) => {
            return prevTasks.map((task) => {
                if (task.id === id) {
                    return {
                        ...task,
                        isCompleted: !task.isCompleted,
                    }
                } else {
                    return task
                }
            })
        })
    }, [setTasks])

    const handleDeleteTask = useCallback((id: number) => {
        setTasks((prevTasks) => {
            return prevTasks.filter((task) => task.id !== id)
        })
    }, [setTasks])

    // Мемоизация фильтрации задач через useMemo
    const filteredTasks = useMemo(() => {
        return tasks.filter((task) => {
            if (filter === 'active') {
                return !task.isCompleted
            }
            if (filter === 'completed') {
                return task.isCompleted
            }
            return true
        })
    }, [tasks, filter])

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

            <ul className="todo-list">
                {listContent}
            </ul>
        </div>
    )
}