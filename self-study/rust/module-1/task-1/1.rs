/*

Объяви глобальную константу MAX_CONNECTIONS: u32 со значением 100.

Создай мутабельную переменную active_users типа i32 со значением 15. Увеличь ее на 5.

Продемонстрируй шэдоуинг (shadowing): создай переменную name со строковым значением "aoki", 
а затем переобъяви её же (let name = name.len();), 
превратив в число (длину строки). Выведи всё это в консоль через println!.

*/

const MAX_CONNECTIONS: u32 = 100;

fn main() {
    let mut active_users: i32 = 15;
    active_users += 5;

    let name = "aoki";
    let name = name.len();

    println!("Макс. подключений: {}", MAX_CONNECTIONS);
    println!("Активные пользователи: {}", active_users);
    println!("Длина имени: {}", name);
}