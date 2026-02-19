"""
Модуль для расчета стоимости автомобилей
=========================================

Предоставляет классы и функции для расчета рыночной стоимости автомобилей
с учетом различных факторов: возраст, пробег, состояние.

Основные компоненты:
    CarPriceCalculator - основной класс для расчета стоимости
    calculate_depreciation() - функция расчета амортизации
"""

from datetime import datetime
from typing import Dict, Union, Optional, List, Tuple


class CarPriceCalculator:
    """
    Калькулятор стоимости автомобилей с учетом различных факторов
    
    Attributes:
        base_price (float): базовая стоимость автомобиля
        year (int): год выпуска
        mileage (float): пробег в км
        condition (str): состояние (excellent, good, average, poor, damaged)
        current_year (int): текущий год для расчета
    
    Example:
        >>> calc = CarPriceCalculator(1500000, 2020, 50000, "good")
        >>> result = calc.calculate_market_price()
        >>> print(result['market_price'])
    """
    
    # Коэффициенты для разных состояний
    CONDITION_FACTORS = {
        'excellent': 1.2,   # отличное
        'good': 1.0,         # хорошее
        'average': 0.8,      # среднее
        'poor': 0.6,         # плохое
        'damaged': 0.4       # поврежденное
    }
    
    # Рекомендации по состоянию
    CONDITION_DESCRIPTIONS = {
        'excellent': "Отличное состояние, без дефектов",
        'good': "Хорошее состояние, небольшие следы эксплуатации",
        'average': "Среднее состояние, требует мелкого ремонта",
        'poor': "Плохое состояние, требует серьезного ремонта",
        'damaged': "Поврежден, требует восстановления"
    }
    
    def __init__(
        self, 
        base_price: float, 
        year: int, 
        mileage: float = 0,
        condition: str = 'good'
    ):
        """
        Инициализация калькулятора
        
        Args:
            base_price: базовая стоимость (цена покупки или оценки)
            year: год выпуска
            mileage: пробег в километрах
            condition: состояние автомобиля
        
        Raises:
            ValueError: при некорректных параметрах
        """
        # Валидация входных данных
        if base_price <= 0:
            raise ValueError(f"Цена должна быть положительной: {base_price}")
        
        current_year = datetime.now().year
        if year < 1900 or year > current_year + 1:
            raise ValueError(f"Некорректный год выпуска: {year}")
        
        if mileage < 0:
            raise ValueError(f"Пробег не может быть отрицательным: {mileage}")
        
        if condition not in self.CONDITION_FACTORS:
            raise ValueError(
                f"Некорректное состояние. Допустимые значения: {list(self.CONDITION_FACTORS.keys())}"
            )
        
        self.base_price = base_price
        self.year = year
        self.mileage = mileage
        self.condition = condition
        self.current_year = current_year
    
    def calculate_age_factor(self) -> float:
        """
        Рассчитать коэффициент износа по возрасту
        
        Логика: каждый год теряет 3% стоимости, максимум 50% потери
        
        Returns:
            float: коэффициент износа (0.5 - 1.0)
        """
        age = self.current_year - self.year
        factor = max(0.5, 1 - (age * 0.03))
        return round(factor, 2)
    
    def calculate_mileage_factor(self) -> float:
        """
        Рассчитать коэффициент износа по пробегу
        
        Логика:
            < 50,000 км: +10% (малый пробег)
            50,000 - 100,000 км: 0% (нормальный пробег)
            100,000 - 150,000 км: -10% (выше среднего)
            150,000 - 200,000 км: -20% (большой пробег)
            > 200,000 км: -40% (очень большой пробег)
        
        Returns:
            float: коэффициент износа (0.6 - 1.1)
        """
        if self.mileage < 50000:
            return 1.1  # Малый пробег - надбавка
        elif self.mileage < 100000:
            return 1.0  # Средний пробег
        elif self.mileage < 150000:
            return 0.9  # Выше среднего
        elif self.mileage < 200000:
            return 0.8  # Большой пробег
        else:
            return 0.6  # Очень большой пробег
    
    def calculate_condition_factor(self) -> float:
        """
        Рассчитать коэффициент по состоянию
        
        Returns:
            float: коэффициент состояния
        """
        return self.CONDITION_FACTORS.get(self.condition, 1.0)
    
    def calculate_market_price(self) -> Dict[str, Union[float, str, Dict]]:
        """
        Рассчитать рыночную стоимость автомобиля
        
        Формула: 
            рыночная_цена = базовая_цена * возраст_фактор * пробег_фактор * состояние_фактор
        
        Returns:
            Dict: словарь с результатами расчета
            
            Содержит:
                - base_price: базовая цена
                - market_price: расчетная рыночная цена
                - min_price: минимальная цена (для торга)
                - max_price: максимальная цена
                - factors: коэффициенты расчета
                - depreciation: процент амортизации
                - condition: состояние
        """
        age_factor = self.calculate_age_factor()
        mileage_factor = self.calculate_mileage_factor()
        condition_factor = self.calculate_condition_factor()
        
        # Базовая формула расчета
        market_price = (
            self.base_price * 
            age_factor * 
            mileage_factor * 
            condition_factor
        )
        
        # Округление до тысяч
        market_price = round(market_price / 1000) * 1000
        
        # Расчет диапазона цен (±10%)
        min_price = round(market_price * 0.9 / 1000) * 1000
        max_price = round(market_price * 1.1 / 1000) * 1000
        
        # Расчет амортизации
        depreciation = (1 - (market_price / self.base_price)) * 100
        if market_price > self.base_price:
            depreciation = 0  # Нет амортизации если цена выросла
        
        return {
            'base_price': self.base_price,
            'market_price': market_price,
            'min_price': min_price,
            'max_price': max_price,
            'factors': {
                'age': age_factor,
                'mileage': mileage_factor,
                'condition': condition_factor
            },
            'depreciation': round(depreciation, 1),
            'condition': self.condition,
            'condition_description': self.CONDITION_DESCRIPTIONS.get(self.condition, '')
        }
    
    def get_recommendations(self) -> Dict[str, str]:
        """
        Получить рекомендации по цене и продаже
        
        Returns:
            Dict: рекомендации с пояснениями
        """
        result = self.calculate_market_price()
        price = result['market_price']
        
        if price > self.base_price * 1.1:
            return {
                'action': '🚀 СРОЧНО ПРОДАВАТЬ',
                'reason': 'Цена значительно выше базовой',
                'advice': f'Выгодно продать сейчас по цене {price:,} ₽',
                'risk': 'Риск падения цены'
            }
        elif price > self.base_price:
            return {
                'action': '💰 ПРОДАВАТЬ',
                'reason': 'Цена выше базовой',
                'advice': f'Рекомендуемая цена: {price:,} ₽',
                'risk': 'Можно немного поднять цену'
            }
        elif price < self.base_price * 0.7:
            return {
                'action': '⚡ СРОЧНАЯ ПРОДАЖА',
                'reason': 'Высокий износ или большой пробег',
                'advice': f'Снизить цену до {price:,} ₽ для быстрой продажи',
                'risk': 'Дальнейшее падение цены'
            }
        elif price < self.base_price * 0.85:
            return {
                'action': '📉 ПРОДАВАТЬ С ДИСКОНТОМ',
                'reason': 'Умеренный износ',
                'advice': f'Целевая цена: {price:,} ₽. Возможен торг.',
                'risk': 'Незначительное падение'
            }
        else:
            return {
                'action': '⏳ ОЖИДАТЬ',
                'reason': 'Цена в рынке',
                'advice': f'Оптимальная цена: {price:,} ₽. Торг уместен.',
                'risk': 'Цена стабильна'
            }
    
    def compare_with_average(self, average_price: float) -> Dict[str, Union[float, str]]:
        """
        Сравнить с рыночной средней
        
        Args:
            average_price: средняя рыночная цена для этого класса авто
        
        Returns:
            Dict: результаты сравнения
        """
        market_price = self.calculate_market_price()['market_price']
        difference = market_price - average_price
        percent_diff = (difference / average_price) * 100 if average_price else 0
        
        if percent_diff > 10:
            verdict = "Выше рынка"
        elif percent_diff < -10:
            verdict = "Ниже рынка"
        else:
            verdict = "В рынке"
        
        return {
            'market_price': market_price,
            'average_price': average_price,
            'difference': round(difference, 2),
            'percent_diff': round(percent_diff, 1),
            'verdict': verdict,
            'recommendation': self.get_recommendations()['advice']
        }
    
    def calculate_price_range(self, steps: int = 5) -> List[Dict[str, Union[float, str]]]:
        """
        Рассчитать ценовой диапазон с разными условиями
        
        Args:
            steps: количество шагов для вариации
        
        Returns:
            List[Dict]: список цен при разных условиях
        """
        result = []
        conditions = list(self.CONDITION_FACTORS.keys())
        
        for condition in conditions[:steps]:
            temp_calc = CarPriceCalculator(
                self.base_price,
                self.year,
                self.mileage,
                condition
            )
            price = temp_calc.calculate_market_price()['market_price']
            result.append({
                'condition': condition,
                'price': price,
                'description': self.CONDITION_DESCRIPTIONS[condition]
            })
        
        return result


