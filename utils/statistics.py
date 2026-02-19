"""
Модуль для статистического анализа автомобильных данных
=========================================================

Предоставляет классы и функции для вычисления статистических показателей,
анализа трендов и генерации отчетов по автопарку.

Основные классы:
    CarStatistics - основной класс для статистического анализа
    StatisticsCalculator - калькулятор статистических показателей
    TrendAnalyzer - анализатор трендов
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union, Tuple
from collections import Counter
import math
import statistics
from ..models.car import Car, CarStatus


class StatisticsError(Exception):
    """Исключение при ошибках статистических вычислений"""
    pass


class StatisticsCalculator:
    """
    Калькулятор статистических показателей
    
    Предоставляет статические методы для вычисления различных
    статистических метрик.
    """
    
    @staticmethod
    def mean(values: List[float]) -> float:
        """
        Среднее арифметическое
        
        Args:
            values: список значений
        
        Returns:
            float: среднее значение
        """
        if not values:
            return 0.0
        return sum(values) / len(values)
    
    @staticmethod
    def median(values: List[float]) -> float:
        """
        Медиана
        
        Args:
            values: список значений
        
        Returns:
            float: медиана
        """
        if not values:
            return 0.0
        return statistics.median(values)
    
    @staticmethod
    def mode(values: List[Any]) -> Any:
        """
        Мода (наиболее частое значение)
        
        Args:
            values: список значений
        
        Returns:
            Any: наиболее частое значение
        """
        if not values:
            return None
        
        counter = Counter(values)
        return counter.most_common(1)[0][0]
    
    @staticmethod
    def variance(values: List[float]) -> float:
        """
        Дисперсия
        
        Args:
            values: список значений
        
        Returns:
            float: дисперсия
        """
        if len(values) < 2:
            return 0.0
        return statistics.variance(values)
    
    @staticmethod
    def std_dev(values: List[float]) -> float:
        """
        Среднеквадратическое отклонение
        
        Args:
            values: список значений
        
        Returns:
            float: стандартное отклонение
        """
        if len(values) < 2:
            return 0.0
        return statistics.stdev(values)
    
    @staticmethod
    def min_value(values: List[float]) -> float:
        """
        Минимальное значение
        
        Args:
            values: список значений
        
        Returns:
            float: минимум
        """
        if not values:
            return 0.0
        return min(values)
    
    @staticmethod
    def max_value(values: List[float]) -> float:
        """
        Максимальное значение
        
        Args:
            values: список значений
        
        Returns:
            float: максимум
        """
        if not values:
            return 0.0
        return max(values)
    
    @staticmethod
    def percentile(values: List[float], percent: float) -> float:
        """
        Процентиль
        
        Args:
            values: список значений
            percent: процент (0-100)
        
        Returns:
            float: значение процентиля
        """
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        index = (len(sorted_values) - 1) * percent / 100
        if index.is_integer():
            return sorted_values[int(index)]
        
        i = int(index)
        return sorted_values[i] + (sorted_values[i + 1] - sorted_values[i]) * (index - i)
    
    @staticmethod
    def coefficient_of_variation(values: List[float]) -> float:
        """
        Коэффициент вариации (отношение std к mean)
        
        Args:
            values: список значений
        
        Returns:
            float: коэффициент вариации
        """
        if not values:
            return 0.0
        
        mean_val = StatisticsCalculator.mean(values)
        if mean_val == 0:
            return 0.0
        
        std_val = StatisticsCalculator.std_dev(values)
        return std_val / mean_val
    
    @staticmethod
    def skewness(values: List[float]) -> float:
        """
        Асимметрия распределения
        
        Args:
            values: список значений
        
        Returns:
            float: коэффициент асимметрии
        """
        if len(values) < 3:
            return 0.0
        
        n = len(values)
        mean_val = StatisticsCalculator.mean(values)
        std_val = StatisticsCalculator.std_dev(values)
        
        if std_val == 0:
            return 0.0
        
        skew = sum((x - mean_val) ** 3 for x in values)
        skew = skew / (n * std_val ** 3)
        
        return skew


class TrendAnalyzer:
    """
    Анализатор трендов и временных рядов
    
    Позволяет анализировать изменения показателей во времени,
    выявлять сезонность и прогнозировать тренды.
    """
    
    def __init__(self, data: List[Tuple[datetime, float]]):
        """
        Инициализация анализатора
        
        Args:
            data: список кортежей (дата, значение)
        """
        self.data = sorted(data, key=lambda x: x[0])
        self.dates = [d for d, _ in self.data]
        self.values = [v for _, v in self.data]
    
    def linear_trend(self) -> Dict[str, float]:
        """
        Линейный тренд (метод наименьших квадратов)
        
        Returns:
            Dict: коэффициенты тренда и качество аппроксимации
        """
        if len(self.data) < 2:
            return {'slope': 0, 'intercept': 0, 'r_squared': 0}
        
        # Преобразуем даты в числовые значения (дни от начала)
        start_date = self.dates[0]
        x = [(d - start_date).days for d in self.dates]
        y = self.values
        
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(xi ** 2 for xi in x)
        
        # Коэффициенты линейной регрессии
        denominator = n * sum_x2 - sum_x ** 2
        if denominator == 0:
            return {'slope': 0, 'intercept': 0, 'r_squared': 0}
        
        slope = (n * sum_xy - sum_x * sum_y) / denominator
        intercept = (sum_y - slope * sum_x) / n
        
        # R-squared (коэффициент детерминации)
        y_mean = sum_y / n
        ss_tot = sum((yi - y_mean) ** 2 for yi in y)
        ss_reg = sum(((slope * xi + intercept) - y_mean) ** 2 for xi in x)
        
        r_squared = ss_reg / ss_tot if ss_tot > 0 else 0
        
        return {
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_squared,
            'trend': 'rising' if slope > 0 else 'falling' if slope < 0 else 'stable'
        }
    
    def moving_average(self, window: int = 7) -> List[float]:
        """
        Скользящее среднее
        
        Args:
            window: размер окна
        
        Returns:
            List[float]: сглаженный ряд
        """
        if len(self.values) < window:
            return self.values.copy()
        
        result = []
        for i in range(len(self.values) - window + 1):
            avg = sum(self.values[i:i + window]) / window
            result.append(avg)
        
        return result
    
    def growth_rate(self) -> Dict[str, float]:
        """
        Темпы роста
        
        Returns:
            Dict: показатели роста
        """
        if len(self.values) < 2:
            return {'total_growth': 0, 'average_growth': 0}
        
        first = self.values[0]
        last = self.values[-1]
        
        if first == 0:
            total_growth = float('inf') if last > 0 else 0
        else:
            total_growth = (last - first) / first * 100
        
        # Средний темп роста
        if len(self.values) > 2:
            avg_growth = sum(
                (self.values[i] - self.values[i-1]) / self.values[i-1] * 100
                for i in range(1, len(self.values))
                if self.values[i-1] != 0
            ) / (len(self.values) - 1)
        else:
            avg_growth = total_growth
        
        return {
            'total_growth': total_growth,
            'average_growth': avg_growth,
            'first_value': first,
            'last_value': last
        }
    
    def forecast(self, days_ahead: int) -> List[Tuple[datetime, float]]:
        """
        Прогноз на основе линейного тренда
        
        Args:
            days_ahead: количество дней для прогноза
        
        Returns:
            List[Tuple[datetime, float]]: прогнозные значения
        """
        trend = self.linear_trend()
        slope = trend['slope']
        intercept = trend['intercept']
        
        if not self.dates:
            return []
        
        start_date = self.dates[0]
        last_date = self.dates[-1]
        
        forecast = []
        for i in range(1, days_ahead + 1):
            date = last_date + timedelta(days=i)
            days_from_start = (date - start_date).days
            value = slope * days_from_start + intercept
            forecast.append((date, max(0, value)))  # Неотрицательные значения
        
        return forecast


class CarStatistics:
    """
    Класс для статистического анализа автомобилей
    
    Предоставляет методы для вычисления различных статистических
    показателей по автопарку, анализа распределений и генерации отчетов.
    
    Attributes:
        cars: список автомобилей
        prices: список цен
        years: список годов выпуска
        mileages: список пробегов
    """
    
    def __init__(self, cars: List[Car]):
        """
        Инициализация статистического анализатора
        
        Args:
            cars: список автомобилей
        
        Raises:
            StatisticsError: если список пуст
        """
        self.cars = cars
        self._validate_data()
        
        # Основные числовые ряды
        self.prices = [c.price for c in cars if c.price > 0]
        self.years = [c.year for c in cars]
        self.mileages = [c.mileage for c in cars if c.mileage > 0]
        self.ages = [c.get_age() for c in cars]
        
        # Калькулятор
        self.calc = StatisticsCalculator
    
    def _validate_data(self):
        """Проверка данных"""
        if not self.cars:
            raise StatisticsError("Список автомобилей пуст")
    
    # ===== Базовые статистики =====
    
    def get_price_statistics(self) -> Dict[str, float]:
        """
        Получить статистику по ценам
        
        Returns:
            Dict: статистика цен
        """
        if not self.prices:
            return {}
        
        return {
            'count': len(self.prices),
            'sum': sum(self.prices),
            'mean': self.calc.mean(self.prices),
            'median': self.calc.median(self.prices),
            'mode': self.calc.mode(self.prices),
            'min': self.calc.min_value(self.prices),
            'max': self.calc.max_value(self.prices),
            'std_dev': self.calc.std_dev(self.prices),
            'variance': self.calc.variance(self.prices),
            'cv': self.calc.coefficient_of_variation(self.prices),
            'q1': self.calc.percentile(self.prices, 25),
            'q3': self.calc.percentile(self.prices, 75),
            'iqr': self.calc.percentile(self.prices, 75) - self.calc.percentile(self.prices, 25)
        }
    
    def get_year_statistics(self) -> Dict[str, float]:
        """
        Получить статистику по годам выпуска
        
        Returns:
            Dict: статистика годов
        """
        if not self.years:
            return {}
        
        return {
            'count': len(self.years),
            'mean': self.calc.mean(self.years),
            'median': self.calc.median(self.years),
            'min': self.calc.min_value(self.years),
            'max': self.calc.max_value(self.years),
            'range': self.calc.max_value(self.years) - self.calc.min_value(self.years),
            'std_dev': self.calc.std_dev(self.years)
        }
    
    def get_mileage_statistics(self) -> Dict[str, float]:
        """
        Получить статистику по пробегу
        
        Returns:
            Dict: статистика пробега
        """
        if not self.mileages:
            return {}
        
        return {
            'count': len(self.mileages),
            'sum': sum(self.mileages),
            'mean': self.calc.mean(self.mileages),
            'median': self.calc.median(self.mileages),
            'min': self.calc.min_value(self.mileages),
            'max': self.calc.max_value(self.mileages),
            'std_dev': self.calc.std_dev(self.mileages)
        }
    
    def get_age_statistics(self) -> Dict[str, float]:
        """
        Получить статистику по возрасту
        
        Returns:
            Dict: статистика возраста
        """
        if not self.ages:
            return {}
        
        return {
            'count': len(self.ages),
            'mean': self.calc.mean(self.ages),
            'median': self.calc.median(self.ages),
            'min': self.calc.min_value(self.ages),
            'max': self.calc.max_value(self.ages),
            'std_dev': self.calc.std_dev(self.ages)
        }
    
    # ===== Распределения =====
    
    def get_price_distribution(self, bins: int = 10) -> Dict[str, int]:
        """
        Получить распределение цен по диапазонам
        
        Args:
            bins: количество диапазонов
        
        Returns:
            Dict: распределение цен
        """
        if not self.prices:
            return {}
        
        min_price = min(self.prices)
        max_price = max(self.prices)
        bin_size = (max_price - min_price) / bins if max_price > min_price else 1
        
        distribution = {}
        for i in range(bins):
            lower = min_price + i * bin_size
            upper = lower + bin_size
            if i == bins - 1:
                upper = max_price + 1  # включаем максимум
            
            count = sum(1 for p in self.prices if lower <= p < upper)
            label = f"{lower:,.0f} - {upper:,.0f} ₽"
            distribution[label] = count
        
        return distribution
    
    def get_year_distribution(self) -> Dict[int, int]:
        """
        Получить распределение по годам
        
        Returns:
            Dict: количество авто по годам
        """
        distribution = {}
        for car in self.cars:
            distribution[car.year] = distribution.get(car.year, 0) + 1
        
        return dict(sorted(distribution.items()))
    
    def get_brand_distribution(self) -> Dict[str, int]:
        """
        Получить распределение по маркам
        
        Returns:
            Dict: количество авто по маркам
        """
        distribution = {}
        for car in self.cars:
            distribution[car.brand] = distribution.get(car.brand, 0) + 1
        
        # Сортируем по убыванию
        return dict(sorted(distribution.items(), key=lambda x: x[1], reverse=True))
    
    def get_status_distribution(self) -> Dict[str, int]:
        """
        Получить распределение по статусам
        
        Returns:
            Dict: количество авто по статусам
        """
        distribution = {}
        for car in self.cars:
            status = car.status.value if hasattr(car.status, 'value') else str(car.status)
            distribution[status] = distribution.get(status, 0) + 1
        
        return distribution
    
    def get_color_distribution(self) -> Dict[str, int]:
        """
        Получить распределение по цветам
        
        Returns:
            Dict: количество авто по цветам
        """
        distribution = {}
        for car in self.cars:
            distribution[car.color] = distribution.get(car.color, 0) + 1
        
        return dict(sorted(distribution.items(), key=lambda x: x[1], reverse=True))
    
    def get_condition_distribution(self) -> Dict[str, int]:
        """
        Получить распределение по состоянию
        
        Returns:
            Dict: количество авто по состоянию
        """
        from ..utils.formatter import format_condition
        
        distribution = {}
        for car in self.cars:
            condition_display = format_condition(car.condition)
            distribution[condition_display] = distribution.get(condition_display, 0) + 1
        
        return distribution
    
    # ===== Аналитика =====
    
    def get_top_brands(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Получить топ марок
        
        Args:
            limit: количество в топе
        
        Returns:
            List[Dict]: список марок с показателями
        """
        brand_stats = {}
        
        for car in self.cars:
            if car.brand not in brand_stats:
                brand_stats[car.brand] = {
                    'count': 0,
                    'total_price': 0,
                    'prices': [],
                    'years': []
                }
            
            stats = brand_stats[car.brand]
            stats['count'] += 1
            stats['total_price'] += car.price
            stats['prices'].append(car.price)
            stats['years'].append(car.year)
        
        result = []
        for brand, stats in brand_stats.items():
            result.append({
                'brand': brand,
                'count': stats['count'],
                'avg_price': stats['total_price'] / stats['count'],
                'total_value': stats['total_price'],
                'min_year': min(stats['years']),
                'max_year': max(stats['years']),
                'price_std': self.calc.std_dev(stats['prices']) if len(stats['prices']) > 1 else 0
            })
        
        # Сортируем по количеству
        result.sort(key=lambda x: x['count'], reverse=True)
        
        return result[:limit]
    
    def get_price_analysis_by_age(self) -> Dict[str, Dict[str, float]]:
        """
        Анализ цен по возрастным группам
        
        Returns:
            Dict: статистика цен по возрастным группам
        """
        age_groups = {
            'new': {'ages': range(0, 2), 'prices': []},
            'young': {'ages': range(2, 4), 'prices': []},
            'medium': {'ages': range(4, 7), 'prices': []},
            'old': {'ages': range(7, 11), 'prices': []},
            'vintage': {'ages': range(11, 100), 'prices': []}
        }
        
        for car in self.cars:
            age = car.get_age()
            for group_name, group_data in age_groups.items():
                if age in group_data['ages']:
                    group_data['prices'].append(car.price)
                    break
        
        result = {}
        for group_name, group_data in age_groups.items():
            prices = group_data['prices']
            if prices:
                result[group_name] = {
                    'count': len(prices),
                    'avg_price': self.calc.mean(prices),
                    'min_price': min(prices),
                    'max_price': max(prices),
                    'median': self.calc.median(prices)
                }
        
        return result
    
    def get_depreciation_analysis(self) -> Dict[str, float]:
        """
        Анализ амортизации
        
        Returns:
            Dict: показатели амортизации
        """
        if len(self.cars) < 2:
            return {}
        
        # Группируем по годам
        cars_by_year = {}
        for car in self.cars:
            if car.year not in cars_by_year:
                cars_by_year[car.year] = []
            cars_by_year[car.year].append(car.price)
        
        years = sorted(cars_by_year.keys())
        if len(years) < 2:
            return {}
        
        # Средние цены по годам
        avg_prices = []
        for year in years:
            avg_prices.append(self.calc.mean(cars_by_year[year]))
        
        # Расчет годовой амортизации
        depreciation_rates = []
        for i in range(1, len(avg_prices)):
            if avg_prices[i-1] > 0:
                rate = (avg_prices[i-1] - avg_prices[i]) / avg_prices[i-1] * 100
                depreciation_rates.append(rate)
        
        return {
            'avg_annual_depreciation': self.calc.mean(depreciation_rates) if depreciation_rates else 0,
            'total_depreciation': (avg_prices[0] - avg_prices[-1]) / avg_prices[0] * 100 if avg_prices[0] > 0 else 0,
            'years_range': f"{years[0]}-{years[-1]}",
            'oldest_avg_price': avg_prices[0],
            'newest_avg_price': avg_prices[-1]
        }
    
    # ===== Временные ряды =====
    
    def get_price_trend(self) -> Dict[str, Any]:
        """
        Анализ тренда цен по датам добавления
        
        Returns:
            Dict: результаты анализа тренда
        """
        # Собираем данные по датам
        date_data = {}
        for car in self.cars:
            date = car.created_at.date()
            if date not in date_data:
                date_data[date] = []
            date_data[date].append(car.price)
        
        # Средние цены по дням
        time_series = []
        for date, prices in sorted(date_data.items()):
            time_series.append((datetime.combine(date, datetime.min.time()), 
                               self.calc.mean(prices)))
        
        if len(time_series) < 2:
            return {'has_trend': False}
        
        # Анализ тренда
        analyzer = TrendAnalyzer(time_series)
        trend = analyzer.linear_trend()
        growth = analyzer.growth_rate()
        
        return {
            'has_trend': True,
            'trend': trend['trend'],
            'slope': trend['slope'],
            'r_squared': trend['r_squared'],
            'total_growth': growth['total_growth'],
            'avg_growth': growth['average_growth'],
            'data_points': len(time_series)
        }
    
    # ===== Сводные отчеты =====
    
    def get_summary_statistics(self) -> Dict[str, Any]:
        """
        Получить сводную статистику
        
        Returns:
            Dict: сводная статистика по всем показателям
        """
        price_stats = self.get_price_statistics()
        year_stats = self.get_year_statistics()
        mileage_stats = self.get_mileage_statistics()
        age_stats = self.get_age_statistics()
        
        # Основные показатели
        total_cars = len(self.cars)
        available_cars = sum(1 for c in self.cars if c.is_available())
        sold_cars = sum(1 for c in self.cars if c.status == CarStatus.SOLD)
        
        return {
            'overview': {
                'total_cars': total_cars,
                'available_cars': available_cars,
                'sold_cars': sold_cars,
                'available_percent': (available_cars / total_cars * 100) if total_cars else 0,
                'total_value': price_stats.get('sum', 0),
                'unique_brands': len(self.get_brand_distribution())
            },
            'prices': price_stats,
            'years': year_stats,
            'mileage': mileage_stats,
            'age': age_stats,
            'distributions': {
                'by_status': self.get_status_distribution(),
                'by_brand': self.get_brand_distribution(),
                'by_color': self.get_color_distribution(),
                'by_condition': self.get_condition_distribution()
            }
        }
    
    def get_summary_report(self, detailed: bool = True) -> str:
        """
        Получить текстовый отчет со статистикой
        
        Args:
            detailed: подробный отчет
        
        Returns:
            str: отформатированный отчет
        """
        from ..utils.formatter import (
            format_price, format_mileage, format_percentage,
            format_report_header, format_key_value
        )
        
        stats = self.get_summary_statistics()
        overview = stats['overview']
        prices = stats['prices']
        
        lines = [
            format_report_header("СТАТИСТИЧЕСКИЙ ОТЧЕТ", 
                                subtitle=f"Анализ автопарка ({overview['total_cars']} авто)"),
            "",
            "ОСНОВНЫЕ ПОКАЗАТЕЛИ:",
            format_key_value({
                "Всего автомобилей": overview['total_cars'],
                "В наличии": f"{overview['available_cars']} ({overview['available_percent']:.1f}%)",
                "Продано": overview['sold_cars'],
                "Уникальных марок": overview['unique_brands'],
                "Общая стоимость": format_price(overview['total_value'])
            }),
            "",
            "ЦЕНОВОЙ АНАЛИЗ:",
            format_key_value({
                "Средняя цена": format_price(prices.get('mean', 0)),
                "Медианная цена": format_price(prices.get('median', 0)),
                "Минимальная цена": format_price(prices.get('min', 0)),
                "Максимальная цена": format_price(prices.get('max', 0)),
                "Стандартное отклонение": format_price(prices.get('std_dev', 0)),
                "Коэффициент вариации": f"{prices.get('cv', 0):.2f}"
            })
        ]
        
        if detailed:
            # Добавляем распределение по маркам
            lines.extend([
                "",
                "ТОП МАРОК:"
            ])
            
            for brand_data in self.get_top_brands(5):
                lines.append(
                    f"  • {brand_data['brand']}: {brand_data['count']} авто, "
                    f"средняя цена {format_price(brand_data['avg_price'])}"
                )
            
            # Добавляем распределение по статусам
            lines.extend([
                "",
                "СТАТУСЫ:"
            ])
            
            for status, count in stats['distributions']['by_status'].items():
                percent = (count / overview['total_cars']) * 100
                lines.append(f"  • {status}: {count} ({percent:.1f}%)")
            
            # Добавляем анализ амортизации
            dep_analysis = self.get_depreciation_analysis()
            if dep_analysis:
                lines.extend([
                    "",
                    "АНАЛИЗ АМОРТИЗАЦИИ:",
                    f"  • Среднегодовая амортизация: {dep_analysis['avg_annual_depreciation']:.1f}%",
                    f"  • Общая амортизация за период: {dep_analysis['total_depreciation']:.1f}%"
                ])
        
        lines.append("")
        lines.append("=" * 60)
        
        return '\n'.join(lines)
    
    def get_brand_comparison(self, brand1: str, brand2: str) -> Dict[str, Any]:
        """
        Сравнение двух марок
        
        Args:
            brand1: первая марка
            brand2: вторая марка
        
        Returns:
            Dict: результаты сравнения
        """
        cars1 = [c for c in self.cars if c.brand.lower() == brand1.lower()]
        cars2 = [c for c in self.cars if c.brand.lower() == brand2.lower()]
        
        if not cars1 or not cars2:
            raise StatisticsError("Одна из марок не найдена")
        
        prices1 = [c.price for c in cars1]
        prices2 = [c.price for c in cars2]
        
        stats1 = CarStatistics(cars1)
        stats2 = CarStatistics(cars2)
        
        return {
            brand1: {
                'count': len(cars1),
                'avg_price': self.calc.mean(prices1),
                'median_price': self.calc.median(prices1),
                'price_range': (min(prices1), max(prices1)),
                'avg_age': self.calc.mean([c.get_age() for c in cars1]),
                'total_value': sum(prices1),
                'distribution': stats1.get_status_distribution()
            },
            brand2: {
                'count': len(cars2),
                'avg_price': self.calc.mean(prices2),
                'median_price': self.calc.median(prices2),
                'price_range': (min(prices2), max(prices2)),
                'avg_age': self.calc.mean([c.get_age() for c in cars2]),
                'total_value': sum(prices2),
                'distribution': stats2.get_status_distribution()
            },
            'comparison': {
                'price_difference': self.calc.mean(prices1) - self.calc.mean(prices2),
                'price_ratio': self.calc.mean(prices1) / self.calc.mean(prices2) if self.calc.mean(prices2) > 0 else 0,
                'count_difference': len(cars1) - len(cars2)
            }
        }
    
    def export_to_dict(self) -> Dict[str, Any]:
        """
        Экспорт всей статистики в словарь
        
        Returns:
            Dict: полная статистика
        """
        return {
            'summary': self.get_summary_statistics(),
            'price_distribution': self.get_price_distribution(),
            'brand_distribution': self.get_brand_distribution(),
            'year_distribution': self.get_year_distribution(),
            'status_distribution': self.get_status_distribution(),
            'top_brands': self.get_top_brands(10),
            'depreciation_analysis': self.get_depreciation_analysis(),
            'price_trend': self.get_price_trend(),
            'generated_at': datetime.now().isoformat()
        }


