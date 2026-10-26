/* 

Напиши классический FizzBuzz для чисел от 1 до 30 включительно:

Если число делится на 3 и на 5, выведи "FizzBuzz".

Если только на 3 — "Fizz".

Если только на 5 — "Buzz".

Иначе — само число.

Используй конструкцию for с диапазоном (1..=30) и ветвление if/else (или попробуй match).

*/

fn main() {
    for i in 1..=30 {
        if i % 3 == 0 && i % 5 == 0 {
            println!("FizzBuzz");
        } else if i % 3 == 0 {
            println!("Fizz");
        } else if i % 5 == 0 {
            println!("Buzz");
        } else {
            println!("{}", i);
        }
    }
}