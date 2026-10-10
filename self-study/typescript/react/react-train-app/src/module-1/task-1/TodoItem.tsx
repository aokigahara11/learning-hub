import React from 'react'
import type { ITask } from '../../types/todo'


// Props — это механизм передачи данных от родительского компонента к дочернему в React.
// Props передаем как условные аргументы функции для его исполнения.
export interface TodoItemProps {
    task: ITask
    onToggle: (id: number) => void
    onDelete: (id: number) => void
}

// Оборачиваем весь компонент в React.memo снаружи
export const TodoItem: React.FC<TodoItemProps> = React.memo(({ task, onToggle, onDelete }) => {
    let itemClassName = 'todo-item'
    if (task.isCompleted) {
        itemClassName = 'todo-item completed'
    }

    return (
        <li className={itemClassName}>
            {/* Клик по тексту переключает статус */}
            <span className="todo-item-text" onClick={() => onToggle(task.id)}>
                {/* Вызываем переданную функцию через onToggle */}
                {task.title}
            </span>

            {/* Клик удаляет задание */}
            <button className="todo-delete-btn" onClick={() => onDelete(task.id)}>
                {/* Вызываем переданную функцию через onDelete */}
                ✕
            </button>
        </li>
    )
})