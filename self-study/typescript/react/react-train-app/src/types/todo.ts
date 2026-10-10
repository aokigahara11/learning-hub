/* 
Создать единый файл общих типов (src/types/todo.ts или src/types/index.ts):

Сейчас у нас типы (ITask, FilterType, TodoState, TodoActions) 
импортируются из папок старых модулей (например, из module-1). 
Нам нужно вынести их в отдельную глобальную папку types, 
чтобы компоненты, контекст и редюсер ссылались на один чистый источник типов.

Провести рефакторинг импортов и структуры папок:

Убедиться, что пути чистые, нет дублирования кода, неиспользуемых переменных и импортов-заглушек.
*/

export interface ITask {
    id: number
    title: string
    isCompleted: boolean
}

export type FilterType = 'all' | 'active' | 'completed'

export interface TodoState {
    tasks: ITask[]
    filter: FilterType
}

export type TodoActions =
    | { type: 'ADD_TASK'; payload: string }
    | { type: 'TOGGLE_TASK'; payload: number }
    | { type: 'DELETE_TASK'; payload: number }
    | { type: 'SET_FILTER'; payload: FilterType }