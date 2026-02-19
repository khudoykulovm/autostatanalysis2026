"""
Utils module - вспомогательные утилиты AutoStatAnalysis
=========================================================

Модуль содержит вспомогательные функции:

Функции:
    format_price() - форматирование цены
    format_car_info() - форматирование информации об авто
    save_to_csv() - сохранение в CSV
    load_from_csv() - загрузка из CSV
    CarStatistics - класс для статистического анализа
"""

from .formatter import format_price, format_car_info
from .file_handler import save_to_csv, load_from_csv, save_to_json, load_from_json
from .statistics import CarStatistics

__all__ = [
    'format_price',
    'format_car_info',
    'save_to_csv',
    'load_from_csv',
    'save_to_json',
    'load_from_json',
    'CarStatistics'
]
