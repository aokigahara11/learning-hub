/*

Напиши две чистые функции:calculate_bmi(weight: f64, height: f64) -> f64 — 
вычисляет индекс массы тела по формуле $\text{вес} / \text{рост}^2$.

Обрати внимание на синтаксис возврата без 
ключевого слова return и точки с запятой в конце выражения.is_even(n: i32) -> bool — проверяет, 
четное ли число, возвращая булево значение.

*/

fn calculate_bmi(weight: f64, height: f64) -> f64 {
    weight / (height * height)
}

fn is_even(n: i32) -> bool {
    n % 2 == 0
}

fn main() {
    let my_weight: f64 = 52.7;
    let my_height: f64 = 1.76;

    println!("Мой индекс массы тела: {}", calculate_bmi(my_weight, my_height));

    let number: i32 = 2;

    println!("Число четное? {}", is_even(number));
}