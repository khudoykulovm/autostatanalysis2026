"""
Модуль с примерами данных для тестирования и демонстрации
===========================================================

Предоставляет функции для генерации тестовых данных об автомобилях,
а также готовые наборы данных для различных целей.

Основные функции:
    get_sample_cars() - получить список примеров автомобилей
    generate_test_data() - сгенерировать тестовые данные
    load_sample_dataset() - загрузить пример датасета
"""

import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from ..models.car import Car, CarStatus


# Константы для генерации данных
BRANDS = [
    "Toyota", "Honda", "Nissan", "Mazda", "Mitsubishi", "Subaru", "Suzuki",
    "BMW", "Mercedes-Benz", "Audi", "Volkswagen", "Porsche", "Opel",
    "Ford", "Chevrolet", "Cadillac", "Jeep", "Dodge",
    "Hyundai", "Kia", "Daewoo", "SsangYong",
    "Volvo", "Saab", "Scania",
    "Fiat", "Alfa Romeo", "Lamborghini", "Ferrari", "Maserati",
    "Renault", "Peugeot", "Citroen", "Bugatti",
    "Lada", "GAZ", "UAZ", "ZAZ"
]

# Модели для разных марок
MODELS_BY_BRAND = {
    "Toyota": ["Camry", "Corolla", "RAV4", "Land Cruiser", "Prius", "Yaris", "Highlander", "C-HR"],
    "Honda": ["Civic", "Accord", "CR-V", "Pilot", "Fit", "HR-V", "Odyssey"],
    "BMW": ["X5", "X3", "X1", "3 Series", "5 Series", "7 Series", "M3", "M5"],
    "Mercedes-Benz": ["E-Class", "C-Class", "S-Class", "GLC", "GLE", "G-Class", "A-Class"],
    "Audi": ["A4", "A6", "A8", "Q5", "Q7", "TT", "R8"],
    "Volkswagen": ["Golf", "Passat", "Tiguan", "Polo", "Jetta", "Touareg"],
    "Ford": ["Focus", "Fusion", "Mustang", "Explorer", "F-150", "Kuga"],
    "Hyundai": ["Solaris", "Creta", "Tucson", "Santa Fe", "Elantra", "Sonata"],
    "Kia": ["Rio", "Sportage", "Sorento", "Optima", "Ceed", "Stinger"],
    "Lada": ["Granta", "Vesta", "Largus", "Niva", "X-Ray", "Kalina"],
    "Renault": ["Logan", "Sandero", "Duster", "Kaptur", "Megan", "Arkana"],
    "Nissan": ["Qashqai", "X-Trail", "Juke", "Almera", "Terrano", "Patrol"]
}

# Цвета автомобилей
COLORS = [
    "Белый", "Черный", "Серый", "Серебристый", "Красный",
    "Синий", "Голубой", "Зеленый", "Желтый", "Оранжевый",
    "Коричневый", "Бежевый", "Фиолетовый", "Золотой", "Бордовый"
]

# Типы двигателей
ENGINE_TYPES = ["Бензин", "Дизель", "Гибрид", "Электро", "Газ"]

# Типы коробок передач
TRANSMISSIONS = ["Механика", "Автомат", "Робот", "Вариатор"]

# Типы привода
DRIVES = ["Передний", "Задний", "Полный"]

# Состояния автомобилей
CONDITIONS = ["excellent", "good", "average", "poor", "damaged"]

# Статусы
STATUSES = [CarStatus.AVAILABLE, CarStatus.SOLD, CarStatus.RESERVED, CarStatus.IN_TRANSIT]


def get_sample_cars(count: int = 5, realistic: bool = True) -> List[Car]:
    """
    Получить список примеров автомобилей
    
    Args:
        count: количество автомобилей
        realistic: реалистичные данные (True) или случайные (False)
    
    Returns:
        List[Car]: список объектов Car
    
    Example:
        >>> cars = get_sample_cars(10)
        >>> for car in cars:
        ...     print(car)
    """
    cars = []
    
    for i in range(count):
        if realistic:
            car = _generate_realistic_car(i)
        else:
            car = _generate_random_car(i)
        
        cars.append(car)
    
    return cars