# ===== Вспомогательные функции =====

def compare_dealerships(dealerships: List[Any]) -> Dict[str, Any]:
    """
    Сравнение нескольких автосалонов
    
    Args:
        dealerships: список автосалонов
    
    Returns:
        Dict: результаты сравнения
    """
    results = {}
    
    for dealership in dealerships:
        stats = CarStatistics(dealership.cars)
        results[dealership.name] = {
            'total_cars': len(dealership.cars),
            'total_value': stats.get_price_statistics().get('sum', 0),
            'avg_price': stats.get_price_statistics().get('mean', 0),
            'available_cars': len(dealership.get_available_cars()),
            'unique_brands': len(stats.get_brand_distribution())
        }
    
    # Добавляем сравнение
    if len(results) > 1:
        values = [d['total_value'] for d in results.values()]
        max_value = max(values)
        min_value = min(values)
        
        results['_comparison'] = {
            'max_value_dealership': max(results.items(), key=lambda x: x[1]['total_value'])[0],
            'min_value_dealership': min(results.items(), key=lambda x: x[1]['total_value'])[0],
            'value_range': max_value - min_value,
            'value_ratio': max_value / min_value if min_value > 0 else 0
        }
    
    return results


def calculate_correlation(cars: List[Car]) -> Dict[str, float]:
    """
    Расчет корреляции между различными показателями
    
    Args:
        cars: список автомобилей
    
    Returns:
        Dict: корреляционные коэффициенты
    """
    if len(cars) < 2:
        return {}
    
    # Подготавливаем данные
    data = []
    for car in cars:
        data.append({
            'price': car.price,
            'year': car.year,
            'mileage': car.mileage,
            'age': car.get_age()
        })
    
    # Функция для расчета корреляции Пирсона
    def pearson_corr(x_list, y_list):
        n = len(x_list)
        if n < 2:
            return 0
        
        mean_x = sum(x_list) / n
        mean_y = sum(y_list) / n
        
        numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_list, y_list))
        denominator_x = sum((x - mean_x) ** 2 for x in x_list) ** 0.5
        denominator_y = sum((y - mean_y) ** 2 for y in y_list) ** 0.5
        
        if denominator_x == 0 or denominator_y == 0:
            return 0
        
        return numerator / (denominator_x * denominator_y)
    
    # Извлекаем ряды
    prices = [d['price'] for d in data]
    years = [d['year'] for d in data]
    mileages = [d['mileage'] for d in data]
    ages = [d['age'] for d in data]
    
    return {
        'price_year': pearson_corr(prices, years),
        'price_mileage': pearson_corr(prices, mileages),
        'price_age': pearson_corr(prices, ages),
        'year_mileage': pearson_corr(years, mileages),
        'age_mileage': pearson_corr(ages, mileages)
    }


# Для обратной совместимости
__all__ = [
    'StatisticsError',
    'StatisticsCalculator',
    'TrendAnalyzer',
    'CarStatistics',
    'compare_dealerships',
    'calculate_correlation'
] 

