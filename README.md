## 🔧 Требования
Python 3.8 или выше

pandas >= 1.3.0

numpy >= 1.21.0

## 📝 Лицензия
Этот проект распространяется под лицензией MIT. Подробности в файле LICENSE.

## 👤 Автор
Murodjon

GitHub: @khudoykulovm

Email: khudoykulov2003@gmail.com

# 🚗 AutoStatAnalysis 

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-0.1.0-orange)

**AutoStatAnalysis** — это Python пакет для анализа автомобильных данных, расчета стоимости автомобилей и статистической обработки информации об автотранспорте.

## 📋 Оглавление
- [Возможности](#-возможности)
- [Установка](#-установка)
- [Быстрый старт](#-быстрый-старт)
- [Структура проекта](#-структура-проекта)
- [Требования](#-требования)
- [Лицензия](#-лицензия)
- [Автор](#-автор)

## ✨ Возможности

- ✅ **Расчет рыночной стоимости** автомобилей с учетом возраста, пробега и состояния
- ✅ **Статистический анализ** автопарка
- ✅ **Модели данных** для автомобилей и автосалонов
- ✅ **Валидация** вводимых данных
- ✅ **Форматирование** цен и вывод отчетов
- ✅ **Генерация** тестовых данных

## 📦 Установка

### Через pip (после публикации)
```bash
pip install autostatanalysis

## Установка из репозитория
git clone https://github.com/khudoykulovm/autostatanalysis2026.git
cd autostatanalysis2026
pip install -e .

## 🚀 Быстрый старт
from autostatanalysis.models.car import Car
from autostatanalysis.core.calculator import CarPriceCalculator
from autostatanalysis.utils.formatter import format_price

## Создание автомобиля
car = Car(
    brand="Toyota",
    model="Camry",
    year=2020,
    price=1500000,
    mileage=50000
)

print(car)  # 🚗 Toyota Camry (2020)

# Расчет стоимости
calculator = CarPriceCalculator(
    base_price=1500000,
    year=2020,
    mileage=50000,
    condition="good"
)

result = calculator.calculate_market_price()
print(f"Рыночная стоимость: {format_price(result['market_price'])}")

# 📁 Структура проекта
autostatanalysis2026/
├── 📄 README.md              # Документация
├── 📄 setup.py                # Настройки пакета
├── 📄 requirements.txt        # Зависимости
├── 📄 LICENSE                 # Лицензия
├── 📄 .gitignore              # Игнорируемые файлы
└── 📁 autostatanalysis/       # Основной пакет
    ├── 📄 __init__.py
    ├── 📁 core/               # Ядро
    │   ├── calculator.py      # Калькулятор цен
    │   ├── filters.py         # Фильтры
    │   └── validator.py       # Валидация
    ├── 📁 models/              # Модели данных
    │   ├── car.py             # Автомобиль
    │   └── dealership.py      # Автосалон
    ├── 📁 utils/               # Утилиты
    │   ├── file_handler.py    # Работа с файлами
    │   ├── formatter.py       # Форматирование
    │   └── statistics.py      # Статистика
    ├── 📁 data/                # Данные
        └── sample_data.py     # Примеры данных

# ⭐ Поддержка проекта
Если вам нравится этот проект, поставьте звездочку на GitHub! Это помогает другим разработчикам найти его.


