# Твоя задача — оптимизировать TodoList.tsx и TodoItem.tsx:

## 1. Мемоизировать фильтрацию задач через useMemo:

**Обернуть расчет filteredTasks в useMemo с зависимостями [tasks, filter].**

## 2. Мемоизировать функции-обработчики через useCallback:

**Обернуть handleToggleTask и handleDeleteTask в useCallback.**

**Подсказка: Чтобы не добавлять tasks в зависимости useCallback, используй функциональное обновление состояния в setTasks((prev) => ...)!**

## 3. Обернуть TodoItem в React.memo:

**Убедиться, что при вводе текста в input карточки задач (TodoItem) не перерисовываются лишний раз.**