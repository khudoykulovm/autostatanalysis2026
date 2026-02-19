 """
Модуль для фильтрации автомобилей по различным критериям
==========================================================

Предоставляет функции для фильтрации списков автомобилей
по цене, году, пробегу, марке и другим параметрам.

Основные функции:
    filter_cars_by_price() - фильтрация по цене
    filter_cars_by_year() - фильтрация по году выпуска
    filter_cars_by_mileage() - фильтрация по пробегу
    filter_cars_by_brand() - фильтрация по марке
    search_cars() - поиск по тексту
    sort_cars() - сортировка автомобилей
"""

from typing import List, Dict, Any, Optional, Callable, Union
from datetime import datetime
from ..models.car import Car


def filter_cars_by_price(
    cars: List[Car],
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
) -> List[Car]:
    """
    Фильтрация автомобилей по цене
    
    Args:
        cars: список автомобилей
        min_price: минимальная цена (если None - без ограничения)
        max_price: максимальная цена (если None - без ограничения)
    
    Returns:
        List[Car]: отфильтрованный список
    
    Example:
        >>> cars = get_sample_cars(10)
        >>> cheap_cars = filter_cars_by_price(cars, max_price=1000000)
        >>> expensive_cars = filter_cars_by_price(cars, min_price=2000000)
    """
    if not cars:
        return []
    
    filtered = cars
    
    if min_price is not None:
        filtered = [c for c in filtered if c.price >= min_price]
    
    if max_price is not None:
        filtered = [c for c in filtered if c.price <= max_price]
    
    return filtered


def filter_cars_by_year(
    cars: List[Car],
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    exact_year: Optional[int] = None
) -> List[Car]:
    """
    Фильтрация автомобилей по году выпуска
    
    Args:
        cars: список автомобилей
        min_year: минимальный год
        max_year: максимальный год
        exact_year: точный год
    
    Returns:
        List[Car]: отфильтрованный список
    
    Example:
        >>> cars = get_sample_cars(10)
        >>> new_cars = filter_cars_by_year(cars, min_year=2020)
        >>> old_cars = filter_cars_by_year(cars, max_year=2015)
        >>> cars_2020 = filter_cars_by_year(cars, exact_year=2020)
    """
    if not cars:
        return []
    
    # Проверка на корректность годов
    current_year = datetime.now().year
    
    if exact_year is not None:
        return [c for c in cars if c.year == exact_year]
    
    filtered = cars
    
    if min_year is not None:
        if min_year < 1900 or min_year > current_year + 1:
            raise ValueError(f"Некорректный минимальный год: {min_year}")
        filtered = [c for c in filtered if c.year >= min_year]
    
    if max_year is not None:
        if max_year < 1900 or max_year > current_year + 1:
            raise ValueError(f"Некорректный максимальный год: {max_year}")
        filtered = [c for c in filtered if c.year <= max_year]
    
    return filtered


def filter_cars_by_mileage(
    cars: List[Car],
    min_mileage: Optional[float] = None,
    max_mileage: Optional[float] = None
) -> List[Car]:
    """
    Фильтрация автомобилей по пробегу
    
    Args:
        cars: список автомобилей
        min_mileage: минимальный пробег
        max_mileage: максимальный пробег
    
    Returns:
        List[Car]: отфильтрованный список
    
    Example:
        >>> cars = get_sample_cars(10)
        >>> low_mileage = filter_cars_by_mileage(cars, max_mileage=50000)
        >>> high_mileage = filter_cars_by_mileage(cars, min_mileage=100000)
    """
    if not cars:
        return []
    
    filtered = cars
    
    if min_mileage is not None:
        if min_mileage < 0:
            raise ValueError(f"Пробег не может быть отрицательным: {min_mileage}")
        filtered = [c for c in filtered if c.mileage >= min_mileage]
    
    if max_mileage is not None:
        if max_mileage < 0:
            raise ValueError(f"Пробег не может быть отрицательным: {max_mileage}")
        filtered = [c for c in filtered if c.mileage <= max_mileage]
    
    return filtered


def filter_cars_by_brand(
    cars: List[Car],
    brands: Union[str, List[str]],
    exact_match: bool = True
) -> List[Car]:
    """
    Фильтрация автомобилей по марке
    
    Args:
        cars: список автомобилей
        brands: марка или список марок
        exact_match: точное совпадение (True) или частичное (False)
    
    Returns:
        List[Car]: отфильтрованный список
    
    Example:
        >>> cars = get_sample_cars(10)
        >>> toyota = filter_cars_by_brand(cars, "Toyota")
        >>> japanese = filter_cars_by_brand(cars, ["Toyota", "Honda", "Nissan"])
    """
    if not cars:
        return []
    
    if isinstance(brands, str):
        brands = [brands]
    
    if exact_match:
        return [c for c in cars if c.brand in brands]
    else:
        # Частичное совпадение (без учета регистра)
        brands_lower = [b.lower() for b in brands]
        return [
            c for c in cars 
            if any(b in c.brand.lower() for b in brands_lower)
        ]


