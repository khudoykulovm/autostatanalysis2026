"""
Модели данных для автомобилей
==============================

Предоставляет классы для представления автомобилей и связанных сущностей.

Основные классы:
    CarStatus - Enum статусов автомобиля
    Car - основная модель автомобиля
    CarFeature - модель дополнительной характеристики
    CarPhoto - модель фотографии
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Any, Union
from enum import Enum
import json


class CarStatus(Enum):
    """
    Статус автомобиля в системе
    
    Возможные значения:
        AVAILABLE: "В наличии" - доступен для продажи
        SOLD: "Продано" - продан
        RESERVED: "Забронировано" - забронирован
        IN_TRANSIT: "В пути" - ожидается поступление
        UNDER_REPAIR: "В ремонте" - на обслуживании
        ARCHIVED: "В архиве" - удален из активного каталога
    """
    
    AVAILABLE = "В наличии"
    SOLD = "Продано"
    RESERVED = "Забронировано"
    IN_TRANSIT = "В пути"
    UNDER_REPAIR = "В ремонте"
    ARCHIVED = "В архиве"
    
    @classmethod
    def from_string(cls, value: str) -> 'CarStatus':
        """
        Создать статус из строки
        
        Args:
            value: строковое значение статуса
        
        Returns:
            CarStatus: соответствующий enum
        """
        for status in cls:
            if status.value == value or status.name == value.upper():
                return status
        return cls.AVAILABLE
    
    def __str__(self) -> str:
        return self.value


@dataclass
class CarFeature:
    """
    Дополнительная характеристика автомобиля
    
    Attributes:
        name: название характеристики (например, "Климат-контроль")
        category: категория (комфорт, безопасность, мультимедиа)
        value: значение (если применимо, например "2-зонный")
        available: доступна ли характеристика
    """
    
    name: str
    category: str = "Другое"
    value: Optional[str] = None
    available: bool = True
    
    def __str__(self) -> str:
        if self.value:
            return f"{self.name}: {self.value}"
        return self.name
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь"""
        return {
            'name': self.name,
            'category': self.category,
            'value': self.value,
            'available': self.available
        }


