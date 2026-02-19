"""
Data module - примеры данных для AutoStatAnalysis
===================================================

Модуль содержит функции для генерации тестовых данных:

Функции:
    get_sample_cars() - получить список примеров автомобилей
    generate_test_data() - сгенерировать тестовые данные
    load_sample_dataset() - загрузить пример датасета
"""

from .sample_data import get_sample_cars, generate_test_data, load_sample_dataset

__all__ = [
    'get_sample_cars',
    'generate_test_data',
    'load_sample_dataset'
]
