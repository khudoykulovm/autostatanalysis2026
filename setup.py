"""
Setup configuration for AutoStatAnalysis package
"""

from setuptools import setup, find_packages
import os

# Чтение README.md для long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Чтение requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    # Основная информация
    name="autostatanalysis",
    version="0.1.0",
    
    # Автор
    author="Murodjon",
    author_email="khudoykulov2003@gmail.com",
    
    # Описание
    description="Пакет для анализа автомобильных данных и расчета стоимости",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    # URL проекта
    url="https://github.com/Murodjon/autostatanalysis2026",
    project_urls={
        "Bug Tracker": "https://github.com/khudoykulovm/autostatanalysis2026/issues",
        "Documentation": "https://github.com/khudoykulovm/autostatanalysis2026#readme",
        "Source Code": "https://github.com/khudoykulovm/autostatanalysis2026",
    },
    
    # Лицензия
    license="MIT",
    
    # Поиск пакетов
    packages=find_packages(),
    
    # Зависимости
    install_requires=requirements,
    
    # Дополнительные зависимости (опционально)
    extras_require={
        'dev': [
            'pytest>=6.2.0',
            'pytest-cov>=2.12.0',
            'black>=21.5b0',
            'flake8>=3.9.0',
            'mypy>=0.812',
        ],
        'docs': [
            'sphinx>=4.0.0',
            'sphinx-rtd-theme>=0.5.2',
        ],
    },
    
    # Python версия
    python_requires=">=3.8",
    
    # Классификаторы (для PyPI)
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    
    # Ключевые слова
    keywords="automotive, car, analysis, statistics, price calculator, data analysis",
    
    # Включить все файлы из манифеста
    include_package_data=True,
    
    # Данные для включения в пакет
    package_data={
        "autostatanalysis": ["data/*.json", "py.typed"],
    },
    
    # Точки входа (если нужны консольные скрипты)
    entry_points={
        "console_scripts": [
            "autostat=autostatanalysis.cli:main",  # если будет CLI
        ],
    },
    
    # Zop безопасность
    zip_safe=False,
    
    # Тестовые требования
    test_suite="tests",
    tests_require=[
        "pytest>=6.2.0",
        "pytest-cov>=2.12.0",
    ],
) 