@dataclass
class CarPhoto:
    """
    Фотография автомобиля
    
    Attributes:
        url: ссылка на фото
        is_main: главное фото
        description: описание
        uploaded_at: дата загрузки
    """
    
    url: str
    is_main: bool = False
    description: Optional[str] = None
    uploaded_at: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        return self.url
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь"""
        return {
            'url': self.url,
            'is_main': self.is_main,
            'description': self.description,
            'uploaded_at': self.uploaded_at.isoformat()
        }


@dataclass
class Car:
    """
    Основная модель автомобиля
    
    Содержит всю информацию об автомобиле: технические характеристики,
    статус, цену, фотографии и т.д.
    
    Attributes:
        brand: марка автомобиля
        model: модель
        year: год выпуска
        price: цена
        vin: VIN номер
        mileage: пробег в км
        color: цвет
        engine_type: тип двигателя
        transmission: тип коробки передач
        drive: тип привода
        condition: состояние
        status: статус в системе
        features: список дополнительных характеристик
        photos: список фотографий
        description: описание
        owner_name: имя владельца
        owner_phone: телефон владельца
        owner_email: email владельца
        created_at: дата создания записи
        updated_at: дата последнего обновления
    
    Example:
        >>> car = Car(
        ...     brand="Toyota",
        ...     model="Camry",
        ...     year=2020,
        ...     price=1500000,
        ...     mileage=45000,
        ...     color="Черный"
        ... )
        >>> print(car)
        🚗 Toyota Camry (2020) - 1,500,000 ₽ [В наличии]
    """
    
    # Обязательные поля
    brand: str
    model: str
    year: int
    price: float
    
    # Опциональные поля с значениями по умолчанию
    vin: str = ''
    mileage: float = 0
    color: str = 'Не указан'
    engine_type: str = 'Бензин'
    transmission: str = 'Автомат'
    drive: str = 'Передний'
    condition: str = 'good'
    status: CarStatus = CarStatus.AVAILABLE
    
    # Сложные поля
    features: List[CarFeature] = field(default_factory=list)
    photos: List[CarPhoto] = field(default_factory=list)
    description: str = ''
    
    # Информация о владельце
    owner_name: str = ''
    owner_phone: str = ''
    owner_email: str = ''
    
    # Метаданные
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Валидация после инициализации"""
        self._validate()
        
        # Если статус передан как строка, преобразуем в enum
        if isinstance(self.status, str):
            self.status = CarStatus.from_string(self.status)
    
    def _validate(self):
        """Валидация данных"""
        from ..core.validator import (
            validate_brand, validate_model, validate_year,
            validate_price, validate_mileage, validate_vin
        )
        
        # Валидация обязательных полей
        if not self.brand or not isinstance(self.brand, str):
            raise ValueError("Марка должна быть непустой строкой")
        
        if not self.model or not isinstance(self.model, str):
            raise ValueError("Модель должна быть непустой строкой")
        
        current_year = datetime.now().year
        if self.year < 1900 or self.year > current_year + 1:
            raise ValueError(f"Некорректный год выпуска: {self.year}")
        
        if self.price <= 0:
            raise ValueError(f"Цена должна быть положительной: {self.price}")
        
        if self.mileage < 0:
            raise ValueError(f"Пробег не может быть отрицательным: {self.mileage}")
    
    # ===== Основные методы =====
    
    def get_full_name(self) -> str:
        """
        Получить полное название автомобиля
        
        Returns:
            str: "Марка Модель (Год)"
        
        Example:
            >>> car.get_full_name()
            'Toyota Camry (2020)'
        """
        return f"{self.brand} {self.model} ({self.year})"
    
    def get_age(self) -> int:
        """
        Получить возраст автомобиля
        
        Returns:
            int: возраст в годах
        
        Example:
            >>> car.get_age()
            4
        """
        return datetime.now().year - self.year
    
    def is_new(self) -> bool:
        """
        Проверить, новый ли автомобиль
        
        Returns:
            bool: True если пробег < 100 км и возраст <= 1 год
        """
        return self.mileage < 100 and self.get_age() <= 1
    
    def is_available(self) -> bool:
        """
        Проверить, доступен ли автомобиль для продажи
        
        Returns:
            bool: True если статус AVAILABLE
        """
        return self.status == CarStatus.AVAILABLE
    
    def get_price_with_currency(self, currency: str = '₽') -> str:
        """
        Получить цену с валютой
        
        Args:
            currency: символ валюты (₽, $, €)
        
        Returns:
            str: форматированная цена
        
        Example:
            >>> car.get_price_with_currency()
            '1,500,000 ₽'
        """
        return f"{self.price:,.0f} {currency}"
    
    def get_mileage_str(self) -> str:
        """
        Получить пробег в читаемом формате
        
        Returns:
            str: пробег с единицей измерения
        
        Example:
            >>> car.get_mileage_str()
            '45,000 км'
        """
        if self.mileage < 1000:
            return f"{self.mileage:.0f} км"
        return f"{self.mileage:,.0f} км"
    
    # ===== Методы для работы с характеристиками =====
    
    def add_feature(self, feature: CarFeature) -> None:
        """
        Добавить характеристику
        
        Args:
            feature: характеристика для добавления
        """
        self.features.append(feature)
        self.updated_at = datetime.now()
    
    def add_features(self, features: List[CarFeature]) -> None:
        """
        Добавить несколько характеристик
        
        Args:
            features: список характеристик
        """
        self.features.extend(features)
        self.updated_at = datetime.now()
    
    def get_features_by_category(self, category: str) -> List[CarFeature]:
        """
        Получить характеристики по категории
        
        Args:
            category: категория для фильтрации
        
        Returns:
            List[CarFeature]: отфильтрованный список
        """
        return [f for f in self.features if f.category == category]
    
    def get_features_dict(self) -> Dict[str, List[str]]:
        """
        Получить характеристики в виде словаря по категориям
        
        Returns:
            Dict: словарь с категориями и характеристиками
        """
        result = {}
        for feature in self.features:
            if feature.available:
                if feature.category not in result:
                    result[feature.category] = []
                result[feature.category].append(str(feature))
        return result
    
    # ===== Методы для работы с фотографиями =====
    
    def add_photo(self, photo: CarPhoto) -> None:
        """
        Добавить фотографию
        
        Args:
            photo: фотография для добавления
        """
        # Если это первое фото, делаем его главным
        if not self.photos:
            photo.is_main = True
        self.photos.append(photo)
        self.updated_at = datetime.now()
    
    def add_photos(self, photos: List[CarPhoto]) -> None:
        """
        Добавить несколько фотографий
        
        Args:
            photos: список фотографий
        """
        for photo in photos:
            self.add_photo(photo)
    
    def get_main_photo(self) -> Optional[CarPhoto]:
        """
        Получить главное фото
        
        Returns:
            Optional[CarPhoto]: главное фото или None
        """
        for photo in self.photos:
            if photo.is_main:
                return photo
        return self.photos[0] if self.photos else None
    
    def set_main_photo(self, index: int) -> bool:
        """
        Установить главное фото по индексу
        
        Args:
            index: индекс фотографии
        
        Returns:
            bool: True если успешно
        """
        if 0 <= index < len(self.photos):
            for i, photo in enumerate(self.photos):
                photo.is_main = (i == index)
            self.updated_at = datetime.now()
            return True
        return False
    
    # ===== Методы для сериализации =====
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразовать в словарь
        
        Returns:
            Dict: словарь с данными автомобиля
        """
        return {
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'price': self.price,
            'vin': self.vin,
            'mileage': self.mileage,
            'color': self.color,
            'engine_type': self.engine_type,
            'transmission': self.transmission,
            'drive': self.drive,
            'condition': self.condition,
            'status': self.status.value,
            'features': [f.to_dict() for f in self.features],
            'photos': [p.to_dict() for p in self.photos],
            'description': self.description,
            'owner_name': self.owner_name,
            'owner_phone': self.owner_phone,
            'owner_email': self.owner_email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def to_json(self) -> str:
        """
        Преобразовать в JSON строку
        
        Returns:
            str: JSON представление
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Car':
        """
        Создать объект из словаря
        
        Args:
            data: словарь с данными
        
        Returns:
            Car: созданный автомобиль
        
        Example:
            >>> data = {'brand': 'Toyota', 'model': 'Camry', 'year': 2020, 'price': 1500000}
            >>> car = Car.from_dict(data)
        """
        # Обработка сложных полей
        features = []
        if 'features' in data:
            for f_data in data['features']:
                if isinstance(f_data, dict):
                    features.append(CarFeature(**f_data))
        
        photos = []
        if 'photos' in data:
            for p_data in data['photos']:
                if isinstance(p_data, dict):
                    if 'uploaded_at' in p_data and isinstance(p_data['uploaded_at'], str):
                        p_data['uploaded_at'] = datetime.fromisoformat(p_data['uploaded_at'])
                    photos.append(CarPhoto(**p_data))
        
        # Обработка дат
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data and isinstance(data['updated_at'], str):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        
        # Удаляем сложные поля из словаря перед созданием
        car_data = {k: v for k, v in data.items() 
                   if k not in ['features', 'photos']}
        
        car = cls(**car_data)
        car.features = features
        car.photos = photos
        
        return car
    
    # ===== Магические методы =====
    
    def __str__(self) -> str:
        """Строковое представление для пользователя"""
        return (
            f"🚗 {self.brand} {self.model} ({self.year}) - "
            f"{self.get_price_with_currency()} [{self.status}]"
        )
    
    def __repr__(self) -> str:
        """Представление для отладки"""
        return (
            f"Car(brand='{self.brand}', model='{self.model}', "
            f"year={self.year}, price={self.price})"
        )
    
    def __eq__(self, other) -> bool:
        """Сравнение по VIN или по всем полям"""
        if not isinstance(other, Car):
            return False
        if self.vin and other.vin:
            return self.vin == other.vin
        return (
            self.brand == other.brand and
            self.model == other.model and
            self.year == other.year and
            self.price == other.price
        )
    
    def __hash__(self) -> int:
        """Хеш для использования в множествах"""
        if self.vin:
            return hash(self.vin)
        return hash((self.brand, self.model, self.year, self.price))


