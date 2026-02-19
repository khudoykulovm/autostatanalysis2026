"""
Модуль для валидации данных автомобилей
========================================

Предоставляет функции и классы для проверки корректности
данных об автомобилях перед их обработкой или сохранением.

Основные компоненты:
    ValidationError - класс исключения для ошибок валидации
    validate_car_data() - основная функция валидации
    CarValidator - класс с методами валидации
"""

from datetime import datetime
from typing import Dict, Any, List, Optional, Union
import re


class ValidationError(Exception):
    """
    Исключение, возникающее при ошибке валидации данных
    
    Attributes:
        message: сообщение об ошибке
        field: поле, в котором произошла ошибка
        value: некорректное значение
    """
    
    def __init__(self, message: str, field: Optional[str] = None, value: Any = None):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.field:
            return f"[{self.field}] {self.message} (значение: {self.value})"
        return self.message


class CarValidator:
    """
    Класс для валидации данных автомобиля
    
    Содержит методы для проверки отдельных полей
    и комплексной валидации всего объекта.
    """
    
    # Допустимые типы двигателей
    VALID_ENGINE_TYPES = ['бензин', 'дизель', 'гибрид', 'электро', 'газ']
    
    # Допустимые типы коробок передач
    VALID_TRANSMISSIONS = ['механика', 'автомат', 'робот', 'вариатор']
    
    # Допустимые типы привода
    VALID_DRIVES = ['передний', 'задний', 'полный']
    
    # Допустимые состояния
    VALID_CONDITIONS = ['excellent', 'good', 'average', 'poor', 'damaged']
    
    # Допустимые цвета (основные)
    VALID_COLORS = [
        'белый', 'черный', 'серый', 'серебристый', 'красный',
        'синий', 'зеленый', 'желтый', 'коричневый', 'бежевый',
        'оранжевый', 'фиолетовый', 'золотой'
    ]
    
    def __init__(self, strict_mode: bool = False):
        """
        Инициализация валидатора
        
        Args:
            strict_mode: строгий режим (проверка всех полей)
        """
        self.strict_mode = strict_mode
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    @staticmethod
    def validate_brand(brand: Any) -> bool:
        """
        Проверка марки автомобиля
        
        Args:
            brand: марка для проверки
        
        Returns:
            True если корректно
        
        Raises:
            ValidationError: если марка некорректна
        """
        if not brand:
            raise ValidationError("Марка не может быть пустой", 'brand', brand)
        
        if not isinstance(brand, str):
            raise ValidationError(
                f"Марка должна быть строкой, получен {type(brand).__name__}",
                'brand', brand
            )
        
        brand = brand.strip()
        if len(brand) < 2:
            raise ValidationError(
                "Марка должна содержать минимум 2 символа",
                'brand', brand
            )
        
        if len(brand) > 50:
            raise ValidationError(
                "Марка не может быть длиннее 50 символов",
                'brand', brand
            )
        
        # Проверка на допустимые символы (буквы, цифры, дефис, пробел)
        if not re.match(r'^[a-zA-Zа-яА-Я0-9\s\-]+$', brand):
            raise ValidationError(
                "Марка может содержать только буквы, цифры, дефис и пробелы",
                'brand', brand
            )
        
        return True
    
    @staticmethod
    def validate_model(model: Any) -> bool:
        """
        Проверка модели автомобиля
        
        Args:
            model: модель для проверки
        
        Returns:
            True если корректно
        
        Raises:
            ValidationError: если модель некорректна
        """
        if not model:
            raise ValidationError("Модель не может быть пустой", 'model', model)
        
        if not isinstance(model, str):
            raise ValidationError(
                f"Модель должна быть строкой, получен {type(model).__name__}",
                'model', model
            )
        
        model = model.strip()
        if len(model) < 1:
            raise ValidationError(
                "Модель должна содержать минимум 1 символ",
                'model', model
            )
        
        if len(model) > 50:
            raise ValidationError(
                "Модель не может быть длиннее 50 символов",
                'model', model
            )
        
        # Проверка на допустимые символы
        if not re.match(r'^[a-zA-Zа-яА-Я0-9\s\-\.]+$', model):
            raise ValidationError(
                "Модель может содержать только буквы, цифры, дефис, точку и пробелы",
                'model', model
            )
        
        return True
    
    @staticmethod
    def validate_year(year: Any) -> bool:
        """
        Проверка года выпуска
        
        Args:
            year: год для проверки
        
        Returns:
            True если корректно
        
        Raises:
            ValidationError: если год некорректен
        """
        if year is None:
            raise ValidationError("Год выпуска не может быть пустым", 'year', year)
        
        try:
            year = int(float(year))
        except (ValueError, TypeError):
            raise ValidationError(
                f"Год должен быть числом, получен {type(year).__name__}",
                'year', year
            )
        
        current_year = datetime.now().year
        min_year = 1900
        max_year = current_year + 1  # +1 для новых моделей следующего года
        
        if year < min_year or year > max_year:
            raise ValidationError(
                f"Год должен быть между {min_year} и {max_year}",
                'year', year
            )
        
        return True
    
    @staticmethod
    def validate_price(price: Any) -> bool:
        """
        Проверка цены
        
        Args:
            price: цена для проверки
        
        Returns:
            True если корректно
        
        Raises:
            ValidationError: если цена некорректна
        """
        if price is None:
            raise ValidationError("Цена не может быть пустой", 'price', price)
        
        try:
            price = float(price)
        except (ValueError, TypeError):
            raise ValidationError(
                f"Цена должна быть числом, получен {type(price).__name__}",
                'price', price
            )
        
        if price <= 0:
            raise ValidationError(
                "Цена должна быть положительной",
                'price', price
            )
        
        if price > 100_000_000:  # 100 миллионов
            raise ValidationError(
                "Цена не может превышать 100 000 000",
                'price', price
            )
        
        return True
    
    @staticmethod
    def validate_mileage(mileage: Any) -> bool:
        """
        Проверка пробега
        
        Args:
            mileage: пробег для проверки
        
        Returns:
            True если корректно
        
        Raises:
            ValidationError: если пробег некорректен
        """
        if mileage is None:
            return True  # пробег может быть не указан
        
        try:
            mileage = float(mileage)
        except (ValueError, TypeError):
            raise ValidationError(
                f"Пробег должен быть числом, получен {type(mileage).__name__}",
                'mileage', mileage
            )
        
        if mileage < 0:
            raise ValidationError(
                "Пробег не может быть отрицательным",
                'mileage', mileage
            )
        
        if mileage > 1_000_000:  # 1 миллион км
            raise ValidationError(
                "Пробег не может превышать 1 000 000 км",
                'mileage', mileage
            )
        
        return True
    
    @staticmethod
    def validate_vin(vin: Any) -> bool:
        """
        Проверка VIN номера
        
        Args:
            vin: VIN для проверки
        
        Returns:
            True если корректно
        
        Raises:
            ValidationError: если VIN некорректен
        """
        if not vin:
            return True  # VIN может быть не указан
        
        if not isinstance(vin, str):
            raise ValidationError(
                f"VIN должен быть строкой, получен {type(vin).__name__}",
                'vin', vin
            )
        
        vin = vin.strip().upper()
        
        # VIN должен содержать 17 символов
        if len(vin) != 17:
            raise ValidationError(
                "VIN должен содержать ровно 17 символов",
                'vin', vin
            )
        
        # Проверка на допустимые символы (буквы и цифры, кроме I, O, Q)
        if not re.match(r'^[A-HJ-NPR-Z0-9]{17}$', vin):
            raise ValidationError(
                "VIN может содержать только буквы (кроме I, O, Q) и цифры",
                'vin', vin
            )
        
        return True
    
    @staticmethod
    def validate_engine_type(engine_type: Any) -> bool:
        """
        Проверка типа двигателя
        
        Args:
            engine_type: тип двигателя
        
        Returns:
            True если корректно
        
        Raises:
            ValidationError: если тип некорректен
        """
        if not engine_type:
            return True
        
        if not isinstance(engine_type, str):
            raise ValidationError(
                f"Тип двигателя должен быть строкой, получен {type(engine_type).__name__}",
                'engine_type', engine_type
            )
        
        engine_type_lower = engine_type.lower()
        if engine_type_lower not in CarValidator.VALID_ENGINE_TYPES:
            raise ValidationError(
                f"Некорректный тип двигателя. Допустимые: {CarValidator.VALID_ENGINE_TYPES}",
                'engine_type', engine_type
            )
        
        return True
    
    @staticmethod
    def validate_transmission(transmission: Any) -> bool:
        """
        Проверка типа коробки передач
        
        Args:
            transmission: тип КПП
        
        Returns:
            True если корректно
        
        Raises:
            ValidationError: если тип некорректен
        """
        if not transmission:
            return True
        
        if not isinstance(transmission, str):
            raise ValidationError(
                f"Тип КПП должен быть строкой, получен {type(transmission).__name__}",
                'transmission', transmission
            )
        
        transmission_lower = transmission.lower()
        if transmission_lower not in CarValidator.VALID_TRANSMISSIONS:
            raise ValidationError(
                f"Некорректный тип КПП. Допустимые: {CarValidator.VALID_TRANSMISSIONS}",
                'transmission', transmission
            )
        
        return True
    
    @staticmethod
    def validate_drive(drive: Any) -> bool:
        """
        Проверка типа привода
        
        Args:
            drive: тип привода
        
        Returns:
            True если корректно
        
        Raises:
            ValidationError: если тип некорректен
        """
        if not drive:
            return True
        
        if not isinstance(drive, str):
            raise ValidationError(
                f"Тип привода должен быть строкой, получен {type(drive).__name__}",
                'drive', drive
            )
        
        drive_lower = drive.lower()
        if drive_lower not in CarValidator.VALID_DRIVES:
            raise ValidationError(
                f"Некорректный тип привода. Допустимые: {CarValidator.VALID_DRIVES}",
                'drive', drive
            )
        
        return True
    
    @staticmethod
    def validate_color(color: Any) -> bool:
        """
        Проверка цвета
        
        Args:
            color: цвет
        
        Returns:
            True если корректно
        
        Raises:
            ValidationError: если цвет некорректен
        """
        if not color:
            return True
        
        if not isinstance(color, str):
            raise ValidationError(
                f"Цвет должен быть строкой, получен {type(color).__name__}",
                'color', color
            )
        
        color_lower = color.lower()
        if color_lower not in CarValidator.VALID_COLORS:
            # В нестрогом режиме просто предупреждаем
            return True
        
        return True
    
    @staticmethod
    def validate_condition(condition: Any) -> bool:
        """
        Проверка состояния
        
        Args:
            condition: состояние
        
        Returns:
            True если корректно
        
        Raises:
            ValidationError: если состояние некорректно
        """
        if not condition:
            return True
        
        if not isinstance(condition, str):
            raise ValidationError(
                f"Состояние должно быть строкой, получен {type(condition).__name__}",
                'condition', condition
            )
        
        condition_lower = condition.lower()
        if condition_lower not in CarValidator.VALID_CONDITIONS:
            raise ValidationError(
                f"Некорректное состояние. Допустимые: {CarValidator.VALID_CONDITIONS}",
                'condition', condition
            )
        
        return True
    
    @staticmethod
    def validate_phone(phone: Any) -> bool:
        """
        Проверка номера телефона
        
        Args:
            phone: номер телефона
        
        Returns:
            True если корректно
        
        Raises:
            ValidationError: если номер некорректен
        """
        if not phone:
            return True
        
        if not isinstance(phone, str):
            raise ValidationError(
                f"Телефон должен быть строкой, получен {type(phone).__name__}",
                'phone', phone
            )
        
        # Удаляем все нецифровые символы
        digits = re.sub(r'\D', '', phone)
        
        if len(digits) < 10 or len(digits) > 15:
            raise ValidationError(
                "Телефон должен содержать 10-15 цифр",
                'phone', phone
            )
        
        return True
    
    @staticmethod
    def validate_email(email: Any) -> bool:
        """
        Проверка email адреса
        
        Args:
            email: email для проверки
        
        Returns:
            True если корректно
        
        Raises:
            ValidationError: если email некорректен
        """
        if not email:
            return True
        
        if not isinstance(email, str):
            raise ValidationError(
                f"Email должен быть строкой, получен {type(email).__name__}",
                'email', email
            )
        
        # Простая проверка формата email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValidationError(
                "Некорректный формат email",
                'email', email
            )
        
        return True
    
    def validate_car(self, car_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Полная валидация данных автомобиля
        
        Args:
            car_data: словарь с данными автомобиля
        
        Returns:
            Dict: валидированные и очищенные данные
        
        Raises:
            ValidationError: если данные некорректны
        """
        self.errors = []
        self.warnings = []
        
        # Копируем данные для обработки
        validated = car_data.copy()
        
        # Обязательные поля
        required_fields = ['brand', 'model', 'year', 'price']
        for field in required_fields:
            if field not in car_data or car_data[field] is None:
                if self.strict_mode:
                    raise ValidationError(
                        f"Отсутствует обязательное поле: {field}",
                        field
                    )
                else:
                    self.warnings.append(f"Отсутствует поле: {field}")
        
        # Валидация полей
        try:
            if 'brand' in car_data:
                self.validate_brand(car_data['brand'])
                validated['brand'] = str(car_data['brand']).strip()
        except ValidationError as e:
            self._handle_error(e)
        
        try:
            if 'model' in car_data:
                self.validate_model(car_data['model'])
                validated['model'] = str(car_data['model']).strip()
        except ValidationError as e:
            self._handle_error(e)
        
        try:
            if 'year' in car_data:
                self.validate_year(car_data['year'])
                validated['year'] = int(float(car_data['year']))
        except ValidationError as e:
            self._handle_error(e)
        
        try:
            if 'price' in car_data:
                self.validate_price(car_data['price'])
                validated['price'] = float(car_data['price'])
        except ValidationError as e:
            self._handle_error(e)
        
        try:
            if 'mileage' in car_data:
                self.validate_mileage(car_data['mileage'])
                if car_data['mileage']:
                    validated['mileage'] = float(car_data['mileage'])
        except ValidationError as e:
            self._handle_error(e)
        
        try:
            if 'vin' in car_data:
                self.validate_vin(car_data['vin'])
                if car_data['vin']:
                    validated['vin'] = str(car_data['vin']).strip().upper()
        except ValidationError as e:
            self._handle_error(e)
        
        try:
            if 'engine_type' in car_data:
                self.validate_engine_type(car_data['engine_type'])
        except ValidationError as e:
            self._handle_error(e)
        
        try:
            if 'transmission' in car_data:
                self.validate_transmission(car_data['transmission'])
        except ValidationError as e:
            self._handle_error(e)
        
        try:
            if 'drive' in car_data:
                self.validate_drive(car_data['drive'])
        except ValidationError as e:
            self._handle_error(e)
        
        try:
            if 'color' in car_data:
                self.validate_color(car_data['color'])
        except ValidationError as e:
            self._handle_error(e)
        
        try:
            if 'condition' in car_data:
                self.validate_condition(car_data['condition'])
        except ValidationError as e:
            self._handle_error(e)
        
        try:
            if 'phone' in car_data:
                self.validate_phone(car_data['phone'])
        except ValidationError as e:
            self._handle_error(e)
        
        try:
            if 'email' in car_data:
                self.validate_email(car_data['email'])
        except ValidationError as e:
            self._handle_error(e)
        
        # Если есть ошибки и включен строгий режим
        if self.errors and self.strict_mode:
            raise ValidationError(
                f"Ошибки валидации: {'; '.join(self.errors)}"
            )
        
        # Добавляем предупреждения в результат
        validated['_warnings'] = self.warnings
        validated['_errors'] = self.errors
        
        return validated
    
    def _handle_error(self, error: ValidationError) -> None:
        """Обработка ошибки валидации"""
        if self.strict_mode:
            raise error
        else:
            self.errors.append(str(error))


# Упрощенная функция для быстрой валидации
def validate_car_data(
    car_data: Dict[str, Any],
    strict: bool = False
) -> Dict[str, Any]:
    """
    Быстрая валидация данных автомобиля
    
    Args:
        car_data: словарь с данными автомобиля
        strict: строгий режим (выбрасывать исключения)
    
    Returns:
        Dict: валидированные данные
    
    Raises:
        ValidationError: если данные некорректны и strict=True
    
    Example:
        >>> data = {
        ...     'brand': 'Toyota',
        ...     'model': 'Camry',
        ...     'year': 2020,
        ...     'price': 1500000
        ... }
        >>> validated = validate_car_data(data)
        >>> print(validated['brand'])  # Toyota
    """
    validator = CarValidator(strict_mode=strict)
    return validator.validate_car(car_data)


def validate_car_batch(
    cars_data: List[Dict[str, Any]],
    strict: bool = False
) -> List[Dict[str, Any]]:
    """
    Валидация пакета автомобилей
    
    Args:
        cars_data: список словарей с данными
        strict: строгий режим
    
    Returns:
        List[Dict]: список валидированных данных
    """
    results = []
    
    for data in cars_data:
        try:
            validated = validate_car_data(data, strict)
            results.append(validated)
        except ValidationError as e:
            if strict:
                raise
            # В нестрогом режиме добавляем данные с ошибкой
            data['_validation_error'] = str(e)
            results.append(data)
    
    return results


def is_valid_car_data(car_data: Dict[str, Any]) -> bool:
    """
    Быстрая проверка данных без получения деталей
    
    Args:
        car_data: словарь с данными
    
    Returns:
        bool: True если данные корректны
    """
    try:
        validate_car_data(car_data, strict=True)
        return True
    except ValidationError:
        return False


def validate_required_fields(
    car_data: Dict[str, Any],
    required_fields: List[str] = None
) -> List[str]:
    """
    Проверка наличия обязательных полей
    
    Args:
        car_data: словарь с данными
        required_fields: список обязательных полей
    
    Returns:
        List[str]: список отсутствующих полей
    """
    if required_fields is None:
        required_fields = ['brand', 'model', 'year', 'price']
    
    missing = []
    for field in required_fields:
        if field not in car_data or car_data[field] is None:
            missing.append(field)
    
    return missing


def sanitize_car_data(car_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Очистка данных автомобиля (удаление пробелов, приведение типов)
    
    Args:
        car_data: исходные данные
    
    Returns:
        Dict: очищенные данные
    """
    cleaned = {}
    
    for key, value in car_data.items():
        if value is None:
            cleaned[key] = None
        elif isinstance(value, str):
            cleaned[key] = value.strip()
        else:
            cleaned[key] = value
    
    return cleaned


# Для обратной совместимости
__all__ = [
    'ValidationError',
    'CarValidator',
    'validate_car_data',
    'validate_car_batch',
    'is_valid_car_data',
    'validate_required_fields',
    'sanitize_car_data'
] 

