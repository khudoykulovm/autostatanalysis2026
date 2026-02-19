from autostatanalysis.models.car import Car, CarStatus, CarFeature, CarPhoto, create_sample_car

# 1. Создание простого автомобиля
car1 = Car(
    brand="Toyota",
    model="Camry",
    year=2020,
    price=1500000,
    mileage=45000
)
print(car1)
print(f"Возраст: {car1.get_age()} лет")
print(f"Доступен: {car1.is_available()}")

# 2. Создание автомобиля со всеми полями
car2 = Car(
    brand="BMW",
    model="X5",
    year=2021,
    price=3500000,
    vin="WBA12345678901234",
    mileage=15000,
    color="Черный",
    engine_type="Дизель",
    transmission="Автомат",
    drive="Полный",
    condition="excellent",
    status=CarStatus.AVAILABLE,
    owner_name="Иванов Иван",
    owner_phone="+7 (999) 123-45-67"
)

# 3. Добавление характеристик
feature = CarFeature("Климат-контроль", "Комфорт", "2-зонный")
car2.add_feature(feature)

# 4. Добавление фотографий
photo = CarPhoto(
    url="https://example.com/photo1.jpg",
    is_main=True,
    description="Вид спереди"
)
car2.add_photo(photo)

# 5. Создание из словаря
data = {
    'brand': 'Honda',
    'model': 'CR-V',
    'year': 2019,
    'price': 1800000,
    'mileage': 60000
}
car3 = Car.from_dict(data)

# 6. Использование примера
sample_car = create_sample_car()
print(sample_car.get_features_dict())

# 7. Сериализация в JSON
json_str = car2.to_json()
print(json_str)

# 8. Работа со статусами
car2.status = CarStatus.SOLD
print(f"Статус: {car2.status}")  # "Продано"

# 9. Фильтрация характеристик
comfort_features = car2.get_features_by_category("Комфорт")
for f in comfort_features:
    print(f"  - {f}")

# 10. Сравнение автомобилей
car_a = Car("Toyota", "Camry", 2020, 1500000)
car_b = Car("Toyota", "Camry", 2020, 1500000)
print(car_a == car_b)  # True 

