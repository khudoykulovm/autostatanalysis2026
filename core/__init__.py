"""
Core module - ядро пакета AutoStatAnalysis
============================================

Модуль содержит основные функции для расчета и анализа:

Классы:
    CarPriceCalculator - калькулятор стоимости автомобилей

Функции:
    calculate_depreciation() - расчет амортизации
    filter_cars_by_price() - фильтрация по цене
    filter_cars_by_year() - фильтрация по году
    validate_car_data() - валидация данных автомобиля
"""

from .calculator import CarPriceCalculator, calculate_depreciation
from .filters import filter_cars_by_price, filter_cars_by_year
from .validator import validate_car_data, ValidationError

__all__ = [
    'CarPriceCalculator',
    'calculate_depreciation',
    'filter_cars_by_price',
    'filter_cars_by_year',
    'validate_car_data',
    'ValidationError'
]
