[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/kOqwghv0)
# ML Project — [Название проекта]

**Студент:** Детина Степан Ильич

**Группа:** БИВ235


## Оглавление

1. [Описание задачи](#описание-задачи)
2. [Структура репозитория](#структура-репозитория)
3. [Запуски](#быстрый-старт)
4. [Данные](#данные)
5. [Результаты](#результаты)
7. [Отчёт](#отчёт)


## Описание задачи

**Задача:**
Обучение с учителем: бинарная классификация (Binary Classification).

**Датасет:** [Digital Payment Fraud Detection Benchmark на Kaggle](https://www.kaggle.com/datasets/rohit8527kmr7518/digital-payment-fraud-detection-benchmark/data)

**Целевая метрика:** `PR-AUC` и `F1-score`. 
*Обоснование:* В задаче присутствует сильный дисбаланс классов (фрода всего ~1.6%). Использовать Accuracy нельзя. PR-AUC и F1-score фокусируются на качестве распознавания именно миноритарного (мошеннического) класса.

**Датасет:** [Digital Payment Fraud Detection Benchmark на Kaggle](https://www.kaggle.com/datasets/rohit8527kmr7518/digital-payment-fraud-detection-benchmark/data)

## Структура репозитория
```
├── data
│   ├── processed               # Очищенные и обработанные данные
│   └── raw                     # Исходные файлы
├── models                      # Сохранённые модели (.pkl)
├── notebooks
│   ├── 01_eda.ipynb            # EDA, очистка, Feature Engineering, сплит
│   ├── 02_baseline.ipynb       # Baseline-модель (LogReg)
│   └── 03_experiments.ipynb    # Эксперименты, тюнинг, PCA
├── presentation                # Презентация для защиты
├── report
│   ├── images                  # Изображения для отчёта
│   └── report.md               # Финальный отчёт
├── src
│   ├── preprocessing.py        # Предобработка данных
│   └── modeling.py             # Обучение и оценка моделей
├── tests
│   └── test.py                 # Тесты пайплайна
├── requirements.txt            # Зависимости проекта
├── ruff.toml                   # Конфиг линтера Ruff
├── Dockerfile                  # Инструкции для сборки образа
├── docker-compose.yml          # Запуск контейнера
└── README.md
```

## Запуск

```bash
# 1. Клонировать репозиторий
git clone <url>
cd <repo-name>

# 2. Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# 3. Установить зависимости
pip install -r requirements.txt
```

Альтернативно:
```bash
# 1. Запуск сборки и старт контейнера
docker-compose up --build

# 2. Откройте в браузере http://localhost:8888 
# Пароль для доступа: fraudproject
```

## Данные
- `data/raw/` — исходные файлы
- `data/processed/` — предобработанные данные


## Результаты
| Модель | PR-AUC | ROC-AUC | F1-Score | Precision | Recall |
|--------|--------|---------|----------|-----------|--------|
| Baseline (LogReg) | **0.2834** | **0.8409** | 0.1175 | 0.0636 | **0.7690** |
| HistGradientBoosting | 0.2549 | 0.8289 | 0.1980 | 0.1169 | 0.6486 |
| Random Forest (Tuned) | 0.2018 | 0.8213 | **0.2407** | **0.1532** | 0.5615 |

**Обоснование финальной модели:** 
Несмотря на лидерство Baseline по метрике PR-AUC, линейная модель имеет неприемлемо низкий Precision (6%). В качестве финальной бизнес-модели выбран **Random Forest (Tuned)**. Эта модель лучше всех справилась с балансом классов: она имеет наивысший F1-score (0.24) и лучший Precision (15.3%), что позволит блокировать мошенников, минимизируя негатив от честных клиентов (False Positives).


## Отчёт

Финальный отчёт: [`report/report.md`](report/report.md)
