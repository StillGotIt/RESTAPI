# Тестовое задание "Создание REST API приложения"

## Описание

Необходимо реализовать REST API приложение для справочника Организаций, Зданий и Деятельности.

### Сущности

1. **Организация**:
    - Название: Например, ООО “Рога и Копыта”.
    - Номер телефона: Организация может иметь несколько номеров телефонов (например, 2-222-222, 3-333-333,
      8-923-666-13-13).
    - Здание: Организация должна находиться в одном конкретном здании (например, Блюхера, 32/1).
    - Деятельность: Организация может заниматься несколькими видами деятельности (например, “Молочная продукция”,
      “Мясная продукция”).

2. **Здание**:
    - Адрес: Например, г. Москва, ул. Ленина 1, офис 3.
    - Географические координаты: Местоположение здания должно быть в виде широты и долготы.

3. **Деятельность**:
    - Название: Например, “Еда”, “Автомобили”.
    - Иерархия: Деятельность может быть вложенной. Пример дерева:
        - Еда
            - Мясная продукция
            - Молочная продукция
        - Автомобили
            - Грузовые
            - Легковые
                - Запчасти
                - Аксессуары

### Функционал приложения

Взаимодействие с пользователем происходит посредством HTTP-запросов к API серверу с использованием статического API
ключа. Все ответы должны быть в формате JSON. Необходимо реализовать следующие методы:

- **Список всех организаций, находящихся в конкретном здании**.
- **Список всех организаций, которые относятся к указанному виду деятельности**.
- **Список организаций, которые находятся в заданном радиусе/прямоугольной области относительно указанной точки на карте
  **.
- **Вывод информации об организации по её идентификатору**.
- **Поиск организаций по виду деятельности**. Например, поиск по виду деятельности «Еда», которая находится на первом
  уровне дерева, и чтобы нашлись все организации, которые относятся к видам деятельности, лежащим внутри. Т.е. в
  результатах поиска должны отобразиться организации с видом деятельности Еда, Мясная продукция, Молочная продукция.
- **Поиск организации по названию**.
- **Ограничить уровень вложенности деятельностей 3 уровнями**.

## API Endpoints

### Organizations

#### Get Organizations

- **URL**: `/api/organizations/`
- **Method**: `GET`
- **Description**: Возвращает список организаций на основе заданных параметров.
- **Query Parameters**:
    - `api_key` (required): Апи ключ для возможности делать запросы. Пример: `api_key_1234234jkasd`.
    - `name` (optional): Название организации. Пример: `Microsoft`.
    - `id` (optional): Идентификатор организации. Пример: `111`.
- **Response**: Возвращает объект `FullOutOrganizationSchema` или `None`, если организация не найдена.

#### Get Organizations by Activity

- **URL**: `/api/organizations/activities/`
- **Method**: `GET`
- **Description**: Возвращает список организаций, связанных с определенной деятельностью. Если `is_parent` установлен
  в `True`, возвращает организации, связанные с родительской деятельностью и всеми её дочерними элементами.
- **Query Parameters**:
    - `api_key` (required): Апи ключ для возможности делать запросы. Пример: `api_key_1234234jkasd`.
    - `id` (optional): Идентификатор деятельности. Пример: `123`.
    - `is_parent` (optional): Флаг, указывающий, является ли деятельность родительской. По умолчанию `False`(если
      поставлен в True, начинает искать дочерние виды деятельности на 3 в глубь и возвращает организации которые
      соотносятся с этими видами деятельности).
    - `name` (optional): Название деятельности. Пример: `Cleaning`.
- **Response**: Возвращает список организаций или `None`, если организации не найдены.

#### Get Organizations by Building

- **URL**: `/api/organizations/buildings/`
- **Method**: `GET`
- **Description**: Возвращает список организаций, связанных с определенным зданием или находящихся в заданном радиусе от
  указанных координат.
- **Query Parameters**:
    - `api_key` (required): Апи ключ для возможности делать запросы. Пример: `api_key_1234234jkasd`.
    - `id` (optional): Идентификатор здания. Пример: `456`.
    - `longitude` (optional): Долгота для поиска организаций в радиусе. Пример: `23.123`.
    - `latitude` (optional): Широта для поиска организаций в радиусе. Пример: `-23.12356`.
    - `radius_km` (optional): Радиус поиска в километрах. По умолчанию `1`. Пример: `1.1`.
- **Response**: Возвращает список организаций или `None`, если организации не найдены.

### Технологический стек

- **FastAPI**: Для создания REST API.
- **Pydantic**: Для валидации данных.
- **SQLAlchemy**: Для работы с базой данных.
- **Alembic**: Для управления миграциями базы данных.
- **PostgreSQL**: В качестве базы данных.
- **Docker**: Для контейнеризации приложения.

---

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### 2. Создать и заполнить .env по примеру .env_example

```POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db_name
POSTGRES_PORT=5432
```

### 3. Запустить проект через докер

```docker compose up --build -d```

### 3. Заполнить тестовыми данными

```docker-compose exec rest_api_app```

```python fill_db.py```
