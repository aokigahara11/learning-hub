import os
import webbrowser
import folium

# 0. В предложенном примере исправьте ошибку типа для записи № 4 и логическую ошибку 
# для записи № 6, чтобы они отображались в таблице.  

# Если интерактивная карта Google не отображается из-за блокировок и ограничений, 
# попробуйте воспользоваться альтернативными вариантами карт

# 1 (Корректировка весов ГИС-модели). Научный руководитель посчитал, что в ХМАО 
# пространственная близость инфраструктуры к Приполярному Уралу важнее абсолютной 
# высоты. Измените формулу расчета потенциала так, чтобы максимальный вес фактора 
# высоты (height_score) составил 30 баллов, а максимальный вес фактора близости к горам 
# (distance_score) увеличился до 70 баллов. Зафиксируйте смену позиций объектов на 
# карте. 

# 2 (Тестирование системы исключений). Добавьте в исходный словарь raw_field_data 
# две новые гипотетические точки развития туризма в Югре, содержащие умышленные 
# ошибки: 1. Объект, где широта (lat) указана в виде строки "шестьдесят один градус" 
# вместо вещественного числа. 2. Объект, где высота (elevation) полностью отсутствует 
# (None). Убедитесь, что встроенные блоки except корректно обработали новые ошибки, 
# программа не завершилась аварийно, а новые точки были отсеяны препроцессором. 

# 3 (Модификация логики ООП-инкапсуляции). Добавьте в класс GeoTourismObject новое 
# скрытое свойство __average_snow_months (среднее количество месяцев со снегом) и 
# передайте его через конструктор __init__. Измените метод calculate_slope_index так, 
# чтобы итоговый индекс уклона умножался на количество снежных месяцев. Для вершин 
# Приполярного Урала установите параметр равным 7, для Ханты-Мансийска — 5. 

# 4 (Адаптация под инфраструктурный туризм). Добавьте в блок расчетов потенциала 
# проверку условий (оператор if-else). Если тип объекта равен "ГЛК" или "База отдыха", к 
# его итоговому индексу автоматически должно прибавляться 20 бонусных баллов за счет 
# уже имеющейся инфраструктуры. Посмотрите, как изменятся цвета маркеров на карте. 

# 5 (Добавление нового географического объекта). Добавьте в базу данных 
# raw_field_data реальный географический объект ХМАО: «База отдыха Окуневские зори 
# (городской округ Урай)», координаты: lat = 60.1211, lon = 64.6310, высота рельефа = 60 
# метров, тип = "База отдыха". Убедитесь, что объект успешно прошел валидацию и 
# отобразился на веб-карте.

class GeoTourismObject:
    def __init__(self, name: str, obj_type: str, elevation: int, lat: float, lon: float, average_snow_months: int):
        self.name = name
        self.obj_type = obj_type
        self.elevation = elevation
        self.lat = lat
        self.lon = lon
        self._average_snow_months = average_snow_months # Cкрытое свойство
        self._base_accessibility = 1.0 if obj_type == 'Вершина' else 1.5

    def __repr__(self):
        return f'[{self.obj_type}] "{self.name}" ({self.elevation} м)'

    def calculate_slope_index(self):
        base_index = (self.elevation * self._base_accessibility) / 100
        return round(base_index * self._average_snow_months, 2) # Учет зимних


print('[1/4] Запуск ГИС-препроцессора. Валидация входных данных рельефа ХМАО...\n')

# Словарь данных
raw_field_data = [
    {
        'name': 'г. Народная (Приполярный Урал)', 'type': 'Вершина',
        'elevation': 1895, 'lat': 65.0347, 'lon': 60.1133, 'snow_months': 7
    },
    {
        'name': 'г. Неройка (Приполярный Урал)', 'type': 'Вершина',
        'elevation': 1645, 'lat': 64.5667, 'lon': 59.5492, 'snow_months': 7
    },
    {
        'name': 'ГЛК "Хвойный урман" (Ханты-Мансийск)', 'type': 'ГЛК',
        'elevation': 110, 'lat': 60.9922, 'lon': 69.0011, 'snow_months': 5
    },
    {
        # Задание 0: Исправлена высота 
        'name': 'ГЛК "Каменный мыс" (Сургут)', 'type': 'ГЛК',
        'elevation': 85, 'lat': 61.1689, 'lon': 73.4772, 'snow_months': 5
    },
    {
        'name': 'База отдыха "Сказка" (Нефтеюганск)', 'type': 'База отдыха',
        'elevation': 45, 'lat': 61.1214, 'lon': 72.5812, 'snow_months': 5
    },
    {
        # Задание 0: Исправлён параметр lat, заменён с None на реальное число
        'name': 'Этно-стойбище (Нягань)', 'type': 'Этно-туризм',
        'elevation': 50, 'lat': 62.1440, 'lon': 65.4122, 'snow_months': 5
    },
    {
        'name': 'Гора Люлин-Вор (Северный Сосьвинский край)', 'type': 'Вершина',
        'elevation': 310, 'lat': 61.9841, 'lon': 61.2215, 'snow_months': 7
    },
    # Задание 5: Добавлена «База отдыха Окуневские зори (городской округ Урай)»
    {
        'name': 'База отдыха "Окуневские зори" (Урай)', 'type': 'База отдыха',
        'elevation': 60, 'lat': 60.1211, 'lon': 64.6310, 'snow_months': 5
    },
    # Задание 2 (Тест 1): Умышленная ошибка типа в широте (строка вместо числа)
    {
        'name': 'Тестовый объект "Ошибка широты"', 'type': 'Вершина',
        'elevation': 500, 'lat': "шестьдесят один градус", 'lon': 65.0, 'snow_months': 6
    },
    # Задание 2 (Тест 2): Умышленная логическая ошибка — отсутствие высоты (None)
    {
        'name': 'Тестовый объект "Нет высоты"', 'type': 'Вершина',
        'elevation': None, 'lat': 62.0, 'lon': 64.0, 'snow_months': 6
    }
]

