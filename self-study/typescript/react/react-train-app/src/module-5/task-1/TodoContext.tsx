import React, { createContext, useContext, useReducer, useEffect } from 'react'
import { todoReducer, type TodoState } from './TodoReducer'
import { useLocalStorage } from '../../module-3/task-1/useLocalStorage'
import { type ITask } from '../../module-1/task-1/TodoItem'
import { type FilterType } from '../../module-1/task-1/TodoList'

// Описываем, что будет доступно через контекст
interface TodoContextType {
    state: TodoState
    filteredTasks: ITask[]
    addTask: (title: string) => void
    toggleTask: (id: number) => void
    deleteTask: (id: number) => void
    setFilter: (filter: FilterType) => void
}

const TodoContext = createContext<TodoContextType | null>(null)

export const TodoProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    // Используем наш кастомный хук для персистентности задач
    const [savedTasks, setSavedTasks] = useLocalStorage<ITask[]>('todo_tasks', [])

    // Инициализируем useReducer
    const [state, dispatch] = useReducer(todoReducer, {
        tasks: savedTasks,
        filter: 'all',
    })

    // Синхронизируем изменения стейта задач с localStorage
    useEffect(() => {
        setSavedTasks(state.tasks)
    }, [state.tasks, setSavedTasks])

    // Вспомогательные функции-обработчики
    const addTask = (title: string) => {
        dispatch({ type: 'ADD_TASK', payload: title })
    }

    const toggleTask = (id: number) => {
        dispatch({ type: 'TOGGLE_TASK', payload: id })
    }

    const deleteTask = (id: number) => {
        dispatch({ type: 'DELETE_TASK', payload: id })
    }

    const setFilter = (filter: FilterType) => {
        dispatch({ type: 'SET_FILTER', payload: filter })
    }

    // Вычисляем отфильтрованные задачи
    const filteredTasks = state.tasks.filter((task) => {
        if (state.filter === 'active') {
            return !task.isCompleted
        }
        if (state.filter === 'completed') {
            return task.isCompleted
        }
        return true
    })

    return (
        <TodoContext.Provider
            value={{
                state,
                filteredTasks,
                addTask,
                toggleTask,
                deleteTask,
                setFilter,
            }}
        >
            {children}
        </TodoContext.Provider>
    )
}

// Кастомный хук для удобного использования контекста в компонентах
export const useTodo = () => {
    const context = useContext(TodoContext)
    if (context === null) {
        throw new Error('useTodo должен использоваться внутри TodoProvider')
    }
    return context
}