def _generate_realistic_car(index: int) -> Car:
    """Генерация реалистичного автомобиля"""
    
    # Выбираем бренд с весами (более популярные чаще)
    brand_weights = {
        "Toyota": 15, "Honda": 12, "Nissan": 10, "Mazda": 8,
        "BMW": 10, "Mercedes-Benz": 8, "Audi": 7, "Volkswagen": 10,
        "Ford": 8, "Hyundai": 12, "Kia": 10, "Lada": 15,
        "Renault": 8, "Mitsubishi": 5, "Subaru": 3
    }
    
    brands_list = list(brand_weights.keys())
    weights = list(brand_weights.values())
    brand = random.choices(brands_list, weights=weights)[0]
    
    # Выбираем модель
    if brand in MODELS_BY_BRAND:
        model = random.choice(MODELS_BY_BRAND[brand])
    else:
        model = f"Model-{random.randint(1, 10)}"
    
    # Год выпуска (чаще последние 10 лет)
    current_year = datetime.now().year
    year_weights = [1] * (current_year - 2000 + 1)
    for i in range(min(10, len(year_weights))):
        year_weights[-(i+1)] = 10 - i  # последние годы имеют больший вес
    
    year = random.choices(
        range(2000, current_year + 1),
        weights=year_weights[:current_year-2000+1]
    )[0]
    
    # Цена зависит от марки, года и модели
    base_price = _get_base_price(brand, model)
    age_factor = 1 - (current_year - year) * 0.03
    price = int(base_price * max(0.5, age_factor))
    price = round(price / 1000) * 1000  # округление до тысяч
    
    # Пробег
    age = current_year - year
    if age <= 1:
        mileage = random.randint(0, 15000)
    elif age <= 3:
        mileage = random.randint(10000, 60000)
    elif age <= 5:
        mileage = random.randint(40000, 100000)
    elif age <= 10:
        mileage = random.randint(80000, 180000)
    else:
        mileage = random.randint(150000, 300000)
    
    # Генерация VIN
    vin = _generate_vin(brand, year, index)
    
    # Цвет
    color = random.choice(COLORS)
    
    # Тип двигателя
    if "электро" in model.lower() or brand in ["Tesla"]:
        engine_type = "Электро"
    elif "гибрид" in model.lower() or "Prius" in model:
        engine_type = "Гибрид"
    elif year > 2015 and random.random() > 0.7:
        engine_type = random.choice(["Бензин", "Дизель", "Гибрид"])
    else:
        engine_type = random.choice(["Бензин", "Дизель"])
    
    # Коробка передач
    if year > 2010:
        transmission = random.choices(
            ["Автомат", "Механика", "Робот", "Вариатор"],
            weights=[60, 20, 10, 10]
        )[0]
    else:
        transmission = random.choices(
            ["Механика", "Автомат"],
            weights=[40, 60]
        )[0]
    
    # Привод
    if "SUV" in model or "внедорожник" in model.lower() or brand in ["Jeep", "Land Rover"]:
        drive = random.choices(["Полный", "Передний"], weights=[80, 20])[0]
    else:
        drive = random.choices(["Передний", "Задний", "Полный"], weights=[60, 20, 20])[0]
    
    # Состояние
    if age <= 3 and mileage < 50000:
        condition = random.choices(["excellent", "good"], weights=[60, 40])[0]
    elif age <= 7 and mileage < 120000:
        condition = random.choices(["good", "average"], weights=[70, 30])[0]
    elif age <= 12:
        condition = random.choices(["average", "poor"], weights=[60, 40])[0]
    else:
        condition = random.choices(["poor", "damaged"], weights=[70, 30])[0]
    
    # Статус
    if price > 3000000:
        status = random.choices(
            [CarStatus.AVAILABLE, CarStatus.RESERVED, CarStatus.SOLD],
            weights=[30, 40, 30]
        )[0]
    elif price < 500000:
        status = random.choices(
            [CarStatus.AVAILABLE, CarStatus.SOLD],
            weights=[20, 80]
        )[0]
    else:
        status = random.choices(
            [CarStatus.AVAILABLE, CarStatus.SOLD, CarStatus.RESERVED],
            weights=[50, 30, 20]
        )[0]
    
    # Создаем автомобиль
    car = Car(
        brand=brand,
        model=model,
        year=year,
        price=price,
        vin=vin,
        mileage=mileage,
        color=color,
        engine_type=engine_type,
        transmission=transmission,
        drive=drive,
        condition=condition,
        status=status
    )
    
    return car


