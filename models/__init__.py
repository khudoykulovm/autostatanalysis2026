"""
Models module - модели данных AutoStatAnalysis
===============================================

Модуль содержит классы для представления данных:

Классы:
    Car - модель автомобиля
    Dealership - модель автосалона
    CarStatus - enum статусов автомобиля
"""

from .car import Car, CarStatus
from .dealership import Dealership

__all__ = [
    'Car',
    'CarStatus',
    'Dealership'
]
