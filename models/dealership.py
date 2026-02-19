 """
Модель автосалона для управления автопарком
============================================

Предоставляет классы для представления автосалона и связанных сущностей.

Основные классы:
    Dealership - основная модель автосалона
    DealershipEmployee - модель сотрудника
    DealershipCustomer - модель клиента
    DealershipTransaction - модель транзакции
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Any, Union
from enum import Enum
import json
import uuid

from .car import Car, CarStatus


class EmployeeRole(Enum):
    """Роли сотрудников автосалона"""
    
    MANAGER = "Менеджер"
    SALES = "Продавец"
    ACCOUNTANT = "Бухгалтер"
    TECHNICIAN = "Техник"
    DIRECTOR = "Директор"
    ADMIN = "Администратор"


class TransactionStatus(Enum):
    """Статусы транзакций"""
    
    PENDING = "Ожидает"
    COMPLETED = "Завершена"
    CANCELLED = "Отменена"
    REFUNDED = "Возврат"


class PaymentMethod(Enum):
    """Методы оплаты"""
    
    CASH = "Наличные"
    CARD = "Карта"
    CREDIT = "Кредит"
    LEASING = "Лизинг"
    TRADE_IN = "Trade-in"


@dataclass
class DealershipEmployee:
    """
    Сотрудник автосалона
    
    Attributes:
        employee_id: уникальный идентификатор
        name: ФИО
        role: роль
        phone: телефон
        email: email
        hire_date: дата найма
        salary: зарплата
        is_active: активен ли
    """
    
    name: str
    role: EmployeeRole
    phone: str = ''
    email: str = ''
    hire_date: datetime = field(default_factory=datetime.now)
    salary: float = 0
    is_active: bool = True
    employee_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    
    def __str__(self) -> str:
        return f"{self.name} ({self.role.value})"
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь"""
        return {
            'employee_id': self.employee_id,
            'name': self.name,
            'role': self.role.value,
            'phone': self.phone,
            'email': self.email,
            'hire_date': self.hire_date.isoformat(),
            'salary': self.salary,
            'is_active': self.is_active
        }


@dataclass
class DealershipCustomer:
    """
    Клиент автосалона
    
    Attributes:
        customer_id: уникальный идентификатор
        name: ФИО
        phone: телефон
        email: email
        address: адрес
        registered_at: дата регистрации
        is_regular: постоянный клиент
        notes: заметки
    """
    
    name: str
    phone: str = ''
    email: str = ''
    address: str = ''
    registered_at: datetime = field(default_factory=datetime.now)
    is_regular: bool = False
    notes: str = ''
    customer_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    
    def __str__(self) -> str:
        return f"{self.name} ({self.phone})"
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь"""
        return {
            'customer_id': self.customer_id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'registered_at': self.registered_at.isoformat(),
            'is_regular': self.is_regular,
            'notes': self.notes
        }


@dataclass
class DealershipTransaction:
    """
    Транзакция продажи/покупки
    
    Attributes:
        transaction_id: уникальный идентификатор
        car: проданный/купленный автомобиль
        customer: клиент
        employee: сотрудник
        price: цена сделки
        payment_method: метод оплаты
        status: статус
        date: дата сделки
        notes: заметки
    """
    
    car: Car
    customer: DealershipCustomer
    employee: DealershipEmployee
    price: float
    payment_method: PaymentMethod
    status: TransactionStatus = TransactionStatus.PENDING
    date: datetime = field(default_factory=datetime.now)
    notes: str = ''
    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    
    def __str__(self) -> str:
        return (
            f"Сделка #{self.transaction_id}: {self.car.brand} {self.car.model} - "
            f"{self.price:,.0f} ₽ [{self.status.value}]"
        )
    
    def complete(self) -> None:
        """Завершить сделку"""
        self.status = TransactionStatus.COMPLETED
        self.car.status = CarStatus.SOLD
    
    def cancel(self) -> None:
        """Отменить сделку"""
        self.status = TransactionStatus.CANCELLED
        self.car.status = CarStatus.AVAILABLE
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь"""
        return {
            'transaction_id': self.transaction_id,
            'car': self.car.to_dict(),
            'customer': self.customer.to_dict(),
            'employee': self.employee.to_dict(),
            'price': self.price,
            'payment_method': self.payment_method.value,
            'status': self.status.value,
            'date': self.date.isoformat(),
            'notes': self.notes
        }


