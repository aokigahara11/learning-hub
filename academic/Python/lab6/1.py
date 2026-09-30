# Пусть дана строка, состоящая из слов, пробелов и знаков препинания. 
# На основании этой строки создайте новую (и выведите ее на консоль):
# Содержащую только слова больше 5 символов. Разделитель слов в строке — пробел.

import string
text = input("Введите строку: ")

for char in string.punctuation:
    text = text.replace(char, "")

words = text.split()

long_words = []

for word in words:
    if len(word) > 5:
        long_words.append(word)

new_string = " ".join(long_words)

print("Новая строка:", new_string)