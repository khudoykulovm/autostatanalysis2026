 """
Модуль для форматирования данных автомобилей
=============================================

Предоставляет функции для форматирования цен, дат, пробега и другой информации
в удобочитаемый вид для отображения пользователю и создания отчетов.

Основные функции:
    format_price() - форматирование цены
    format_mileage() - форматирование пробега
    format_date() - форматирование даты
    format_car_info() - форматирование информации об автомобиле
    format_table() - создание таблиц
"""

from datetime import datetime
from typing import List, Dict, Any, Optional, Union, Tuple
import re


# ===== Форматирование чисел и валют =====

def format_price(
    price: float,
    currency: str = '₽',
    include_currency: bool = True,
    decimal_places: int = 0,
    thousand_separator: str = ' ',
    compact: bool = False
) -> str:
    """
    Форматирование цены в читаемый вид
    
    Args:
        price: цена
        currency: символ валюты (₽, $, €)
        include_currency: добавлять символ валюты
        decimal_places: количество знаков после запятой
        thousand_separator: разделитель тысяч
        compact: компактный формат (1.5 млн вместо 1,500,000)
    
    Returns:
        str: отформатированная цена
    
    Example:
        >>> format_price(1500000)
        '1 500 000 ₽'
        
        >>> format_price(1500000, compact=True)
        '1.5 млн ₽'
        
        >>> format_price(1500000, currency='$', decimal_places=2)
        '1,500,000.00 $'
    """
    if price is None:
        return '—'
    
    if compact and price >= 1_000_000:
        # Компактный формат для больших чисел
        millions = price / 1_000_000
        if millions >= 100:
            return f"{int(millions)} млн {currency}".strip()
        elif millions >= 10:
            return f"{millions:.1f} млн {currency}".strip()
        else:
            return f"{millions:.2f} млн {currency}".strip()
    elif compact and price >= 1_000:
        thousands = price / 1_000
        return f"{thousands:.1f} тыс {currency}".strip()
    
    # Форматирование с разделителями тысяч
    if decimal_places > 0:
        price_str = f"{price:,.{decimal_places}f}"
    else:
        price_str = f"{price:,.0f}"
    
    # Заменяем запятые на нужный разделитель
    if thousand_separator != ',':
        price_str = price_str.replace(',', thousand_separator)
    
    if include_currency:
        return f"{price_str} {currency}".strip()
    
    return price_str


def format_mileage(
    mileage: float,
    unit: str = 'км',
    include_unit: bool = True,
    compact: bool = False
) -> str:
    """
    Форматирование пробега
    
    Args:
        mileage: пробег
        unit: единица измерения (км, мили)
        include_unit: добавлять единицу измерения
        compact: компактный формат
    
    Returns:
        str: отформатированный пробег
    
    Example:
        >>> format_mileage(45000)
        '45 000 км'
        
        >>> format_mileage(45000, compact=True)
        '45 тыс км'
    """
    if mileage is None:
        return '—'
    
    if mileage < 0:
        mileage = abs(mileage)
        prefix = '-'
    else:
        prefix = ''
    
    if compact and mileage >= 1_000:
        thousands = mileage / 1_000
        if thousands >= 100:
            result = f"{prefix}{int(thousands)} тыс"
        else:
            result = f"{prefix}{thousands:.1f} тыс"
    else:
        result = f"{prefix}{mileage:,.0f}".replace(',', ' ')
    
    if include_unit:
        return f"{result} {unit}"
    
    return result


def format_percentage(
    value: float,
    decimal_places: int = 1,
    include_sign: bool = False
) -> str:
    """
    Форматирование процента
    
    Args:
        value: значение в процентах (10.5 = 10.5%)
        decimal_places: количество знаков после запятой
        include_sign: добавлять знак + для положительных
    
    Returns:
        str: отформатированный процент
    
    Example:
        >>> format_percentage(15.5)
        '15.5%'
        
        >>> format_percentage(-5.3, include_sign=True)
        '-5.3%'
    """
    if value is None:
        return '—'
    
    if include_sign and value > 0:
        sign = '+'
    else:
        sign = ''
    
    format_str = f"{{:.{decimal_places}f}}%"
    return format_str.format(value).replace('-', sign)


