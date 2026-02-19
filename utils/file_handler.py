 """
Модуль для работы с файлами данных
====================================

Предоставляет функции для сохранения и загрузки данных автомобилей
в различных форматах: CSV, JSON, Excel.

Основные функции:
    save_to_csv() - сохранение в CSV
    load_from_csv() - загрузка из CSV
    save_to_json() - сохранение в JSON
    load_from_json() - загрузка из JSON
    save_to_excel() - сохранение в Excel
    load_from_excel() - загрузка из Excel
"""

import os
import json
import csv
from datetime import datetime
from typing import List, Dict, Any, Optional, Union
import uuid

# Попытка импорта опциональных зависимостей
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    import openpyxl
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False

from ..models.car import Car
from ..models.dealership import Dealership


class FileHandlerError(Exception):
    """Исключение при работе с файлами"""
    pass


# ===== CSV функции =====

def save_to_csv(
    cars: List[Car],
    filename: str,
    encoding: str = 'utf-8',
    delimiter: str = ','
) -> str:
    """
    Сохранить список автомобилей в CSV файл
    
    Args:
        cars: список автомобилей
        filename: имя файла
        encoding: кодировка
        delimiter: разделитель
    
    Returns:
        str: путь к сохраненному файлу
    
    Example:
        >>> cars = get_sample_cars(5)
        >>> save_to_csv(cars, "cars.csv")
    """
    if not cars:
        raise FileHandlerError("Список автомобилей пуст")
    
    # Добавляем расширение если нужно
    if not filename.endswith('.csv'):
        filename += '.csv'
    
    # Поля для сохранения
    fields = [
        'brand', 'model', 'year', 'price', 'vin', 'mileage',
        'color', 'engine_type', 'transmission', 'drive',
        'condition', 'status'
    ]
    
    try:
        with open(filename, 'w', encoding=encoding, newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields, delimiter=delimiter)
            
            # Записываем заголовок
            writer.writeheader()
            
            # Записываем данные
            for car in cars:
                row = {
                    'brand': car.brand,
                    'model': car.model,
                    'year': car.year,
                    'price': car.price,
                    'vin': car.vin,
                    'mileage': car.mileage,
                    'color': car.color,
                    'engine_type': car.engine_type,
                    'transmission': car.transmission,
                    'drive': car.drive,
                    'condition': car.condition,
                    'status': car.status.value if hasattr(car.status, 'value') else car.status
                }
                writer.writerow(row)
        
        return os.path.abspath(filename)
        
    except Exception as e:
        raise FileHandlerError(f"Ошибка сохранения CSV: {e}")