def filter_cars_by_status(
    cars: List[Car],
    status: Union[str, List[str]]
) -> List[Car]:
    """
    Фильтрация автомобилей по статусу
    
    Args:
        cars: список автомобилей
        status: статус или список статусов
    
    Returns:
        List[Car]: отфильтрованный список
    
    Example:
        >>> cars = get_sample_cars(10)
        >>> available = filter_cars_by_status(cars, "В наличии")
        >>> sold = filter_cars_by_status(cars, "Продано")
    """
    if not cars:
        return []
    
    if isinstance(status, str):
        status = [status]
    
    return [c for c in cars if c.status.value in status]


def filter_cars_by_age(
    cars: List[Car],
    min_age: Optional[int] = None,
    max_age: Optional[int] = None
) -> List[Car]:
    """
    Фильтрация автомобилей по возрасту
    
    Args:
        cars: список автомобилей
        min_age: минимальный возраст
        max_age: максимальный возраст
    
    Returns:
        List[Car]: отфильтрованный список
    
    Example:
        >>> cars = get_sample_cars(10)
        >>> new_cars = filter_cars_by_age(cars, max_age=3)  # до 3 лет
        >>> old_cars = filter_cars_by_age(cars, min_age=10)  # старше 10 лет
    """
    if not cars:
        return []
    
    current_year = datetime.now().year
    
    filtered = cars
    
    if min_age is not None:
        if min_age < 0:
            raise ValueError(f"Возраст не может быть отрицательным: {min_age}")
        filtered = [c for c in filtered if (current_year - c.year) >= min_age]
    
    if max_age is not None:
        if max_age < 0:
            raise ValueError(f"Возраст не может быть отрицательным: {max_age}")
        filtered = [c for c in filtered if (current_year - c.year) <= max_age]
    
    return filtered


def filter_cars_by_condition(
    cars: List[Car],
    conditions: Union[str, List[str]]
) -> List[Car]:
    """
    Фильтрация автомобилей по состоянию
    
    Args:
        cars: список автомобилей
        conditions: состояние или список состояний
    
    Returns:
        List[Car]: отфильтрованный список
    """
    if not cars:
        return []
    
    if isinstance(conditions, str):
        conditions = [conditions]
    
    return [c for c in cars if c.condition in conditions]


def search_cars(
    cars: List[Car],
    query: str,
    fields: Optional[List[str]] = None
) -> List[Car]:
    """
    Поиск автомобилей по тексту в различных полях
    
    Args:
        cars: список автомобилей
        query: поисковый запрос
        fields: поля для поиска (по умолчанию: brand, model)
    
    Returns:
        List[Car]: результаты поиска
    
    Example:
        >>> cars = get_sample_cars(10)
        >>> results = search_cars(cars, "camry")
        >>> results = search_cars(cars, "toyota", fields=["brand"])
    """
    if not cars or not query:
        return []
    
    if fields is None:
        fields = ['brand', 'model']
    
    query = query.lower()
    results = []
    
    for car in cars:
        for field in fields:
            value = getattr(car, field, '')
            if value and query in str(value).lower():
                results.append(car)
                break
    
    return results


def filter_cars_by_color(
    cars: List[Car],
    colors: Union[str, List[str]]
) -> List[Car]:
    """
    Фильтрация автомобилей по цвету
    
    Args:
        cars: список автомобилей
        colors: цвет или список цветов
    
    Returns:
        List[Car]: отфильтрованный список
    """
    if not cars:
        return []
    
    if isinstance(colors, str):
        colors = [colors]
    
    colors_lower = [c.lower() for c in colors]
    return [
        c for c in cars 
        if c.color and c.color.lower() in colors_lower
    ]


def filter_cars_by_engine_type(
    cars: List[Car],
    engine_types: Union[str, List[str]]
) -> List[Car]:
    """
    Фильтрация автомобилей по типу двигателя
    
    Args:
        cars: список автомобилей
        engine_types: тип двигателя или список типов
    
    Returns:
        List[Car]: отфильтрованный список
    """
    if not cars:
        return []
    
    if isinstance(engine_types, str):
        engine_types = [engine_types]
    
    return [c for c in cars if c.engine_type in engine_types]