def format_number(
    number: float,
    decimal_places: int = 0,
    thousand_separator: str = ' ',
    prefix: str = '',
    suffix: str = ''
) -> str:
    """
    Форматирование числа
    
    Args:
        number: число
        decimal_places: количество знаков после запятой
        thousand_separator: разделитель тысяч
        prefix: префикс
        suffix: суффикс
    
    Returns:
        str: отформатированное число
    """
    if number is None:
        return '—'
    
    if decimal_places > 0:
        num_str = f"{number:,.{decimal_places}f}"
    else:
        num_str = f"{number:,.0f}"
    
    if thousand_separator != ',':
        num_str = num_str.replace(',', thousand_separator)
    
    return f"{prefix}{num_str}{suffix}".strip()


# ===== Форматирование дат и времени =====

def format_date(
    date: Optional[datetime],
    format: str = '%d.%m.%Y',
    default: str = '—'
) -> str:
    """
    Форматирование даты
    
    Args:
        date: дата
        format: формат даты
        default: значение по умолчанию
    
    Returns:
        str: отформатированная дата
    
    Example:
        >>> from datetime import datetime
        >>> format_date(datetime.now())
        '15.01.2024'
        
        >>> format_date(datetime.now(), format='%Y-%m-%d')
        '2024-01-15'
    """
    if date is None:
        return default
    
    return date.strftime(format)


def format_datetime(
    dt: Optional[datetime],
    format: str = '%d.%m.%Y %H:%M',
    default: str = '—'
) -> str:
    """
    Форматирование даты и времени
    
    Args:
        dt: дата и время
        format: формат
        default: значение по умолчанию
    
    Returns:
        str: отформатированная дата и время
    """
    if dt is None:
        return default
    
    return dt.strftime(format)


def format_relative_date(date: Optional[datetime]) -> str:
    """
    Форматирование относительной даты (сегодня, вчера, и т.д.)
    
    Args:
        date: дата
    
    Returns:
        str: относительная дата
    
    Example:
        >>> from datetime import datetime, timedelta
        >>> format_relative_date(datetime.now())
        'сегодня'
        
        >>> format_relative_date(datetime.now() - timedelta(days=1))
        'вчера'
    """
    if date is None:
        return '—'
    
    today = datetime.now().date()
    date_only = date.date()
    
    if date_only == today:
        return 'сегодня'
    elif date_only == today - timedelta(days=1):
        return 'вчера'
    elif date_only == today + timedelta(days=1):
        return 'завтра'
    elif (today - date_only).days < 7:
        weekdays = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
        return weekdays[date_only.weekday()]
    else:
        return format_date(date)


# ===== Форматирование строк =====