validated_database = []

for index, raw_obj in enumerate(raw_field_data, 1):
    try:
        if raw_obj['lat'] is None or raw_obj['lon'] is None:
            raise ValueError('Пропущены географические координаты GPS.')
        
        if not isinstance(raw_obj['lat'], (int, float)) or not isinstance(raw_obj['lon'], (int, float)):
            raise TypeError(f'Координаты должны быть числами, получен тип lat: {type(raw_obj["lat"]).__name__}.')
        
        if not isinstance(raw_obj['elevation'], (int, float)):
            raise TypeError(f'Высота должна быть числом, получен тип elevation: {type(raw_obj["elevation"]).__name__}.')

        clean_object = GeoTourismObject(
            name=raw_obj['name'],
            obj_type=raw_obj['type'],
            elevation=raw_obj['elevation'],
            lat=raw_obj['lat'],
            lon=raw_obj['lon'],
            average_snow_months=raw_obj['snow_months']
        )
        validated_database.append(clean_object)

    except TypeError as type_err:
        print(f'❌ Запись №{index} "{raw_obj["name"]}" ОТКЛОНЕНА. Ошибка типа: {type_err}')
    except ValueError as val_err:
        print(f'❌ Запись №{index} "{raw_obj["name"]}" ОТКЛОНЕНА. Логическая ошибка: {val_err}')

print(f'\n[2/4] Очистка завершена. Допущено объектов: {len(validated_database)} из {len(raw_field_data)}.')

# Фильтрация объектов с помощью (высота > 50 метров)
expressed_relief = [obj for obj in validated_database if obj.elevation > 50]

# Ранжирование по индексу уклона с использованием lambda-функции
sorted_by_slope = sorted(expressed_relief, key=lambda x: x.calculate_slope_index(), reverse=True)

print('-' * 95)
print(f'{"№":<3} | {"Наименование туристического объекта":<45} | {"Высота":<8} | {"Индекс уклона":<12}')
print('-' * 95)

for pos, item in enumerate(sorted_by_slope, 1):
    print(f'{pos:<3} | {item.name:<45} | {item.elevation:<6} м | {item.calculate_slope_index():<12}')
print('-' * 95)

print('\n[3/4] Математическое моделирование потенциала и генерация ГИС-слоев...')
mountain_center = {'lat': 64.8000, 'lon': 59.8333}
map_khmao = folium.Map(location=[62.0, 69.0], zoom_start=5, tiles='Esri.WorldStreetMap')

for obj in sorted_by_slope:
    distance = ((obj.lat - mountain_center['lat'])**2 + (obj.lon - mountain_center['lon'])**2)**0.5
    
    # Задание 1: Изменены веса факторов (высота максимум 30 баллов, близость к горам максимум 70 баллов)
    
    # Если высота равна больше нашего максимального значения мы выбираем, 30, так как оно максимальное
    height_score = min((obj.elevation / 1500) * 30, 30)

    # Если обьект находится очень далеко, то омжет быть отрицательное число, в таком случае будет 0
    distance_score = max(70 - (distance * 5), 0)
    
    potential_score = height_score + distance_score
    
    # Задание 4: Инфраструктурный бонус (+20 баллов для ГЛК и Баз отдыха)
    if obj.obj_type in ["ГЛК", "База отдыха"]:
        potential_score += 20
        
    potential_score = round(potential_score, 1)
    
    # Определение цвета маркера в зависимости от итогового потенциала
    marker_color = 'purple' if potential_score > 70 else ('blue' if potential_score > 40 else 'green')

    html_popup = f'<b>{obj.name}</b><br>Тип: {obj.obj_type}<br>Потенциал: {potential_score} / 100'
    
    folium.Marker(
        location=[obj.lat, obj.lon],
        popup=folium.Popup(html_popup, max_width=260),
        icon=folium.Icon(color=marker_color),
        tooltip=obj.name
    ).add_to(map_khmao)

print('\n[4/4] Экспорт геоинформационной модели в веб-формат...')
output_file = 'map.html'
map_khmao.save(output_file)

if os.path.exists(output_file):
    if hasattr(os, 'startfile'):
        os.startfile(output_file)
    else:
        webbrowser.open('file://' + os.path.abspath(output_file))