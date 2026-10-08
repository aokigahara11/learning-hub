import React, { useState } from 'react'
import { TodoItem, type ITask } from './TodoItem'

export type FilterType = 'all' | 'active' | 'completed'

export const TodoList: React.FC = () => {
  // 1. Состояние списка всех задач
  const [tasks, setTasks] = useState<ITask[]>([])

  // 2. Состояние инпута формы
  const [inputText, setInputText] = useState('')

  // 3. Состояние выбранного фильтра
  const [filter, setFilter] = useState<FilterType>('all')

  // Добавление новой задачи
  const handleAddTask = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    if (!inputText.trim()) return

    const newTask: ITask = {
      id: Date.now(),
      title: inputText.trim(),
      isCompleted: false,
    }

    setTasks([...tasks, newTask])
    setInputText('')
  }

  // Переключение статуса задачи (isCompleted: true / false)
  const handleToggleTask = (id: number) => {
    setTasks(
      tasks.map((task) =>
        task.id === id ? { ...task, isCompleted: !task.isCompleted } : task
      )
    )
  }

  // Удаление задачи из массива по ID
  const handleDeleteTask = (id: number) => {
    setTasks(tasks.filter((task) => task.id !== id))
  }

  // Фильтрация задач
  const filteredTasks = tasks.filter((task) => {
    if (filter === 'active') return !task.isCompleted
    if (filter === 'completed') return task.isCompleted
    return true // 'all'
  })

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
          className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          Все
        </button>
        <button
          type="button"
          className={`filter-btn ${filter === 'active' ? 'active' : ''}`}
          onClick={() => setFilter('active')}
        >
          Активные
        </button>
        <button
          type="button"
          className={`filter-btn ${filter === 'completed' ? 'active' : ''}`}
          onClick={() => setFilter('completed')}
        >
          Завершенные
        </button>
      </div>

      <ul className="todo-list">
        {filteredTasks.length === 0 ? (
          <li className="todo-empty">Задач нет</li>
        ) : (
          filteredTasks.map((task) => (
            <TodoItem
              key={task.id}
              task={task}
              onToggle={handleToggleTask}
              onDelete={handleDeleteTask}
            />
          ))
        )}
      </ul>
    </div>
  )
}