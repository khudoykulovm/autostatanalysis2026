"""
AutoStatAnalysis - Пакет для анализа автомобильных данных
===========================================================

Пакет предоставляет инструменты для:
- Расчет стоимости автомобилей
- Статистический анализ автопарка
- Работа с моделями данных
- Валидация и форматирование

Основные модули:
    core: ядро пакета (калькулятор, фильтры, валидатор)
    models: модели данных (автомобиль, автосалон)
    utils: вспомогательные утилиты
    data: примеры данных
"""

__version__ = '0.1.0'
__author__ = 'Murodjon'
__email__ = 'khudoykulov2003@gmail.com'

# Импорты для удобства использования
from .models.car import Car
from .core.calculator import CarPriceCalculator
from .utils.formatter import format_price
from .data.sample_data import get_sample_cars

__all__ = [
    'Car',
    'CarPriceCalculator',
    'format_price',
    'get_sample_cars'
]