def multi_filter(
    cars: List[Car],
    filters: Dict[str, Any]
) -> List[Car]:
    """
    Множественная фильтрация по нескольким критериям
    
    Args:
        cars: список автомобилей
        filters: словарь с критериями фильтрации
    
    Returns:
        List[Car]: отфильтрованный список
    
    Example:
        >>> cars = get_sample_cars(10)
        >>> result = multi_filter(cars, {
        ...     'min_price': 1000000,
        ...     'max_price': 2000000,
        ...     'min_year': 2018,
        ...     'brands': ['Toyota', 'Honda']
        ... })
    """
    if not cars:
        return []
    
    result = cars
    
    # Фильтр по цене
    if 'min_price' in filters or 'max_price' in filters:
        result = filter_cars_by_price(
            result,
            min_price=filters.get('min_price'),
            max_price=filters.get('max_price')
        )
    
    # Фильтр по году
    if 'min_year' in filters or 'max_year' in filters or 'exact_year' in filters:
        result = filter_cars_by_year(
            result,
            min_year=filters.get('min_year'),
            max_year=filters.get('max_year'),
            exact_year=filters.get('exact_year')
        )
    
    # Фильтр по пробегу
    if 'min_mileage' in filters or 'max_mileage' in filters:
        result = filter_cars_by_mileage(
            result,
            min_mileage=filters.get('min_mileage'),
            max_mileage=filters.get('max_mileage')
        )
    
    # Фильтр по марке
    if 'brands' in filters:
        result = filter_cars_by_brand(result, filters['brands'])
    
    # Фильтр по статусу
    if 'status' in filters:
        result = filter_cars_by_status(result, filters['status'])
    
    # Фильтр по возрасту
    if 'min_age' in filters or 'max_age' in filters:
        result = filter_cars_by_age(
            result,
            min_age=filters.get('min_age'),
            max_age=filters.get('max_age')
        )
    
    # Фильтр по цвету
    if 'colors' in filters:
        result = filter_cars_by_color(result, filters['colors'])
    
    # Фильтр по типу двигателя
    if 'engine_types' in filters:
        result = filter_cars_by_engine_type(result, filters['engine_types'])
    
    return result


def sort_cars(
    cars: List[Car],
    key: str = 'price',
    reverse: bool = False
) -> List[Car]:
    """
    Сортировка автомобилей
    
    Args:
        cars: список автомобилей
        key: поле для сортировки (price, year, mileage, age, brand)
        reverse: обратный порядок (True - по убыванию)
    
    Returns:
        List[Car]: отсортированный список
    
    Example:
        >>> cars = get_sample_cars(10)
        >>> by_price = sort_cars(cars, 'price')  # по возрастанию цены
        >>> by_year_desc = sort_cars(cars, 'year', reverse=True)  # по году убывания
    """
    if not cars:
        return []
    
    valid_keys = ['price', 'year', 'mileage', 'age', 'brand']
    if key not in valid_keys:
        raise ValueError(f"Некорректный ключ сортировки. Допустимые: {valid_keys}")
    
    if key == 'age':
        current_year = datetime.now().year
        sorted_cars = sorted(
            cars,
            key=lambda c: current_year - c.year,
            reverse=reverse
        )
    elif key == 'brand':
        sorted_cars = sorted(
            cars,
            key=lambda c: c.brand.lower(),
            reverse=reverse
        )
    else:
        sorted_cars = sorted(
            cars,
            key=lambda c: getattr(c, key),
            reverse=reverse
        )
    
    return sorted_cars


def get_unique_brands(cars: List[Car]) -> List[str]:
    """
    Получить список уникальных марок
    
    Args:
        cars: список автомобилей
    
    Returns:
        List[str]: список уникальных марок
    """
    if not cars:
        return []
    
    brands = sorted(set(c.brand for c in cars if c.brand))
    return brands


def get_price_range(cars: List[Car]) -> Dict[str, float]:
    """
    Получить диапазон цен
    
    Args:
        cars: список автомобилей
    
    Returns:
        Dict: минимальная и максимальная цена
    """
    if not cars:
        return {'min': 0, 'max': 0}
    
    prices = [c.price for c in cars]
    return {
        'min': min(prices),
        'max': max(prices)
    }


def get_year_range(cars: List[Car]) -> Dict[str, int]:
    """
    Получить диапазон годов выпуска
    
    Args:
        cars: список автомобилей
    
    Returns:
        Dict: минимальный и максимальный год
    """
    if not cars:
        return {'min': 0, 'max': 0}
    
    years = [c.year for c in cars]
    return {
        'min': min(years),
        'max': max(years)
    }


def paginate_cars(
    cars: List[Car],
    page: int = 1,
    page_size: int = 10
) -> Dict[str, Any]:
    """
    Пагинация списка автомобилей
    
    Args:
        cars: список автомобилей
        page: номер страницы
        page_size: количество элементов на странице
    
    Returns:
        Dict: результаты с пагинацией
    
    Example:
        >>> cars = get_sample_cars(100)
        >>> page1 = paginate_cars(cars, page=1, page_size=20)
        >>> print(f"Страница {page1['page']}, всего {page1['total_pages']}")
    """
    if not cars:
        return {
            'items': [],
            'total': 0,
            'page': page,
            'page_size': page_size,
            'total_pages': 0,
            'has_next': False,
            'has_previous': False
        }
    
    total = len(cars)
    total_pages = (total + page_size - 1) // page_size
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * page_size
    end = min(start + page_size, total)
    
    return {
        'items': cars[start:end],
        'total': total,
        'page': page,
        'page_size': page_size,
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_previous': page > 1
    }


# Для обратной совместимости
__all__ = [
    'filter_cars_by_price',
    'filter_cars_by_year',
    'filter_cars_by_mileage',
    'filter_cars_by_brand',
    'filter_cars_by_status',
    'filter_cars_by_age',
    'filter_cars_by_condition',
    'filter_cars_by_color',
    'filter_cars_by_engine_type',
    'search_cars',
    'multi_filter',
    'sort_cars',
    'get_unique_brands',
    'get_price_range',
    'get_year_range',
    'paginate_cars'
]