def truncate_string(
    text: str,
    max_length: int = 50,
    ellipsis: str = '...'
) -> str:
    """
    Обрезать строку до заданной длины
    
    Args:
        text: исходный текст
        max_length: максимальная длина
        ellipsis: многоточие
    
    Returns:
        str: обрезанная строка
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(ellipsis)] + ellipsis


def capitalize_words(text: str) -> str:
    """
    Сделать заглавными первые буквы каждого слова
    
    Args:
        text: исходный текст
    
    Returns:
        str: текст с заглавными буквами
    
    Example:
        >>> capitalize_words('toyota camry')
        'Toyota Camry'
    """
    if not text:
        return text
    
    return ' '.join(word.capitalize() for word in text.split())


def slugify(text: str) -> str:
    """
    Преобразовать текст в slug (для URL)
    
    Args:
        text: исходный текст
    
    Returns:
        str: slug
    
    Example:
        >>> slugify('Toyota Camry 2020')
        'toyota-camry-2020'
    """
    if not text:
        return ''
    
    # Транслитерация русских букв
    translit_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
    
    text = text.lower()
    
    # Транслитерация
    result = ''
    for char in text:
        if char in translit_map:
            result += translit_map[char]
        elif char.isalnum() or char in ['-', '_']:
            result += char
        else:
            result += '-'
    
    # Убираем лишние дефисы
    result = re.sub(r'-+', '-', result)
    result = result.strip('-')
    
    return result


# ===== Форматирование информации об автомобиле =====

def format_car_info(
    car: Any,
    detailed: bool = False,
    include_emoji: bool = True
) -> str:
    """
    Форматирование информации об автомобиле
    
    Args:
        car: объект автомобиля
        detailed: подробный вывод
        include_emoji: добавлять эмодзи
    
    Returns:
        str: отформатированная информация
    
    Example:
        >>> from autostatanalysis.models.car import Car
        >>> car = Car("Toyota", "Camry", 2020, 1500000)
        >>> print(format_car_info(car))
        🚗 Toyota Camry (2020) - 1 500 000 ₽
    """
    if car is None:
        return '—'
    
    emoji = '🚗 ' if include_emoji else ''
    
    # Базовая информация
    basic = f"{emoji}{car.brand} {car.model} ({car.year})"
    
    if not detailed:
        return f"{basic} - {format_price(car.price)}"
    
    # Подробная информация
    lines = [
        basic,
        f"💰 Цена: {format_price(car.price)}",
        f"📏 Пробег: {format_mileage(car.mileage)}",
        f"🎨 Цвет: {car.color}",
        f"🔧 Двигатель: {car.engine_type}",
        f"⚙️ КПП: {car.transmission}",
        f"🔄 Привод: {car.drive}",
        f"📊 Состояние: {car.condition}",
        f"📌 Статус: {car.status}",
    ]
    
    if car.vin:
        lines.append(f"🔢 VIN: {car.vin}")
    
    return '\n'.join(lines)


def format_car_short(car: Any) -> str:
    """
    Краткое форматирование информации об автомобиле
    
    Args:
        car: объект автомобиля
    
    Returns:
        str: краткая информация
    """
    if car is None:
        return '—'
    
    return f"{car.brand} {car.model} ({car.year})"


def format_car_list(
    cars: List[Any],
    title: str = "Список автомобилей",
    numbered: bool = True
) -> str:
    """
    Форматирование списка автомобилей
    
    Args:
        cars: список автомобилей
        title: заголовок
        numbered: нумеровать список
    
    Returns:
        str: отформатированный список
    
    Example:
        >>> cars = get_sample_cars(3)
        >>> print(format_car_list(cars, "Мои авто"))
    """
    if not cars:
        return f"{title}:\n  (пусто)"
    
    lines = [
        "=" * 60,
        title.upper(),
        "=" * 60
    ]
    
    for i, car in enumerate(cars, 1):
        if numbered:
            prefix = f"{i:2d}. "
        else:
            prefix = "• "
        
        lines.append(f"{prefix}{format_car_info(car)}")
        
        if i < len(cars):
            lines.append("")
    
    lines.append("=" * 60)
    lines.append(f"Всего: {len(cars)}")
    
    return '\n'.join(lines)


# ===== Форматирование таблиц =====

def format_table(
    data: List[Dict[str, Any]],
    columns: Optional[List[str]] = None,
    headers: Optional[Dict[str, str]] = None,
    title: Optional[str] = None,
    max_width: int = 80
) -> str:
    """
    Форматирование данных в виде таблицы
    
    Args:
        data: список словарей с данными
        columns: список колонок для отображения (если None - все)
        headers: словарь с заголовками колонок
        title: заголовок таблицы
        max_width: максимальная ширина таблицы
    
    Returns:
        str: отформатированная таблица
    
    Example:
        >>> data = [
        ...     {'brand': 'Toyota', 'model': 'Camry', 'price': 1500000},
        ...     {'brand': 'BMW', 'model': 'X5', 'price': 3500000}
        ... ]
        >>> print(format_table(data, headers={'brand': 'Марка', 'price': 'Цена'}))
    """
    if not data:
        return "Нет данных"
    
    # Определяем колонки
    if columns is None:
        # Берем все уникальные ключи
        all_keys = set()
        for row in data:
            all_keys.update(row.keys())
        columns = sorted(list(all_keys))
    
    # Заголовки
    header_names = []
    for col in columns:
        if headers and col in headers:
            header_names.append(headers[col])
        else:
            header_names.append(col.capitalize())
    
    # Вычисляем ширину колонок
    col_widths = []
    for i, col in enumerate(columns):
        # Ширина заголовка
        width = len(str(header_names[i]))
        
        # Ширина данных
        for row in data:
            val = row.get(col, '')
            width = max(width, len(str(val)))
        
        # Ограничиваем максимальную ширину
        width = min(width, max_width // len(columns))
        col_widths.append(width)
    
    # Формируем таблицу
    lines = []
    
    if title:
        lines.append(title)
        lines.append('')
    
    # Верхняя граница
    lines.append('┌' + '┬'.join('─' * w for w in col_widths) + '┐')
    
    # Заголовки
    header_line = '│'
    for i, header in enumerate(header_names):
        header_line += header.center(col_widths[i]) + '│'
    lines.append(header_line)
    
    # Разделитель
    lines.append('├' + '┼'.join('─' * w for w in col_widths) + '┤')
    
    # Данные
    for row in data:
        data_line = '│'
        for i, col in enumerate(columns):
            val = str(row.get(col, ''))
            data_line += val.ljust(col_widths[i]) + '│'
        lines.append(data_line)
    
    # Нижняя граница
    lines.append('└' + '┴'.join('─' * w for w in col_widths) + '┘')
    
    # Итог
    lines.append(f"Всего строк: {len(data)}")
    
    return '\n'.join(lines)


def format_simple_table(
    data: List[List[Any]],
    headers: Optional[List[str]] = None
) -> str:
    """
    Простое форматирование таблицы
    
    Args:
        data: список строк с данными
        headers: заголовки колонок
    
    Returns:
        str: отформатированная таблица
    """
    if not data:
        return "Нет данных"
    
    # Объединяем заголовки и данные
    if headers:
        all_rows = [headers] + data
    else:
        all_rows = data
    
    # Вычисляем ширину колонок
    col_widths = []
    for col in range(len(all_rows[0])):
        width = max(len(str(row[col])) for row in all_rows)
        col_widths.append(width)
    
    # Формируем таблицу
    lines = []
    
    for i, row in enumerate(all_rows):
        line = ' | '.join(str(cell).ljust(width) for cell, width in zip(row, col_widths))
        lines.append(line)
        
        if i == 0 and headers:
            lines.append('-' * len(line))
    
    return '\n'.join(lines)


# ===== Форматирование отчетов =====

def format_report_header(
    title: str,
    subtitle: Optional[str] = None,
    date: Optional[datetime] = None,
    width: int = 60
) -> str:
    """
    Форматирование заголовка отчета
    
    Args:
        title: заголовок
        subtitle: подзаголовок
        date: дата
        width: ширина
    
    Returns:
        str: отформатированный заголовок
    """
    lines = [
        '=' * width,
        title.center(width),
        '=' * width
    ]
    
    if subtitle:
        lines.append(subtitle.center(width))
    
    if date:
        lines.append(format_date(date, '%d.%m.%Y %H:%M').center(width))
    
    lines.append('=' * width)
    
    return '\n'.join(lines)


def format_key_value(
    data: Dict[str, Any],
    key_width: int = 20,
    indent: int = 0
) -> str:
    """
    Форматирование пар ключ-значение
    
    Args:
        data: словарь с данными
        key_width: ширина поля ключа
        indent: отступ
    
    Returns:
        str: отформатированный текст
    
    Example:
        >>> data = {'Марка': 'Toyota', 'Модель': 'Camry', 'Год': 2020}
        >>> print(format_key_value(data))
        Марка                : Toyota
        Модель               : Camry
        Год                  : 2020
    """
    lines = []
    indent_str = ' ' * indent
    
    for key, value in data.items():
        if value is None:
            value_str = '—'
        else:
            value_str = str(value)
        
        lines.append(f"{indent_str}{key:<{key_width}} : {value_str}")
    
    return '\n'.join(lines)


# ===== Форматирование для разных типов данных =====

def format_condition(condition: str, language: str = 'ru') -> str:
    """
    Форматирование состояния автомобиля
    
    Args:
        condition: код состояния (excellent, good, average, poor, damaged)
        language: язык вывода
    
    Returns:
        str: описание состояния
    
    Example:
        >>> format_condition('good')
        'Хорошее'
    """
    conditions = {
        'ru': {
            'excellent': 'Отличное',
            'good': 'Хорошее',
            'average': 'Среднее',
            'poor': 'Плохое',
            'damaged': 'Поврежден'
        },
        'en': {
            'excellent': 'Excellent',
            'good': 'Good',
            'average': 'Average',
            'poor': 'Poor',
            'damaged': 'Damaged'
        }
    }
    
    return conditions.get(language, conditions['ru']).get(condition, condition)


def format_status(status: str, language: str = 'ru') -> str:
    """
    Форматирование статуса автомобиля
    
    Args:
        status: статус
        language: язык вывода
    
    Returns:
        str: описание статуса
    """
    from ..models.car import CarStatus
    
    status_map = {
        CarStatus.AVAILABLE: {'ru': 'В наличии', 'en': 'Available'},
        CarStatus.SOLD: {'ru': 'Продано', 'en': 'Sold'},
        CarStatus.RESERVED: {'ru': 'Забронировано', 'en': 'Reserved'},
        CarStatus.IN_TRANSIT: {'ru': 'В пути', 'en': 'In transit'},
        CarStatus.UNDER_REPAIR: {'ru': 'В ремонте', 'en': 'Under repair'},
        CarStatus.ARCHIVED: {'ru': 'В архиве', 'en': 'Archived'}
    }
    
    if isinstance(status, CarStatus):
        return status_map.get(status, {}).get(language, status.value)
    
    return status


def format_engine_type(engine_type: str, language: str = 'ru') -> str:
    """
    Форматирование типа двигателя
    
    Args:
        engine_type: тип двигателя
        language: язык вывода
    
    Returns:
        str: описание типа двигателя
    """
    engine_map = {
        'ru': {
            'бензин': 'Бензин',
            'дизель': 'Дизель',
            'гибрид': 'Гибрид',
            'электро': 'Электро',
            'газ': 'Газ'
        },
        'en': {
            'бензин': 'Petrol',
            'дизель': 'Diesel',
            'гибрид': 'Hybrid',
            'электро': 'Electric',
            'газ': 'Gas'
        }
    }
    
    engine_lower = engine_type.lower()
    return engine_map.get(language, engine_map['ru']).get(engine_lower, engine_type)


# ===== Дополнительные утилиты =====

def format_bytes(size_bytes: int) -> str:
    """
    Форматирование размера в байтах
    
    Args:
        size_bytes: размер в байтах
    
    Returns:
        str: отформатированный размер
    
    Example:
        >>> format_bytes(1234567)
        '1.2 MB'
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def format_duration(seconds: int) -> str:
    """
    Форматирование длительности
    
    Args:
        seconds: количество секунд
    
    Returns:
        str: отформатированная длительность
    
    Example:
        >>> format_duration(3665)
        '1ч 1м 5с'
    """
    if seconds < 0:
        return '-' + format_duration(-seconds)
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}ч")
    if minutes > 0:
        parts.append(f"{minutes}м")
    if secs > 0 or not parts:
        parts.append(f"{secs}с")
    
    return ' '.join(parts)