# Предопределенные наборы характеристик
COMMON_FEATURES = {
    'comfort': [
        CarFeature("Кондиционер", "Комфорт"),
        CarFeature("Климат-контроль", "Комфорт"),
        CarFeature("Электростеклоподъемники", "Комфорт"),
        CarFeature("Подогрев сидений", "Комфорт"),
        CarFeature("Электропривод сидений", "Комфорт"),
        CarFeature("Люк", "Комфорт"),
        CarFeature("Кожаный салон", "Комфорт"),
    ],
    'safety': [
        CarFeature("ABS", "Безопасность"),
        CarFeature("ESP", "Безопасность"),
        CarFeature("Подушки безопасности", "Безопасность"),
        CarFeature("Парктроники", "Безопасность"),
        CarFeature("Камера заднего вида", "Безопасность"),
        CarFeature("Круиз-контроль", "Безопасность"),
    ],
    'multimedia': [
        CarFeature("Bluetooth", "Мультимедиа"),
        CarFeature("USB", "Мультимедиа"),
        CarFeature("AUX", "Мультимедиа"),
        CarFeature("Навигация", "Мультимедиа"),
        CarFeature("Android Auto", "Мультимедиа"),
        CarFeature("Apple CarPlay", "Мультимедиа"),
    ]
}


def create_sample_car() -> Car:
    """
    Создать пример автомобиля с предустановленными характеристиками
    
    Returns:
        Car: пример автомобиля для тестирования
    """
    car = Car(
        brand="Toyota",
        model="Camry",
        year=2020,
        price=1500000,
        mileage=45000,
        color="Черный",
        vin="JTDBE32KX12345678",
        engine_type="Бензин",
        transmission="Автомат",
        drive="Передний",
        condition="good"
    )
    
    # Добавляем характеристики
    car.add_features(COMMON_FEATURES['comfort'][:3])
    car.add_features(COMMON_FEATURES['safety'][:2])
    car.add_features(COMMON_FEATURES['multimedia'][:2])
    
    return car


# Для обратной совместимости
__all__ = [
    'CarStatus',
    'CarFeature',
    'CarPhoto',
    'Car',
    'COMMON_FEATURES',
    'create_sample_car'
]
