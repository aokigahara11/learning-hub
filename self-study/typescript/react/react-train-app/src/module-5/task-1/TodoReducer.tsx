import type { ITask, TodoActions, TodoState } from '../../types/todo'

export function todoReducer(state: TodoState, action: TodoActions) {
    if (action.type === 'ADD_TASK') {
        const newTask: ITask = {
            id: Date.now(),
            title: action.payload,
            isCompleted: false,
        }
        
        return {
            ...state,
            tasks: [...state.tasks, newTask],
        }
    }

    if (action.type === 'TOGGLE_TASK') {
        const updatedTasks = state.tasks.map((task) => {
            if (task.id === action.payload) {
                return {
                    ...task,
                    isCompleted: !task.isCompleted,
                }
            } else {
                return task
            }
        })
        return {
            ...state,
            tasks: updatedTasks,
        }
    }

    if (action.type === 'DELETE_TASK') {
        const filteredTasks = state.tasks.filter((task) => task.id !== action.payload)
        return {
            ...state,
            tasks: filteredTasks,
        }
    }

    if (action.type === 'SET_FILTER') {
        return {
            ...state,
            filter: action.payload,
        }
    }

    return state
}