def calculate_depreciation(
    purchase_price: float, 
    purchase_year: int,
    current_year: Optional[int] = None,
    annual_rate: float = 0.1
) -> Dict[str, float]:
    """
    Рассчитать амортизацию (обесценивание) автомобиля
    
    Args:
        purchase_price: цена покупки
        purchase_year: год покупки
        current_year: текущий год (если None - текущий)
        annual_rate: годовая норма амортизации (10% по умолчанию)
    
    Returns:
        Dict: данные об амортизации
            
            - years_owned: лет владения
            - annual_depreciation: ежегодная амортизация
            - total_depreciation: общая амортизация
            - current_value: текущая стоимость
            - depreciation_percent: процент амортизации
    
    Example:
        >>> dep = calculate_depreciation(2000000, 2019)
        >>> print(f"Текущая стоимость: {dep['current_value']}")
    """
    if current_year is None:
        current_year = datetime.now().year
    
    if purchase_year > current_year:
        raise ValueError("Год покупки не может быть больше текущего года")
    
    if purchase_price <= 0:
        raise ValueError("Цена покупки должна быть положительной")
    
    if annual_rate <= 0 or annual_rate > 1:
        raise ValueError("Годовая норма амортизации должна быть между 0 и 1")
    
    years_owned = current_year - purchase_year
    
    # Линейная амортизация
    annual_depreciation = purchase_price * annual_rate
    total_depreciation = annual_depreciation * years_owned
    current_value = max(0, purchase_price - total_depreciation)
    
    # Не может стоить меньше 10% от первоначальной цены
    min_value = purchase_price * 0.1
    if current_value < min_value:
        current_value = min_value
        total_depreciation = purchase_price - min_value
    
    return {
        'years_owned': years_owned,
        'annual_depreciation': round(annual_depreciation, 2),
        'total_depreciation': round(total_depreciation, 2),
        'current_value': round(current_value, 2),
        'depreciation_percent': round(
            (total_depreciation / purchase_price) * 100, 1
        )
    }