def _generate_random_car(index: int) -> Car:
    """Генерация полностью случайного автомобиля"""
    
    brand = random.choice(BRANDS)
    model = f"Model-{random.randint(1, 999)}"
    year = random.randint(1990, datetime.now().year)
    price = random.randint(100000, 5000000)
    mileage = random.randint(0, 300000)
    vin = f"VIN{random.randint(10000000000000000, 99999999999999999)}"
    color = random.choice(COLORS)
    engine_type = random.choice(ENGINE_TYPES)
    transmission = random.choice(TRANSMISSIONS)
    drive = random.choice(DRIVES)
    condition = random.choice(CONDITIONS)
    status = random.choice(STATUSES)
    
    return Car(
        brand=brand,
        model=model,
        year=year,
        price=price,
        vin=vin,
        mileage=mileage,
        color=color,
        engine_type=engine_type,
        transmission=transmission,
        drive=drive,
        condition=condition,
        status=status
    )


def _get_base_price(brand: str, model: str) -> int:
    """Получить базовую цену для марки/модели"""
    
    # Премиум бренды
    premium_brands = ["BMW", "Mercedes-Benz", "Audi", "Porsche", "Lexus", "Infiniti"]
    luxury_brands = ["Ferrari", "Lamborghini", "Maserati", "Bugatti"]
    budget_brands = ["Lada", "Daewoo", "ZAZ", "Datsun"]
    
    if brand in luxury_brands:
        base = random.randint(5000000, 20000000)
    elif brand in premium_brands:
        base = random.randint(2000000, 8000000)
    elif brand in budget_brands:
        base = random.randint(300000, 1500000)
    else:
        base = random.randint(500000, 3000000)
    
    # Корректировка по модели
    if "SUV" in model or "внедорожник" in model.lower():
        base = int(base * 1.3)
    elif "спорт" in model.lower() or "GT" in model:
        base = int(base * 1.5)
    
    return base


def _generate_vin(brand: str, year: int, index: int) -> str:
    """Генерация VIN номера"""
    
    # Первые 3 символа - WMI (мировой индекс производителя)
    wmi_map = {
        "Toyota": "JT", "Honda": "JH", "Nissan": "JN", "Mazda": "JM",
        "BMW": "WB", "Mercedes-Benz": "WD", "Audi": "WA", "Volkswagen": "WV",
        "Ford": "1F", "Chevrolet": "1G", "Hyundai": "KM", "Kia": "KN",
        "Lada": "X7", "Renault": "VF", "Peugeot": "VF"
    }
    
    wmi = wmi_map.get(brand, "XX")
    
    # 4-9 символы - VDS (описательная часть)
    vds = f"{random.randint(100000, 999999)}"
    
    # 10 символ - год
    year_codes = "ABCDEFGHJKLMNPRSTVWXY123456789"
    year_index = (year - 1980) % len(year_codes)
    year_code = year_codes[year_index]
    
    # 11 символ - завод
    plant = chr(65 + random.randint(0, 25))
    
    # 12-17 - серийный номер
    serial = f"{index:06d}"
    
    vin = f"{wmi}{vds[0:6]}{year_code}{plant}{serial}"
    
    return vin[:17]  # обрезаем до 17 символов


def generate_test_data(
    count: int = 20,
    include_stats: bool = True
) -> Dict[str, Any]:
    """
    Сгенерировать тестовые данные для демонстрации
    
    Args:
        count: количество автомобилей
        include_stats: включить статистику
    
    Returns:
        Dict: тестовые данные со статистикой
    
    Example:
        >>> data = generate_test_data(30)
        >>> print(f"Всего авто: {data['statistics']['total']}")
        >>> print(f"Общая стоимость: {data['statistics']['total_value']}")
    """
    cars = get_sample_cars(count, realistic=True)
    
    result = {
        'cars': [car.to_dict() for car in cars],
        'generated_at': datetime.now().isoformat(),
        'count': len(cars)
    }
    
    if include_stats:
        # Статистика
        prices = [c.price for c in cars]
        years = [c.year for c in cars]
        statuses = {}
        brands = {}
        
        for car in cars:
            # Статусы
            status_name = car.status.value
            statuses[status_name] = statuses.get(status_name, 0) + 1
            
            # Бренды
            brands[car.brand] = brands.get(car.brand, 0) + 1
        
        result['statistics'] = {
            'total': len(cars),
            'total_value': sum(prices),
            'average_price': round(sum(prices) / len(prices), 2) if prices else 0,
            'min_price': min(prices) if prices else 0,
            'max_price': max(prices) if prices else 0,
            'avg_year': round(sum(years) / len(years), 1) if years else 0,
            'min_year': min(years) if years else 0,
            'max_year': max(years) if years else 0,
            'statuses': statuses,
            'brands': dict(sorted(brands.items(), key=lambda x: x[1], reverse=True)),
            'unique_brands': len(brands)
        }
    
    return result