@dataclass
class Dealership:
    """
    Модель автосалона
    
    Управляет автопарком, сотрудниками, клиентами и транзакциями.
    
    Attributes:
        name: название автосалона
        address: адрес
        phone: телефон
        email: email
        website: веб-сайт
        cars: список автомобилей
        employees: список сотрудников
        customers: список клиентов
        transactions: список транзакций
        created_at: дата создания
        updated_at: дата обновления
    
    Example:
        >>> dealership = Dealership("Автосалон №1", "ул. Ленина, 1", "+7 (999) 123-45-67")
        >>> car = Car("Toyota", "Camry", 2020, 1500000)
        >>> dealership.add_car(car)
        >>> print(dealership.get_statistics())
    """
    
    name: str
    address: str = ''
    phone: str = ''
    email: str = ''
    website: str = ''
    
    # Коллекции
    cars: List[Car] = field(default_factory=list)
    employees: List[DealershipEmployee] = field(default_factory=list)
    customers: List[DealershipCustomer] = field(default_factory=list)
    transactions: List[DealershipTransaction] = field(default_factory=list)
    
    # Метаданные
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    dealership_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    
    def __str__(self) -> str:
        """Строковое представление"""
        return (
            f"🏢 {self.name}\n"
            f"📍 {self.address}\n"
            f"📞 {self.phone}\n"
            f"🚗 Автомобилей: {len(self.cars)}"
        )
    
    # ===== Методы для работы с автомобилями =====
    
    def add_car(self, car: Car) -> None:
        """
        Добавить автомобиль в автопарк
        
        Args:
            car: автомобиль для добавления
        """
        self.cars.append(car)
        self.updated_at = datetime.now()
    
    def add_cars(self, cars: List[Car]) -> None:
        """
        Добавить несколько автомобилей
        
        Args:
            cars: список автомобилей
        """
        self.cars.extend(cars)
        self.updated_at = datetime.now()
    
    def remove_car(self, car: Union[Car, str]) -> Optional[Car]:
        """
        Удалить автомобиль из автопарка
        
        Args:
            car: автомобиль или VIN для удаления
        
        Returns:
            Optional[Car]: удаленный автомобиль или None
        """
        if isinstance(car, str):
            # Поиск по VIN
            for i, c in enumerate(self.cars):
                if c.vin == car:
                    return self.cars.pop(i)
        else:
            # Поиск по объекту
            for i, c in enumerate(self.cars):
                if c == car:
                    return self.cars.pop(i)
        
        self.updated_at = datetime.now()
        return None
    
    def get_car_by_vin(self, vin: str) -> Optional[Car]:
        """
        Получить автомобиль по VIN
        
        Args:
            vin: VIN номер
        
        Returns:
            Optional[Car]: найденный автомобиль или None
        """
        for car in self.cars:
            if car.vin == vin:
                return car
        return None
    
    def get_available_cars(self) -> List[Car]:
        """
        Получить доступные для продажи автомобили
        
        Returns:
            List[Car]: список доступных автомобилей
        """
        return [c for c in self.cars if c.is_available()]
    
    def get_sold_cars(self) -> List[Car]:
        """
        Получить проданные автомобили
        
        Returns:
            List[Car]: список проданных автомобилей
        """
        return [c for c in self.cars if c.status == CarStatus.SOLD]
    
    def get_cars_by_brand(self, brand: str) -> List[Car]:
        """
        Получить автомобили по марке
        
        Args:
            brand: марка для фильтрации
        
        Returns:
            List[Car]: отфильтрованный список
        """
        return [c for c in self.cars if c.brand.lower() == brand.lower()]
    
    def get_cars_by_year_range(self, min_year: int, max_year: int) -> List[Car]:
        """
        Получить автомобили в диапазоне годов
        
        Args:
            min_year: минимальный год
            max_year: максимальный год
        
        Returns:
            List[Car]: отфильтрованный список
        """
        return [c for c in self.cars if min_year <= c.year <= max_year]
    
    def get_cars_by_price_range(self, min_price: float, max_price: float) -> List[Car]:
        """
        Получить автомобили в диапазоне цен
        
        Args:
            min_price: минимальная цена
            max_price: максимальная цена
        
        Returns:
            List[Car]: отфильтрованный список
        """
        return [c for c in self.cars if min_price <= c.price <= max_price]
    
    # ===== Методы для работы с сотрудниками =====
    
    def add_employee(self, employee: DealershipEmployee) -> None:
        """
        Добавить сотрудника
        
        Args:
            employee: сотрудник для добавления
        """
        self.employees.append(employee)
        self.updated_at = datetime.now()
    
    def remove_employee(self, employee_id: str) -> Optional[DealershipEmployee]:
        """
        Удалить сотрудника по ID
        
        Args:
            employee_id: ID сотрудника
        
        Returns:
            Optional[DealershipEmployee]: удаленный сотрудник
        """
        for i, emp in enumerate(self.employees):
            if emp.employee_id == employee_id:
                return self.employees.pop(i)
        return None
    
    def get_employees_by_role(self, role: EmployeeRole) -> List[DealershipEmployee]:
        """
        Получить сотрудников по роли
        
        Args:
            role: роль для фильтрации
        
        Returns:
            List[DealershipEmployee]: отфильтрованный список
        """
        return [e for e in self.employees if e.role == role]
    
    def get_active_employees(self) -> List[DealershipEmployee]:
        """
        Получить активных сотрудников
        
        Returns:
            List[DealershipEmployee]: список активных сотрудников
        """
        return [e for e in self.employees if e.is_active]
    
    # ===== Методы для работы с клиентами =====
    
    def add_customer(self, customer: DealershipCustomer) -> None:
        """
        Добавить клиента
        
        Args:
            customer: клиент для добавления
        """
        self.customers.append(customer)
        self.updated_at = datetime.now()
    
    def get_customer_by_id(self, customer_id: str) -> Optional[DealershipCustomer]:
        """
        Получить клиента по ID
        
        Args:
            customer_id: ID клиента
        
        Returns:
            Optional[DealershipCustomer]: найденный клиент
        """
        for customer in self.customers:
            if customer.customer_id == customer_id:
                return customer
        return None
    
    def search_customers(self, query: str) -> List[DealershipCustomer]:
        """
        Поиск клиентов по имени или телефону
        
        Args:
            query: поисковый запрос
        
        Returns:
            List[DealershipCustomer]: результаты поиска
        """
        query = query.lower()
        results = []
        
        for customer in self.customers:
            if (query in customer.name.lower() or 
                query in customer.phone.lower() or
                query in customer.email.lower()):
                results.append(customer)
        
        return results
    
    def get_regular_customers(self) -> List[DealershipCustomer]:
        """
        Получить постоянных клиентов
        
        Returns:
            List[DealershipCustomer]: список постоянных клиентов
        """
        return [c for c in self.customers if c.is_regular]
    
    # ===== Методы для работы с транзакциями =====
    
    def create_transaction(
        self,
        car: Car,
        customer: DealershipCustomer,
        employee: DealershipEmployee,
        price: float,
        payment_method: PaymentMethod,
        notes: str = ''
    ) -> DealershipTransaction:
        """
        Создать новую транзакцию
        
        Args:
            car: продаваемый автомобиль
            customer: покупатель
            employee: сотрудник
            price: цена сделки
            payment_method: метод оплаты
            notes: заметки
        
        Returns:
            DealershipTransaction: созданная транзакция
        
        Raises:
            ValueError: если автомобиль не доступен
        """
        if not car.is_available():
            raise ValueError(f"Автомобиль {car} недоступен для продажи")
        
        transaction = DealershipTransaction(
            car=car,
            customer=customer,
            employee=employee,
            price=price,
            payment_method=payment_method,
            notes=notes
        )
        
        self.transactions.append(transaction)
        car.status = CarStatus.RESERVED
        self.updated_at = datetime.now()
        
        return transaction
    
    def complete_transaction(self, transaction_id: str) -> bool:
        """
        Завершить транзакцию
        
        Args:
            transaction_id: ID транзакции
        
        Returns:
            bool: True если успешно
        """
        for transaction in self.transactions:
            if transaction.transaction_id == transaction_id:
                transaction.complete()
                self.updated_at = datetime.now()
                return True
        return False
    
    def cancel_transaction(self, transaction_id: str) -> bool:
        """
        Отменить транзакцию
        
        Args:
            transaction_id: ID транзакции
        
        Returns:
            bool: True если успешно
        """
        for transaction in self.transactions:
            if transaction.transaction_id == transaction_id:
                transaction.cancel()
                self.updated_at = datetime.now()
                return True
        return False
    
    def get_transactions_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[DealershipTransaction]:
        """
        Получить транзакции за период
        
        Args:
            start_date: начальная дата
            end_date: конечная дата
        
        Returns:
            List[DealershipTransaction]: транзакции за период
        """
        return [
            t for t in self.transactions
            if start_date <= t.date <= end_date
        ]
    
    def get_transactions_by_customer(
        self,
        customer: Union[DealershipCustomer, str]
    ) -> List[DealershipTransaction]:
        """
        Получить транзакции клиента
        
        Args:
            customer: клиент или его ID
        
        Returns:
            List[DealershipTransaction]: транзакции клиента
        """
        customer_id = customer if isinstance(customer, str) else customer.customer_id
        
        return [
            t for t in self.transactions
            if t.customer.customer_id == customer_id
        ]
    
    def get_transactions_by_employee(
        self,
        employee: Union[DealershipEmployee, str]
    ) -> List[DealershipTransaction]:
        """
        Получить транзакции сотрудника
        
        Args:
            employee: сотрудник или его ID
        
        Returns:
            List[DealershipTransaction]: транзакции сотрудника
        """
        employee_id = employee if isinstance(employee, str) else employee.employee_id
        
        return [
            t for t in self.transactions
            if t.employee.employee_id == employee_id
        ]
    
    # ===== Статистика и аналитика =====
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Получить полную статистику автосалона
        
        Returns:
            Dict: словарь со статистикой
        """
        available_cars = self.get_available_cars()
        sold_cars = self.get_sold_cars()
        completed_transactions = [
            t for t in self.transactions
            if t.status == TransactionStatus.COMPLETED
        ]
        
        total_revenue = sum(t.price for t in completed_transactions)
        avg_price = total_revenue / len(completed_transactions) if completed_transactions else 0
        
        # Статистика по маркам
        brands = {}
        for car in self.cars:
            brands[car.brand] = brands.get(car.brand, 0) + 1
        
        # Статистика по сотрудникам
        employee_stats = {}
        for emp in self.employees:
            emp_transactions = self.get_transactions_by_employee(emp)
            employee_stats[emp.name] = {
                'count': len(emp_transactions),
                'revenue': sum(t.price for t in emp_transactions)
            }
        
        return {
            'dealership': {
                'name': self.name,
                'id': self.dealership_id,
                'created_at': self.created_at.isoformat()
            },
            'cars': {
                'total': len(self.cars),
                'available': len(available_cars),
                'sold': len(sold_cars),
                'by_brand': brands,
                'total_value': sum(c.price for c in self.cars),
                'available_value': sum(c.price for c in available_cars)
            },
            'employees': {
                'total': len(self.employees),
                'active': len(self.get_active_employees())
            },
            'customers': {
                'total': len(self.customers),
                'regular': len(self.get_regular_customers())
            },
            'transactions': {
                'total': len(self.transactions),
                'completed': len(completed_transactions),
                'pending': len([t for t in self.transactions if t.status == TransactionStatus.PENDING]),
                'total_revenue': total_revenue,
                'average_price': avg_price
            },
            'employee_stats': employee_stats,
            'updated_at': self.updated_at.isoformat()
        }
    
    def get_sales_report(self, year: Optional[int] = None) -> Dict[str, Any]:
        """
        Получить отчет по продажам
        
        Args:
            year: год для отчета (если None - текущий)
        
        Returns:
            Dict: отчет по продажам
        """
        if year is None:
            year = datetime.now().year
        
        # Фильтруем транзакции за указанный год
        year_transactions = [
            t for t in self.transactions
            if t.date.year == year and t.status == TransactionStatus.COMPLETED
        ]
        
        # По месяцам
        monthly = {i: 0 for i in range(1, 13)}
        for t in year_transactions:
            monthly[t.date.month] += 1
        
        # По маркам
        by_brand = {}
        for t in year_transactions:
            by_brand[t.car.brand] = by_brand.get(t.car.brand, 0) + 1
        
        return {
            'year': year,
            'total_sales': len(year_transactions),
            'total_revenue': sum(t.price for t in year_transactions),
            'average_price': sum(t.price for t in year_transactions) / len(year_transactions) if year_transactions else 0,
            'by_month': monthly,
            'by_brand': by_brand,
            'best_month': max(monthly, key=monthly.get) if any(monthly.values()) else None,
            'best_brand': max(by_brand, key=by_brand.get) if by_brand else None
        }
    
    def get_inventory_value(self) -> Dict[str, float]:
        """
        Получить стоимость автопарка
        
        Returns:
            Dict: стоимость по категориям
        """
        total = sum(c.price for c in self.cars)
        available = sum(c.price for c in self.get_available_cars())
        sold = sum(c.price for c in self.get_sold_cars())
        
        return {
            'total': total,
            'available': available,
            'sold': sold,
            'available_percent': (available / total * 100) if total else 0
        }
    
    # ===== Сериализация =====
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразовать в словарь
        
        Returns:
            Dict: словарь с данными автосалона
        """
        return {
            'dealership_id': self.dealership_id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'website': self.website,
            'cars': [c.to_dict() for c in self.cars],
            'employees': [e.to_dict() for e in self.employees],
            'customers': [c.to_dict() for c in self.customers],
            'transactions': [t.to_dict() for t in self.transactions],
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
    def from_dict(cls, data: Dict[str, Any]) -> 'Dealership':
        """
        Создать объект из словаря
        
        Args:
            data: словарь с данными
        
        Returns:
            Dealership: созданный автосалон
        """
        from .car import Car
        from .dealership import DealershipEmployee, DealershipCustomer, DealershipTransaction
        
        # Создаем базовый объект
        dealership_data = {k: v for k, v in data.items() 
                          if k not in ['cars', 'employees', 'customers', 'transactions']}
        
        dealership = cls(**dealership_data)
        
        # Загружаем автомобили
        if 'cars' in data:
            for car_data in data['cars']:
                dealership.cars.append(Car.from_dict(car_data))
        
        # Загружаем сотрудников
        if 'employees' in data:
            for emp_data in data['employees']:
                if 'role' in emp_data:
                    emp_data['role'] = EmployeeRole(emp_data['role'])
                if 'hire_date' in emp_data and isinstance(emp_data['hire_date'], str):
                    emp_data['hire_date'] = datetime.fromisoformat(emp_data['hire_date'])
                dealership.employees.append(DealershipEmployee(**emp_data))
        
        # Загружаем клиентов
        if 'customers' in data:
            for cust_data in data['customers']:
                if 'registered_at' in cust_data and isinstance(cust_data['registered_at'], str):
                    cust_data['registered_at'] = datetime.fromisoformat(cust_data['registered_at'])
                dealership.customers.append(DealershipCustomer(**cust_data))
        
        # Загружаем транзакции (упрощенно)
        if 'transactions' in data:
            for trans_data in data['transactions']:
                # Здесь нужна более сложная логика восстановления связей
                pass
        
        return dealership


def create_sample_dealership() -> Dealership:
    """
    Создать пример автосалона с тестовыми данными
    
    Returns:
        Dealership: пример автосалона
    """
    from .car import create_sample_car
    
    dealership = Dealership(
        name="Автосалон 'Премиум'",
        address="г. Москва, ул. Ленина, д. 1",
        phone="+7 (495) 123-45-67",
        email="info@premium-auto.ru",
        website="www.premium-auto.ru"
    )
    
    # Добавляем сотрудников
    dealership.add_employee(DealershipEmployee(
        name="Иванов Иван Иванович",
        role=EmployeeRole.DIRECTOR,
        phone="+7 (999) 111-22-33",
        salary=150000
    ))
    
    dealership.add_employee(DealershipEmployee(
        name="Петров Петр Петрович",
        role=EmployeeRole.SALES,
        phone="+7 (999) 444-55-66",
        salary=80000
    ))
    
    # Добавляем клиентов
    dealership.add_customer(DealershipCustomer(
        name="Сидоров Алексей",
        phone="+7 (999) 777-88-99",
        email="alex@mail.ru",
        is_regular=True
    ))
    
    # Добавляем автомобили
    for i in range(3):
        dealership.add_car(create_sample_car())
    
    return dealership


# Для обратной совместимости
__all__ = [
    'EmployeeRole',
    'TransactionStatus',
    'PaymentMethod',
    'DealershipEmployee',
    'DealershipCustomer',
    'DealershipTransaction',
    'Dealership',
    'create_sample_dealership'
]