def calculate_loan_payment(
    car_price: float,
    down_payment: float,
    interest_rate: float,
    loan_term_months: int
) -> Dict[str, Union[float, str]]:
    """
    Рассчитать ежемесячный платеж по кредиту
    
    Args:
        car_price: стоимость автомобиля
        down_payment: первоначальный взнос
        interest_rate: годовая процентная ставка
        loan_term_months: срок кредита в месяцах
    
    Returns:
        Dict: детали кредита
    """
    loan_amount = car_price - down_payment
    
    if loan_amount <= 0:
        return {
            'loan_amount': 0,
            'monthly_payment': 0,
            'total_payment': down_payment,
            'total_interest': 0,
            'message': 'Кредит не требуется'
        }
    
    monthly_rate = interest_rate / 100 / 12
    
    # Формула аннуитетного платежа
    monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** loan_term_months) / \
                     ((1 + monthly_rate) ** loan_term_months - 1)
    
    total_payment = monthly_payment * loan_term_months
    total_interest = total_payment - loan_amount
    
    return {
        'loan_amount': round(loan_amount, 2),
        'monthly_payment': round(monthly_payment, 2),
        'total_payment': round(total_payment + down_payment, 2),
        'total_interest': round(total_interest, 2),
        'down_payment': down_payment,
        'interest_rate': interest_rate,
        'loan_term_months': loan_term_months
    }


# Для обратной совместимости
__all__ = [
    'CarPriceCalculator',
    'calculate_depreciation',
    'calculate_loan_payment'
] 