def load_sample_dataset(dataset_name: str = "default") -> List[Car]:
    """
    Загрузить пример датасета
    
    Args:
        dataset_name: имя датасета ("default", "luxury", "economy", "vintage")
    
    Returns:
        List[Car]: список автомобилей
    """
    
    if dataset_name == "luxury":
        # Премиум автомобили
        brands = ["BMW", "Mercedes-Benz", "Audi", "Porsche", "Lexus"]
        years = range(2018, 2024)
        cars = []
        for i in range(10):
            car = Car(
                brand=random.choice(brands),
                model=f"Premium-{i+1}",
                year=random.choice(years),
                price=random.randint(3000000, 10000000),
                mileage=random.randint(0, 50000),
                condition="excellent"
            )
            cars.append(car)
        return cars
    
    elif dataset_name == "economy":
        # Бюджетные автомобили
        brands = ["Lada", "Hyundai", "Kia", "Renault", "Datsun"]
        cars = []
        for i in range(15):
            car = Car(
                brand=random.choice(brands),
                model=f"Economy-{i+1}",
                year=random.randint(2015, 2023),
                price=random.randint(300000, 1200000),
                mileage=random.randint(50000, 150000),
                condition=random.choice(["good", "average"])
            )
            cars.append(car)
        return cars
    
    elif dataset_name == "vintage":
        # Винтажные автомобили
        cars = []
        for i in range(5):
            car = Car(
                brand=random.choice(["Ford", "Chevrolet", "Cadillac", "Mercedes-Benz"]),
                model=f"Classic-{i+1}",
                year=random.randint(1960, 1990),
                price=random.randint(500000, 5000000),
                mileage=random.randint(100000, 300000),
                condition=random.choice(["average", "poor"])
            )
            cars.append(car)
        return cars
    
    else:  # default
        return get_sample_cars(15)


def export_to_json(cars: List[Car], filename: str = "cars_data.json") -> str:
    """
    Экспортировать данные в JSON файл
    
    Args:
        cars: список автомобилей
        filename: имя файла
    
    Returns:
        str: путь к сохраненному файлу
    """
    data = {
        'exported_at': datetime.now().isoformat(),
        'count': len(cars),
        'cars': [car.to_dict() for car in cars]
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return filename


def get_car_statistics_sample() -> Dict[str, Any]:
    """
    Получить пример статистики по автомобилям
    
    Returns:
        Dict: пример статистических данных
    """
    return {
        'total_cars': 50,
        'by_brand': {
            'Toyota': 12,
            'BMW': 8,
            'Mercedes': 7,
            'Hyundai': 6,
            'Lada': 5,
            'Другие': 12
        },
        'by_year': {
            '2020-2024': 15,
            '2015-2019': 20,
            '2010-2014': 10,
            'до 2010': 5
        },
        'by_status': {
            'В наличии': 30,
            'Продано': 15,
            'Забронировано': 5
        },
        'price_range': {
            'min': 350000,
            'max': 8500000,
            'avg': 1850000
        },
        'avg_mileage': 65000
    }


def get_popular_brands() -> List[Dict[str, Any]]:
    """
    Получить список популярных марок с характеристиками
    
    Returns:
        List[Dict]: список марок с информацией
    """
    return [
        {
            'brand': 'Toyota',
            'popularity': 95,
            'avg_price': 2500000,
            'reliability': 92,
            'categories': ['Седаны', 'Кроссоверы', 'Внедорожники']
        },
        {
            'brand': 'BMW',
            'popularity': 88,
            'avg_price': 4500000,
            'reliability': 85,
            'categories': ['Седаны', 'Кроссоверы', 'Спорткары']
        },
        {
            'brand': 'Hyundai',
            'popularity': 85,
            'avg_price': 1800000,
            'reliability': 88,
            'categories': ['Седаны', 'Кроссоверы', 'Хэтчбеки']
        },
        {
            'brand': 'Lada',
            'popularity': 82,
            'avg_price': 800000,
            'reliability': 75,
            'categories': ['Седаны', 'Хэтчбеки', 'Внедорожники']
        },
        {
            'brand': 'Mercedes-Benz',
            'popularity': 80,
            'avg_price': 5500000,
            'reliability': 87,
            'categories': ['Седаны', 'Кроссоверы', 'Представительские']
        }
    ]


# Для обратной совместимости
__all__ = [
    'get_sample_cars',
    'generate_test_data',
    'load_sample_dataset',
    'export_to_json',
    'get_car_statistics_sample',
    'get_popular_brands',
    'BRANDS',
    'COLORS',
    'ENGINE_TYPES',
    'TRANSMISSIONS',
    'DRIVES',
    'CONDITIONS'
] 