def format_phone(phone: str) -> str:
    """
    Форматирование номера телефона
    
    Args:
        phone: номер телефона
    
    Returns:
        str: отформатированный номер
    
    Example:
        >>> format_phone('79991234567')
        '+7 (999) 123-45-67'
    """
    if not phone:
        return ''
    
    # Убираем все нецифровые символы
    digits = re.sub(r'\D', '', phone)
    
    if len(digits) == 11 and digits.startswith('7'):
        # Российский номер
        return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    elif len(digits) == 11 and digits.startswith('8'):
        # Российский номер с 8
        return f"8 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    elif len(digits) == 10:
        # 10-значный номер
        return f"+7 ({digits[0:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:10]}"
    else:
        return phone


def format_vin(vin: str) -> str:
    """
    Форматирование VIN номера
    
    Args:
        vin: VIN номер
    
    Returns:
        str: отформатированный VIN
    
    Example:
        >>> format_vin('JTDBE32KX12345678')
        'JTDBE32K X12345678'
    """
    if not vin or len(vin) != 17:
        return vin
    
    return f"{vin[:8]} {vin[8:]}"


# Для обратной совместимости
__all__ = [
    'format_price',
    'format_mileage',
    'format_percentage',
    'format_number',
    'format_date',
    'format_datetime',
    'format_relative_date',
    'truncate_string',
    'capitalize_words',
    'slugify',
    'format_car_info',
    'format_car_short',
    'format_car_list',
    'format_table',
    'format_simple_table',
    'format_report_header',
    'format_key_value',
    'format_condition',
    'format_status',
    'format_engine_type',
    'format_bytes',
    'format_duration',
    'format_phone',
    'format_vin'
]

