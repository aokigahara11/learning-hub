// Задание 1: Универсальный HTTP-клиент для REST 
// APIНапиши класс HttpClient:Constructor: принимает baseUrl: string 

// Метод get<T>(endpoint: string): Promise<T>:Выполняет fetch(${this.baseUrl}${endpoint}).Проверяет response.ok. 
// Если false, выбрасывает ошибку new Error(...).Возвращает распарсенный JSON ответа как тип T.

// Метод post<T, R>(endpoint: string, body: T): Promise<R>:
// Выполняет fetch с опциями: method: "POST", заголовок 'Content-Type': 'application/json' и body: JSON.stringify(body).

// Проверяет response.ok. Если false, выбрасывает ошибку.Возвращает распарсенный JSON ответа как тип R.

class HttpClient {
    private baseUrl: string;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
    }

    // метод get<T> выполняет GET-запрос к указанному endpoint и возвращает данные типа T
    public async get<T>(endpoint: string): Promise<T> {
        const response = await fetch(`${this.baseUrl}${endpoint}`);

        if (!response.ok) {
            throw new Error(`Ошибка при GET-запросе: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        return data as T;
    }

    // метод post<T, R> выполняет POST-запрос к указанному endpoint и возвращает данные типа R
    public async post<T, R>(endpoint: string, body: T): Promise<R> {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        }); 

        if (!response.ok) {
            throw new Error(`Ошибка при POST-запросе: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        return data as R;
    }
}
