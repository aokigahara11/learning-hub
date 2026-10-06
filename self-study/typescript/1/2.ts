// Создай дженерик-интерфейс ApiSuccessResponse<T>, где payload имеет тип T, а поле success строго равно true.

// Создай интерфейс ApiErrorResponse, где error: string, а success строго равно false.

// Создай тип ApiResponse<T> = ApiSuccessResponse<T> | ApiErrorResponse.

// Напиши функцию handleResponse<T>(response: ApiResponse<T>): T, которая:

// Если success === true, возвращает payload.

// Если success === false, выбрасывает ошибку throw new Error(response.error).

// T - это дженерик-параметр, который позволяет функции handleResponse быть 
// универсальной и работать с любым типом данных, переданным в ApiSuccessResponse.
interface ApiSuccessResponse<T> {
    readonly success: true;
    payload: T;
}

interface ApiErrorResponse {
    readonly success: false;
    error: string;
}

type ApiResponse<T> = ApiSuccessResponse<T> | ApiErrorResponse;

function handleResponse<T>(response: ApiResponse<T>): T {
    if (response.success) {
        return response.payload;
    } else {
        throw new Error(response.error);
    }
}
