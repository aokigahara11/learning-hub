import React from 'react'

// Интерфейс структуры задачи
export interface ITask {
  id: number
  title: string
  isCompleted: boolean
}

// Props 
interface TodoItemProps {
  task: ITask
  onToggle: (id: number) => void
  onDelete: (id: number) => void
}

export const TodoItem: React.FC<TodoItemProps> = ({ task, onToggle, onDelete }) => {
  return (
    <li className={`todo-item ${task.isCompleted ? 'completed' : ''}`}>
      {/* Клик по тексту переключает статус задачи через родительскую функцию */}
      <span className="todo-item-text" onClick={() => onToggle(task.id)}>
        {task.title}
      </span>

      {/* Клик по кнопке удаляет задачу по id */}
      <button className="todo-delete-btn" onClick={() => onDelete(task.id)}>
        ✕
      </button>
    </li>
  )
}