def load_from_csv(
    filename: str,
    encoding: str = 'utf-8',
    delimiter: str = ','
) -> List[Car]:
    """
    Загрузить автомобили из CSV файла
    
    Args:
        filename: имя файла
        encoding: кодировка
        delimiter: разделитель
    
    Returns:
        List[Car]: список автомобилей
    
    Example:
        >>> cars = load_from_csv("cars.csv")
    """
    if not os.path.exists(filename):
        raise FileHandlerError(f"Файл {filename} не найден")
    
    cars = []
    
    try:
        with open(filename, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            
            for row in reader:
                # Преобразование типов
                try:
                    car_data = {
                        'brand': row.get('brand', ''),
                        'model': row.get('model', ''),
                        'year': int(row.get('year', 2000)),
                        'price': float(row.get('price', 0)),
                        'vin': row.get('vin', ''),
                        'mileage': float(row.get('mileage', 0)),
                        'color': row.get('color', 'Не указан'),
                        'engine_type': row.get('engine_type', 'Бензин'),
                        'transmission': row.get('transmission', 'Автомат'),
                        'drive': row.get('drive', 'Передний'),
                        'condition': row.get('condition', 'good'),
                        'status': row.get('status', 'В наличии')
                    }
                    
                    from ..models.car import Car
                    car = Car(**car_data)
                    cars.append(car)
                    
                except (ValueError, TypeError) as e:
                    print(f"Ошибка преобразования строки: {row}, {e}")
                    continue
        
        return cars
        
    except Exception as e:
        raise FileHandlerError(f"Ошибка загрузки CSV: {e}")


# ===== JSON функции =====

def save_to_json(
    data: Union[List[Car], Dealership, Dict],
    filename: str,
    encoding: str = 'utf-8',
    indent: int = 2
) -> str:
    """
    Сохранить данные в JSON файл
    
    Args:
        data: данные для сохранения (список авто, автосалон или словарь)
        filename: имя файла
        encoding: кодировка
        indent: отступы для форматирования
    
    Returns:
        str: путь к сохраненному файлу
    
    Example:
        >>> cars = get_sample_cars(5)
        >>> save_to_json(cars, "cars.json")
        
        >>> dealership = create_sample_dealership()
        >>> save_to_json(dealership, "dealership.json")
    """
    if not filename.endswith('.json'):
        filename += '.json'
    
    try:
        # Преобразование данных в формат для JSON
        if isinstance(data, list):
            # Список автомобилей
            json_data = [car.to_dict() for car in data]
        elif isinstance(data, Dealership):
            # Автосалон
            json_data = data.to_dict()
        elif hasattr(data, 'to_dict'):
            # Любой объект с методом to_dict
            json_data = data.to_dict()
        else:
            # Уже словарь
            json_data = data
        
        # Добавляем метаданные
        output = {
            'metadata': {
                'exported_at': datetime.now().isoformat(),
                'count': len(data) if isinstance(data, list) else 1,
                'type': 'list' if isinstance(data, list) else 'object'
            },
            'data': json_data
        }
        
        with open(filename, 'w', encoding=encoding) as f:
            json.dump(output, f, ensure_ascii=False, indent=indent)
        
        return os.path.abspath(filename)
        
    except Exception as e:
        raise FileHandlerError(f"Ошибка сохранения JSON: {e}")


def load_from_json(
    filename: str,
    encoding: str = 'utf-8'
) -> Union[List[Car], Dealership, Dict]:
    """
    Загрузить данные из JSON файла
    
    Args:
        filename: имя файла
        encoding: кодировка
    
    Returns:
        Union[List[Car], Dealership, Dict]: загруженные данные
    
    Example:
        >>> cars = load_from_json("cars.json")
        >>> dealership = load_from_json("dealership.json")
    """
    if not os.path.exists(filename):
        raise FileHandlerError(f"Файл {filename} не найден")
    
    try:
        with open(filename, 'r', encoding=encoding) as f:
            data = json.load(f)
        
        # Извлекаем данные (если есть метаданные)
        if isinstance(data, dict) and 'data' in data:
            data = data['data']
        
        # Определяем тип данных и восстанавливаем объекты
        if isinstance(data, list):
            # Список - восстанавливаем автомобили
            from ..models.car import Car
            cars = []
            for item in data:
                try:
                    car = Car.from_dict(item)
                    cars.append(car)
                except Exception as e:
                    print(f"Ошибка восстановления автомобиля: {e}")
            return cars
            
        elif isinstance(data, dict):
            # Проверяем, может это автосалон
            if 'dealership_id' in data or 'name' in data and 'address' in data:
                from ..models.dealership import Dealership
                try:
                    return Dealership.from_dict(data)
                except Exception:
                    pass
            
            # Проверяем, может это автомобиль
            if 'brand' in data and 'model' in data:
                from ..models.car import Car
                try:
                    return Car.from_dict(data)
                except Exception:
                    pass
        
        return data
        
    except Exception as e:
        raise FileHandlerError(f"Ошибка загрузки JSON: {e}")


# ===== Excel функции =====

def save_to_excel(
    cars: List[Car],
    filename: str,
    sheet_name: str = 'Автомобили'
) -> str:
    """
    Сохранить список автомобилей в Excel файл
    
    Args:
        cars: список автомобилей
        filename: имя файла
        sheet_name: имя листа
    
    Returns:
        str: путь к сохраненному файлу
    
    Requires:
        pandas и openpyxl должны быть установлены
    """
    if not PANDAS_AVAILABLE or not EXCEL_AVAILABLE:
        raise FileHandlerError(
            "Для работы с Excel требуются библиотеки pandas и openpyxl. "
            "Установите их: pip install pandas openpyxl"
        )
    
    if not cars:
        raise FileHandlerError("Список автомобилей пуст")
    
    if not filename.endswith(('.xlsx', '.xls')):
        filename += '.xlsx'
    
    try:
        # Преобразуем в DataFrame
        data = []
        for car in cars:
            row = {
                'Марка': car.brand,
                'Модель': car.model,
                'Год': car.year,
                'Цена': car.price,
                'VIN': car.vin,
                'Пробег': car.mileage,
                'Цвет': car.color,
                'Двигатель': car.engine_type,
                'КПП': car.transmission,
                'Привод': car.drive,
                'Состояние': car.condition,
                'Статус': car.status.value if hasattr(car.status, 'value') else car.status
            }
            data.append(row)
        
        df = pd.DataFrame(data)
        
        # Сохраняем в Excel
        df.to_excel(filename, sheet_name=sheet_name, index=False)
        
        return os.path.abspath(filename)
        
    except Exception as e:
        raise FileHandlerError(f"Ошибка сохранения Excel: {e}")


def load_from_excel(
    filename: str,
    sheet_name: Optional[str] = None
) -> List[Car]:
    """
    Загрузить автомобили из Excel файла
    
    Args:
        filename: имя файла
        sheet_name: имя листа (если None - первый лист)
    
    Returns:
        List[Car]: список автомобилей
    
    Requires:
        pandas и openpyxl должны быть установлены
    """
    if not PANDAS_AVAILABLE or not EXCEL_AVAILABLE:
        raise FileHandlerError(
            "Для работы с Excel требуются библиотеки pandas и openpyxl"
        )
    
    if not os.path.exists(filename):
        raise FileHandlerError(f"Файл {filename} не найден")
    
    try:
        # Загружаем Excel
        if sheet_name:
            df = pd.read_excel(filename, sheet_name=sheet_name)
        else:
            df = pd.read_excel(filename)
        
        # Преобразуем в список автомобилей
        cars = []
        from ..models.car import Car
        
        # Маппинг колонок (русские названия -> английские)
        column_map = {
            'Марка': 'brand',
            'Модель': 'model',
            'Год': 'year',
            'Цена': 'price',
            'VIN': 'vin',
            'Пробег': 'mileage',
            'Цвет': 'color',
            'Двигатель': 'engine_type',
            'КПП': 'transmission',
            'Привод': 'drive',
            'Состояние': 'condition',
            'Статус': 'status'
        }
        
        for _, row in df.iterrows():
            car_data = {}
            for ru_col, en_col in column_map.items():
                if ru_col in df.columns:
                    value = row[ru_col]
                    # Обработка NaN
                    if pd.isna(value):
                        value = '' if en_col in ['brand', 'model'] else 0
                    car_data[en_col] = value
            
            # Заполняем обязательные поля
            if 'brand' not in car_data or not car_data['brand']:
                car_data['brand'] = 'Неизвестно'
            if 'model' not in car_data or not car_data['model']:
                car_data['model'] = 'Неизвестно'
            
            try:
                car = Car(**car_data)
                cars.append(car)
            except Exception as e:
                print(f"Ошибка создания автомобиля из строки: {e}")
        
        return cars
        
    except Exception as e:
        raise FileHandlerError(f"Ошибка загрузки Excel: {e}")


# ===== Текстовые функции =====

def save_to_txt(
    cars: List[Car],
    filename: str,
    encoding: str = 'utf-8'
) -> str:
    """
    Сохранить список автомобилей в текстовый файл (читаемый формат)
    
    Args:
        cars: список автомобилей
        filename: имя файла
        encoding: кодировка
    
    Returns:
        str: путь к сохраненному файлу
    """
    if not filename.endswith('.txt'):
        filename += '.txt'
    
    try:
        with open(filename, 'w', encoding=encoding) as f:
            f.write("=" * 80 + "\n")
            f.write(f"СПИСОК АВТОМОБИЛЕЙ\n")
            f.write(f"Дата экспорта: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
            f.write(f"Всего автомобилей: {len(cars)}\n")
            f.write("=" * 80 + "\n\n")
            
            for i, car in enumerate(cars, 1):
                f.write(f"{i}. {car.brand} {car.model} ({car.year})\n")
                f.write(f"   Цена: {car.price:,.0f} ₽\n")
                f.write(f"   VIN: {car.vin or 'Не указан'}\n")
                f.write(f"   Пробег: {car.mileage:,.0f} км\n")
                f.write(f"   Цвет: {car.color}\n")
                f.write(f"   Двигатель: {car.engine_type}\n")
                f.write(f"   КПП: {car.transmission}\n")
                f.write(f"   Привод: {car.drive}\n")
                f.write(f"   Состояние: {car.condition}\n")
                f.write(f"   Статус: {car.status}\n")
                f.write("-" * 40 + "\n\n")
        
        return os.path.abspath(filename)
        
    except Exception as e:
        raise FileHandlerError(f"Ошибка сохранения TXT: {e}")


# ===== Функции для резервного копирования =====

def create_backup(
    data: Union[List[Car], Dealership],
    base_filename: Optional[str] = None
) -> str:
    """
    Создать резервную копию данных
    
    Args:
        data: данные для бэкапа
        base_filename: базовое имя файла (если None - генерируется)
    
    Returns:
        str: путь к файлу бэкапа
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if base_filename:
        filename = f"{base_filename}_{timestamp}.json"
    else:
        # Генерируем имя на основе типа данных
        if isinstance(data, list):
            prefix = f"cars_backup_{len(data)}"
        elif isinstance(data, Dealership):
            prefix = f"dealership_{data.name.replace(' ', '_')}"
        else:
            prefix = "data_backup"
        
        filename = f"{prefix}_{timestamp}.json"
    
    return save_to_json(data, filename)


def list_backups(directory: str = '.') -> List[Dict[str, Any]]:
    """
    Получить список файлов бэкапов в директории
    
    Args:
        directory: директория для поиска
    
    Returns:
        List[Dict]: список бэкапов с информацией
    """
    backups = []
    
    for filename in os.listdir(directory):
        if filename.endswith('.json') and ('backup' in filename or '_202' in filename):
            filepath = os.path.join(directory, filename)
            stat = os.stat(filepath)
            
            backups.append({
                'filename': filename,
                'path': filepath,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime),
                'modified': datetime.fromtimestamp(stat.st_mtime)
            })
    
    # Сортируем по дате (новые сверху)
    backups.sort(key=lambda x: x['created'], reverse=True)
    
    return backups


def restore_from_backup(
    filename: str,
    backup_dir: str = '.'
) -> Union[List[Car], Dealership, Dict]:
    """
    Восстановить данные из файла бэкапа
    
    Args:
        filename: имя файла бэкапа
        backup_dir: директория с бэкапами
    
    Returns:
        Union[List[Car], Dealership, Dict]: восстановленные данные
    """
    filepath = os.path.join(backup_dir, filename)
    
    if not os.path.exists(filepath):
        raise FileHandlerError(f"Файл бэкапа {filepath} не найден")
    
    return load_from_json(filepath)


# ===== Функции для работы с временными файлами =====

def save_temp(data: Union[List[Car], Dict], prefix: str = 'temp_') -> str:
    """
    Сохранить данные во временный файл
    
    Args:
        data: данные для сохранения
        prefix: префикс имени файла
    
    Returns:
        str: путь к временному файлу
    """
    temp_id = str(uuid.uuid4())[:8]
    filename = f"{prefix}{temp_id}.json"
    
    return save_to_json(data, filename)


def cleanup_temp_files(directory: str = '.', max_age_hours: int = 24) -> int:
    """
    Удалить старые временные файлы
    
    Args:
        directory: директория для очистки
        max_age_hours: максимальный возраст файлов в часах
    
    Returns:
        int: количество удаленных файлов
    """
    import time
    from datetime import timedelta
    
    now = time.time()
    max_age_seconds = max_age_hours * 3600
    deleted = 0
    
    for filename in os.listdir(directory):
        if filename.startswith('temp_') and filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            file_age = now - os.path.getmtime(filepath)
            
            if file_age > max_age_seconds:
                try:
                    os.remove(filepath)
                    deleted += 1
                except Exception:
                    pass
    
    return deleted


# ===== Функции для экспорта в разные форматы =====

def export_cars(
    cars: List[Car],
    filename: str,
    format: str = 'json'
) -> str:
    """
    Экспортировать автомобили в указанном формате
    
    Args:
        cars: список автомобилей
        filename: имя файла
        format: формат ('json', 'csv', 'excel', 'txt')
    
    Returns:
        str: путь к сохраненному файлу
    
    Example:
        >>> cars = get_sample_cars(10)
        >>> export_cars(cars, "export", format="csv")
    """
    format = format.lower()
    
    if format == 'json':
        return save_to_json(cars, filename)
    elif format == 'csv':
        return save_to_csv(cars, filename)
    elif format == 'excel':
        return save_to_excel(cars, filename)
    elif format == 'txt':
        return save_to_txt(cars, filename)
    else:
        raise FileHandlerError(f"Неподдерживаемый формат: {format}")


def import_cars(
    filename: str,
    format: Optional[str] = None
) -> List[Car]:
    """
    Импортировать автомобили из файла
    
    Args:
        filename: имя файла
        format: формат (если None - определяется по расширению)
    
    Returns:
        List[Car]: список автомобилей
    """
    if format is None:
        # Определяем по расширению
        ext = os.path.splitext(filename)[1].lower()
        if ext == '.json':
            format = 'json'
        elif ext in ['.csv']:
            format = 'csv'
        elif ext in ['.xlsx', '.xls']:
            format = 'excel'
        elif ext == '.txt':
            format = 'txt'
        else:
            raise FileHandlerError(f"Не удалось определить формат файла: {filename}")
    
    format = format.lower()
    
    if format == 'json':
        result = load_from_json(filename)
        if isinstance(result, list):
            return result
        elif isinstance(result, dict):
            # Пытаемся восстановить как автомобиль
            from ..models.car import Car
            return [Car.from_dict(result)]
        else:
            return []
    
    elif format == 'csv':
        return load_from_csv(filename)
    
    elif format == 'excel':
        return load_from_excel(filename)
    
    elif format == 'txt':
        # TXT файлы не импортируем обратно
        raise FileHandlerError("Импорт из TXT не поддерживается")
    
    else:
        raise FileHandlerError(f"Неподдерживаемый формат: {format}")


# Для обратной совместимости
__all__ = [
    'FileHandlerError',
    'save_to_csv',
    'load_from_csv',
    'save_to_json',
    'load_from_json',
    'save_to_excel',
    'load_from_excel',
    'save_to_txt',
    'create_backup',
    'list_backups',
    'restore_from_backup',
    'save_temp',
    'cleanup_temp_files',
    'export_cars',
    'import_cars'
]

