# ✅ Урок 44: Пошук, фільтрація та видалення фільмів.

---
<img src="main_image.png" alt="pygame" width="1500">

## Зміст уроку:

1. [Сьогодні на уроці](#1-сьогодні-на-уроці)
2. [Реалізація команди `/search_film`](#2-реалізація-команди-search_film)
3. [Реалізація команди `/filter_films`](#3-реалізація-команди-filter_films)
4. [Реалізація команди `/delete_film`](#4-реалізація-команди-delete_film)
5. [Реалізація команди `/edit_film`](#5-реалізація-команди-edit_film)
6. [Реалізація команди `/recommend_film`](#6-реалізація-команди-recommend_film)
7. [Підведення підсумків 🚀](#7-підведення-підсумків-)
8. [Домашнє завдання 🏠](#8-домашнє-завдання-)

---

## 1. Сьогодні на уроці

> 💡 На цьому уроці ми розглянемо наступні теми:

- Реалізуємо функції **пошуку** та **фільтрації** фільмів за різними критеріями.
- Реалізуємо функції **видалення** та **редагування** фільмів.

**Пошук, фільтрація, видалення та редагування інформації** - це основні функції, які використовуються в будь-якій **базі
даних** чи **інформаційній системі**.

- Функції дозволяють ефективно обробляти великі обсяги інформації та робити додатки зручнішими для користувачів.
- Можливість **фільтрувати** фільми за жанром чи роком допоможе швидко знайти потрібну інформацію, а **видалення** або
  **редагування** даних дозволяє підтримувати актуальність бібліотеки.
- Подібні функції використовуються в онлайн-магазинах та пошукових системах.

> На попередніх уроках ми створили базовий функціонал для **перегляду** та **додавання** фільмів до списку.

Сьогодні ми продовжимо розширювати можливості нашого **TelegramBot**, додамо функції **пошуку**, **фільтрації**,
**видалення** та **редагування** фільмів, що дозволить користувачам легко **знаходити** потрібні фільми, **видаляти**
непотрібні записи та **оновлювати** інформацію, коли це необхідно.

[Повернутися до змісту](#зміст-уроку)

---

## 2. Реалізація команди `/search_film`

Реалізуємо команду `search_film` для пошуку фільму за назвою.

Необхідно оновити код в файлі `commands.py`:

```python
# Old code
from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

START_COMMAND = Command('start')
FILMS_COMMAND = Command('films')
FILM_CREATE_COMMAND = Command("create_film")

BOT_COMMANDS = [
    BotCommand(command="start", description="Почати розмову"),
    BotCommand(command="films", description="Перегляд списку фільмів"),
    BotCommand(command="create_film", description="Додати новий фільм"),
]
```

```python
# New code
from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

START_COMMAND = Command('start')
FILMS_COMMAND = Command('films')
FILM_CREATE_COMMAND = Command("create_film")
FILM_SEARCH_COMMAND = Command("search_film")

BOT_COMMANDS = [
    BotCommand(command="start", description="Почати розмову"),
    BotCommand(command="films", description="Перегляд списку фільмів"),
    BotCommand(command="create_film", description="Додати новий фільм"),
    BotCommand(command="search_film", description="Пошук фільму за назвою"),
]
``` 

Необхідно додати класс `FilmStates()` в модуль `bot.py`:

```python
class FilmStates(StatesGroup):
    search_query = State()
    filter_criteria = State()
    delete_query = State()
    edit_query = State()
    edit_description = State()
    rate_query = State()
    set_rating = State()
```

💡 Клас `FilmStates` використовує `StatesGroup` для групування та визначення різних станів, які можуть бути використані
для різних дій, пов'язаних з фільмами:

- `search_query`: Стан для пошуку фільму за назвою.
- `filter_criteria`: Стан для фільтрації фільмів за певними критеріями.
- `delete_query`: Стан для видалення фільму.
- `edit_query`: Стан для редагування інформації про фільм.
- `edit_description`: Стан для редагування опису фільму.
- `rate_query`: Стан для запиту на оцінку фільму.
- `set_rating`: Стан для встановлення рейтингу фільму.

Необхідно додати обробник для пошуку фільму - функцію `search_film()` в модуль `bot.py`:

```python
# Пошук фільму за назвою
@dp.message(Command("search_film"))
async def search_film(message: Message, state: FSMContext):
    await state.set_state(FilmStates.search_query)
    await message.reply("<b>Введіть назву фільму для пошуку:</b>")
```

- `@dp.message(Command("search_film"))`: Декоратор, який вказує, що ця функція буде викликана, коли користувач введе
  команду `/search_film`.
- `state.set_state(FilmStates.search_query)`: Встановлює стан `search_query`, щоб бот міг отримати назву фільму від
  користувача.
- `message.reply`: Відправляє повідомлення користувачеві з проханням ввести назву фільму для пошуку.

Необхідно додати обробник для отримання запиту пошуку - функцію `get_search_query()` в модуль `bot.py`:

```python
@dp.message(FilmStates.search_query)
async def get_search_query(message: Message, state: FSMContext):
    query = message.text.lower()
    films_data = get_films()
    results = [film for film in films_data if query in film['name'].lower()]

    if results:
        for film_data in results:
            # Створюємо об'єкт Film з даних
            film = Film(**film_data)
            # Формуємо текст повідомлення з деталями про фільм
            text = (f"<b>Фільм:</b> {film.name}\n"
                    f"<b>Опис:</b> {film.description}\n"
                    f"<b>Рейтинг:</b> {film.rating}\n"
                    f"<b>Жанр:</b> {film.genre}\n"
                    f"<b>Актори:</b> {', '.join(film.actors)}\n")

            # Відправляємо повідомлення з фото та інформацією
            await message.answer_photo(
                caption=text,
                photo=URLInputFile(
                    film.poster,
                    filename=f"{film.name}_poster.{film.poster.split('.')[-1]}"
                )
            )
    else:
        await message.reply("<b>Фільм не знайдено!</b>")

    await state.clear()
```

- `@dp.message(FilmStates.search_query)`: Декоратор, який вказує, що ця функція буде викликана, коли користувач введе
  назву фільму для пошуку.
- `query = message.text.lower()`: Отримує назву фільму від користувача та перетворює її у нижній регістр для пошуку.
- `films_data = get_films()`: Отримує список фільмів з файлу `data.json`.
- `results = [film for film in films_data if query in film['name'].lower()]`: Фільтрує список фільмів, щоб знайти ті,
  назва яких містить запит користувача.
- `if results:`: Якщо фільми знайдено, то для кожного фільму створюється об'єкт `Film` і формується текст з деталями про
  фільм.
- `await message.answer_photo`: Відправляє фото з постером фільму та текстом з деталями про фільм.
- `await message.reply("<b>Фільм не знайдено!</b>")`: Якщо фільми не знайдено, відправляє повідомлення користувачеві про
  те, що фільм не знайдено.
- `await state.clear()`: Очищає стан, завершуючи процес пошуку фільму.

[Повернутися до змісту](#зміст-уроку)

---

## 3. Реалізація команди `/filter_films`

Реалізуємо команду `filter_films` для **фільтрації** фільмів за **жанром**.

Необхідно оновити код в файлі `commands.py`:

```python
# New code
from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

START_COMMAND = Command('start')
FILMS_COMMAND = Command('films')
FILM_CREATE_COMMAND = Command("create_film")
FILM_SEARCH_COMMAND = Command("search_film")
FILM_FILTER_COMMAND = Command("filter_films")

BOT_COMMANDS = [
    BotCommand(command="start", description="Почати розмову"),
    BotCommand(command="films", description="Перегляд списку фільмів"),
    BotCommand(command="create_film", description="Додати новий фільм"),
    BotCommand(command="search_film", description="Пошук фільму за назвою"),
    BotCommand(command="filter_films", description="Фільтрація фільмів за жанром"),
]
```

Необхідно додати функцію `filter_film()` в модуль `bot.py`:

```python
# Фільтрація фільмів за жанром
@dp.message(Command("filter_films"))
async def filter_film(message: Message, state: FSMContext):
    await state.set_state(FilmStates.filter_criteria)
    await message.reply("<b>Введіть жанр фільму для фільтрації:</b>")
```

- Декоратор `@dp.message(Command("filter_films"))` вказує, що функція `filter_film` буде викликана, коли користувач
  введе команду `/filter_films`.
- Асинхронна функція `async def filter_film(message: Message, state: FSMContext):` приймає два параметри: `message` (
  повідомлення від користувача) і `state` (контекст стану кінцевого автомата).
- Рядок `await state.set_state(FilmStates.filter_criteria)` встановлює стан `filter_criteria`, щоб бот міг отримати
  жанр фільму від користувача для фільтрації.
- Рядок `await message.reply("<b>Введіть жанр фільму для фільтрації:</b>")` відправляє повідомлення користувачеві з
  проханням ввести жанр фільму для фільтрації.

Необхідно додати функцію `get_filter_criteria()` в модуль `bot.py`:

```python
@dp.message(FilmStates.filter_criteria)
async def get_filter_criteria(message: Message, state: FSMContext):
    criteria = message.text.lower()
    films_data = get_films()

    # Фільтруємо фільми за жанром
    filtered = list(filter(
        lambda film: criteria in film['genre'].lower(),
        films_data
    ))

    if filtered:
        for film_data in filtered:
            # Створюємо об'єкт Film з даних
            film = Film(**film_data)
            # Формуємо текст повідомлення з деталями про фільм
            text = (f"<b>Фільм:</b> {film.name}\n"
                    f"<b>Опис:</b> {film.description}\n"
                    f"<b>Рейтинг:</b> {film.rating}\n"
                    f"<b>Жанр:</b> {film.genre}\n"
                    f"<b>Актори:</b> {', '.join(film.actors)}\n")

            # Відправляємо повідомлення з фото та інформацією
            await message.answer_photo(
                caption=text,
                photo=URLInputFile(
                    film.poster,
                    filename=f"{film.name}_poster.{film.poster.split('.')[-1]}"
                )
            )
    else:
        await message.reply("<b>Фільмів за вказаним жанром не знайдено.</b>")

    await state.clear()
```

- Декоратор `@dp.message(FilmStates.filter_criteria)` вказує, що функція `get_filter_criteria` буде викликана, коли
  користувач введе жанр фільму для фільтрації.
- Асинхронна функція `async def get_filter_criteria(message: Message, state: FSMContext):` приймає два параметри:
  `message` (повідомлення від користувача) і `state` (контекст стану кінцевого автомата).
- Рядок `criteria = message.text.lower()` отримує жанр фільму від користувача та перетворює його у нижній регістр для
  фільтрації.
- Рядок `films_data = get_films()` викликає функцію `get_films` для отримання списку фільмів з файлу `data.json`.
- Рядок `filtered = list(filter(lambda film: criteria in film['genre'].lower(), films_data))` фільтрує список фільмів,
  щоб знайти ті, жанр яких містить введений користувачем жанр.
- `if filtered:`: Якщо фільми знайдено, то для кожного фільму створюється об'єкт `Film` і формується текст з деталями
  про фільм.
- Рядок `await message.answer_photo` відправляє фото з постером фільму та текстом з деталями про фільм.
- `await message.reply("<b>Фільмів за вказаним жанром не знайдено.</b>")`: Якщо фільми не знайдено, відправляє
  повідомлення користувачеві про те, що фільмів за вказаним жанром не знайдено.
- Рядок `await state.clear()` очищає стан, завершуючи процес фільтрації фільмів.

[Повернутися до змісту](#зміст-уроку)

---

## 4. Реалізація команди `/delete_film`

Реалізуємо команду `delete_film` для **видалення** фільму з бібліотеки.

Необхідно оновити код в файлі `commands.py`:

```python
# New code
from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

START_COMMAND = Command('start')
FILMS_COMMAND = Command('films')
FILM_CREATE_COMMAND = Command("create_film")
FILM_SEARCH_COMMAND = Command("search_film")
FILM_FILTER_COMMAND = Command("filter_films")
FILM_DELETE_COMMAND = Command("delete_film")

BOT_COMMANDS = [
    BotCommand(command="start", description="Почати розмову"),
    BotCommand(command="films", description="Перегляд списку фільмів"),
    BotCommand(command="create_film", description="Додати новий фільм"),
    BotCommand(command="search_film", description="Пошук фільму за назвою"),
    BotCommand(command="filter_films", description="Фільтрація фільмів за жанром"),
    BotCommand(command="delete_film", description="Видалення фільму за назвою"),
]
```

Необхідно додати функцію `delete_film()` в модуль `bot.py`:

```python
# Видалення фільму за назвою
@dp.message(Command("delete_film"))
async def delete_film(message: Message, state: FSMContext):
    await message.reply("<b>Введіть назву фільму, який бажаєте видалити:</b>")
    await state.set_state(FilmStates.delete_query)
```

- Декоратор `@dp.message(Command("delete_film"))` вказує, що функція `delete_film` буде викликана, коли користувач введе
  команду `/delete_film`.
- Асинхронна функція `async def delete_film(message: Message, state: FSMContext):` приймає два параметри: `message`
  (повідомлення від користувача) і `state` (контекст стану кінцевого автомата).
- Рядок `await message.reply("<b>Введіть назву фільму, який бажаєте видалити:</b>")` відправляє повідомлення
  користувачеві з проханням ввести назву фільму для видалення.
- Рядок `await state.set_state(FilmStates.delete_query)` встановлює стан `delete_query`, щоб бот міг отримати назву
  фільму від користувача для видалення.

Необхідно додати функцію `get_delete_query()` в модуль `bot.py`:

```python
@dp.message(FilmStates.delete_query)
async def get_delete_query(message: Message, state: FSMContext):
    film_to_delete = message.text.lower()
    films_data = get_films()

    # Шукаємо фільм за назвою
    for film in films_data:
        if film_to_delete == film['name'].lower():
            films_data.remove(film)
            save_films(films_data)  # Зберігаємо оновлений список фільмів
            await message.reply(f"<b>Фільм '{film['name']}' видалено ✅</b>")
            await state.clear()
            return

    await message.reply("<b>Фільм не знайдено!</b>")
    await state.clear()
```

- Декоратор `@dp.message(FilmStates.delete_query)` вказує, що функція `get_delete_query` буде викликана, коли користувач
  введе назву фільму для видалення.
- Асинхронна функція `async def get_delete_query(message: Message, state: FSMContext):` приймає два параметри:
  `message` (повідомлення від користувача) і `state` (контекст стану кінцевого автомата).
- Рядок `film_to_delete = message.text.lower()` отримує назву фільму від користувача та перетворює її у нижній регістр
  для порівняння.
- Рядок `films_data = get_films()` викликає функцію `get_films` для отримання списку фільмів з файлу `data.json`.
- Цикл `for film in films_data:` проходить по списку фільмів, щоб знайти фільм з назвою, яка збігається з введеною
  користувачем.
- Рядок `if film_to_delete == film['name'].lower():` перевіряє, чи збігається назва фільму з введеною користувачем.
- Рядок `films_data.remove(film)` видаляє фільм зі списку фільмів.
- Рядок `save_films(films_data)` зберігає оновлений список фільмів у файл `data.json`.
- Рядок `await message.reply(f"<b>Фільм '{film['name']}' видалено ✅</b>")` відправляє повідомлення користувачеві про
  успішне видалення фільму.
- Рядок `await state.clear()` очищає стан, завершуючи процес видалення фільму.
- Рядок `await message.reply("<b>Фільм не знайдено!</b>")` відправляє повідомлення користувачеві про те, що фільм не
  знайдено.

Необхідно додати функцію `save_films()`, яка буде зберігати фільми, що залишилися в модуль `data.py`.

```python
# Функція для збереження оновленого списку фільмів у файл
def save_films(films_data: list) -> None:
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(films_data, file, ensure_ascii=False, indent=4)
```

- Рядок `def save_films(films_data: list) -> None:` визначає функцію `save_films`, яка приймає список фільмів
  `films_data` і не повертає значення.
- Рядок `with open('data.json', 'w', encoding='utf-8') as file:` відкриває файл `data.json` у режимі запису з кодуванням
  **UTF-8**.
- Рядок `json.dump(films_data, file, ensure_ascii=False, indent=4)` записує список фільмів у файл у форматі `JSON` з
  відступами та підтримкою **не-ASCII** символів.

Без збереження змін, видалення фільму буде тимчасовим - після перезапуску бота всі фільми повернуться назад, оскільки
вони будуть знову завантажені з початкового джерела даних.

- Змінна `films_data` існує тільки в пам'яті під час виконання функції.
- Якщо не зберегти зміни - вони будуть втрачені.

```python
# Old code
import json


#  Функція для отримання списку фільмів
def get_films(file_path: str = "data.json", film_id: int | None = None) -> list[dict] | dict:
    with open(file_path, 'r') as fp:
        films = json.load(fp)
        if film_id is not None and film_id < len(films):
            return films[film_id]
        return films


#  Функція для додавання нового фільму у список
def add_film(film: dict, file_path: str = "data.json"):
    films = get_films(file_path=file_path, film_id=None)
    if films:
        films.append(film)
        with open(file_path, "w") as fp:
            json.dump(films, fp, indent=4, ensure_ascii=False)
```

```python
# New code
import json


# Функція для отримання списку фільмів
def get_films(file_path: str = "data.json", film_id: int | None = None) -> list[dict] | dict:
    with open(file_path, 'r') as fp:
        films = json.load(fp)
        if film_id is not None and film_id < len(films):
            return films[film_id]
        return films


# Функція для додавання нового фільму у список
def add_film(film: dict, file_path: str = "data.json"):
    films = get_films(file_path=file_path, film_id=None)
    if films:
        films.append(film)
        with open(file_path, "w") as fp:
            json.dump(films, fp, indent=4, ensure_ascii=False)


# Функція для збереження оновленого списку фільмів у файл
def save_films(films_data: list) -> None:
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(films_data, file, ensure_ascii=False, indent=4)
```

Необхідно додати імпорт функції `save_films()` в модуль `bot.py`:

```python
# Old string
from data import get_films, add_film

# New string
from data import get_films, add_film, save_films
```

[Повернутися до змісту](#зміст-уроку)

---

## 5. Реалізація команди `/edit_film`

Реалізуємо команду `edit_film` для редагування інформації про фільм.

Необхідно оновити код в файлі `commands.py`:

```python
# New code
from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

START_COMMAND = Command('start')
FILMS_COMMAND = Command('films')
FILM_CREATE_COMMAND = Command("create_film")
FILM_SEARCH_COMMAND = Command("search_film")
FILM_FILTER_COMMAND = Command("filter_films")
FILM_EDIT_COMMAND = Command("edit_film")
FILM_DELETE_COMMAND = Command("delete_film")

BOT_COMMANDS = [
    BotCommand(command="start", description="Почати розмову"),
    BotCommand(command="films", description="Перегляд списку фільмів"),
    BotCommand(command="create_film", description="Додати новий фільм"),
    BotCommand(command="search_film", description="Пошук фільму за назвою"),
    BotCommand(command="filter_films", description="Фільтрація фільмів за жанром"),
    BotCommand(command="edit_film", description="Редагування інформації про фільм"),
    BotCommand(command="delete_film", description="Видалення фільму за назвою"),
]
```

💡 Функція `edit_film()` дозволяє користувачеві розпочати процес редагування інформації про фільм, якщо такі фільми є в
системі.

Необхідно додати функцію `edit_film()` в модуль `bot.py`:

```python
# Редагування інформації про фільм
@dp.message(Command("edit_film"))
async def edit_film(message: Message, state: FSMContext):
    films_data = get_films()
    if not films_data:
        await message.reply("<b>Список фільмів порожній!</b>")
        return

    film_names = "\n".join([f"- {film['name']}" for film in films_data])
    await message.reply(
        "<b>Введіть назву фільму, який бажаєте редагувати:</b>\n"
        f"Доступні фільми:\n{film_names}"
    )
    await state.set_state(FilmStates.edit_query)
```

- Декоратор `@dp.message(Command("edit_film"))` вказує, що функція `edit_film` буде викликана, коли користувач введе
  команду `/edit_film`.
- Асинхронна функція `async def edit_film(message: Message, state: FSMContext):` приймає два параметри: `message`
  (повідомлення від користувача) і `state` (контекст стану кінцевого автомата).
- Рядок `films_data = get_films()` отримує дані про фільми, використовуючи функцію `get_films()`.
- Умовний блок `if not films_data:` перевіряє, чи є дані про фільми. Якщо список фільмів порожній, бот відповідає
  повідомленням: `<b>Список фільмів порожній!</b>`.
- Рядок `film_names = "\n".join([f"- {film['name']}" for film in films_data])` створює рядок з назвами фільмів, кожна з
  яких починається з нового рядка та з символом `"-"`.
- Рядок
  `await message.reply("<b>Введіть назву фільму, який бажаєте редагувати:</b>\n" f"Доступні фільми:\n{film_names}")`
  відправляє повідомлення користувачеві з проханням ввести назву фільму для редагування та надає список доступних
  фільмів.
- Рядок `await state.set_state(FilmStates.edit_query)` встановлює стан `edit_query`, щоб бот міг отримати назву фільму
  від користувача для подальшого редагування.

💡 Функція `get_edit_query()` дозволяє користувачеві вказати фільм для редагування та отримати інструкції щодо подальших
дій.

Необхідно додати функцію `get_edit_query()` в модуль `bot.py`:

```python
@dp.message(FilmStates.edit_query)
async def get_edit_query(message: Message, state: FSMContext):
    film_name = message.text.strip()
    films_data = get_films()

    film_found = None
    for film in films_data:
        if film_name.lower() == film['name'].lower():
            film_found = film
            break

    if not film_found:
        await message.reply("<b>Фільм не знайдено!</b>")
        await state.clear()
        return

    await state.update_data(film=film_found, films_data=films_data)
    await message.reply(
        "<b>Введіть поле для редагування та нове значення у форматі:</b>\n"
        "<code>поле|нове значення</code>\n\n"
        "<b>Доступні поля:</b> name, description, rating, genre, actors, poster\n"
        "<b>Приклад:</b> <code>rating|9.5</code>"
    )
    await state.set_state(FilmStates.edit_description)
```

- Декоратор `@dp.message(FilmStates.edit_query)` вказує, що функція `get_edit_query` буде викликана, коли користувач
  надасть назву фільму для редагування, перебуваючи у стані `edit_query`.
- Асинхронна функція `async def get_edit_query(message: Message, state: FSMContext):` приймає два параметри: `message`
  (повідомлення від користувача з назвою фільму) і `state` (контекст стану кінцевого автомата).
- Рядок `film_name = message.text.strip()` отримує назву фільму з повідомлення користувача, видаляючи зайві пробіли.
- Рядок `films_data = get_films()` отримує дані про фільми, використовуючи функцію `get_films()`.
- Блок `for` шукає фільм у списку `films_data`, порівнюючи назву фільму з тим, що ввів користувач. Якщо фільм знайдено,
  він зберігається у змінній `film_found`.
- Умовний блок `if not film_found:` перевіряє, чи був знайдений фільм. Якщо фільм не знайдено, бот відповідає
  повідомленням `<b>Фільм не знайдено!</b>` і очищає стан за допомогою `await state.clear()`.
- Рядок `await state.update_data(film=film_found, films_data=films_data)` оновлює дані стану, зберігаючи знайдений фільм
  та загальні дані про фільми.
- Рядок `await message.reply("<b>Введіть поле для редагування та нове значення у форматі:</b>\n"` `"<code>поле|нове
  значення</code>\n\n"` `"<b>Доступні поля:</b> name, description, rating, genre, actors, poster\n" "<b>`
  `Приклад:</b> <code>rating|9.5</code>")` відправляє повідомлення користувачеві з інструкцією щодо формату введення
  поля та нового значення для редагування.
- Рядок `await state.set_state(FilmStates.edit_description)` встановлює стан `edit_description`, щоб бот міг отримати
  поле та нове значення для редагування від користувача.

💡 Функція `process_edit()` дозволяє користувачеві оновити інформацію про фільм, обробляючи різні типи даних та
повідомляючи про успішне оновлення або помилки.

Необхідно додати функцію `process_edit()` в модуль `bot.py`:

```python
@dp.message(FilmStates.edit_description)
async def process_edit(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        film = data['film']
        films_data = data['films_data']

        if '|' not in message.text:
            raise ValueError("Невірний формат. Використовуйте '|' для розділення поля та значення")

        field, new_value = message.text.split('|', 1)
        field = field.strip().lower()
        new_value = new_value.strip()

        valid_fields = ['name', 'description', 'rating', 'genre', 'actors', 'poster']
        if field not in valid_fields:
            raise ValueError(f"Невірне поле. Доступні: {', '.join(valid_fields)}")

        # Обробка спеціальних типів даних
        if field == 'rating':
            try:
                new_value = float(new_value)
                if not 0 <= new_value <= 10:
                    raise ValueError("Рейтинг повинен бути від 0 до 10")
            except ValueError:
                raise ValueError("Рейтинг повинен бути числом (наприклад, 8.5)")
        elif field == 'actors':
            new_value = [actor.strip() for actor in new_value.split(',')]

        # Оновлення поля
        for f in films_data:
            if f['name'] == film['name']:
                f[field] = new_value
                break

        save_films(films_data)
        await message.reply(f"<b>Фільм '{film['name']}' успішно оновлено!</b>\n"
                            f"<b>{field}:</b> {new_value}")
        await state.clear()

    except Exception as e:
        await message.reply(f"<b>Помилка:</b> {str(e)}\n"
                            "<b>Використовуйте формат:</b>\n"
                            "<code>поле|нове значення</code>\n"
                            "<b>Приклад:</b> <code>rating|9.5</code>")
        await state.clear()
```

- Декоратор `@dp.message(FilmStates.edit_description)` вказує, що функція `process_edit` буде викликана, коли користувач
  надасть інформацію про поле та нове значення для редагування, перебуваючи у стані `edit_description`.
- Асинхронна функція `async def process_edit(message: Message, state: FSMContext):` приймає два параметри: `message`
  (повідомлення від користувача з полем та новим значенням) і `state` (контекст стану кінцевого автомата).
- Блок `try:` використовується для обробки можливих помилок під час виконання функції.
- Рядок `data = await state.get_data()` отримує дані стану, які містять інформацію про фільм та загальні дані про
  фільми.
- Рядки `film = data['film'] та films_data = data['films_data']` отримують відповідно дані про конкретний фільм та
  загальні дані про фільми.
- Умовний блок `if '|' not in message.text:` перевіряє, чи містить повідомлення символ `|`, який використовується для
  розділення поля та нового значення. Якщо ні, викликається помилка з повідомленням про невірний формат.
- Рядок `field, new_value = message.text.split('|', 1)` розділяє повідомлення на поле та нове значення.
- Рядки `field = field.strip().lower() та new_value = new_value.strip()` видаляють зайві пробіли з поля та нового
  значення.
- Умовний блок `if field not in valid_fields:` перевіряє, чи є вказане поле у списку допустимих полів. Якщо ні,
  викликається помилка з повідомленням про невірне поле.
- Блоки `if field == 'rating': та elif field == 'actors':` обробляють спеціальні типи даних для полів `rating` та
  `actors`.
- Для `rating` перевіряється, чи є нове значення числом у діапазоні від `0` до `10`. Для `actors` нове значення
  розділяється на список акторів.
- Цикл `for f in films_data:` оновлює значення поля для конкретного фільму у загальних даних про фільми.
- Рядок `save_films(films_data)` зберігає оновлені дані про фільми.
- Рядок `await message.reply(f"<b>Фільм '{film['name']}' успішно оновлено!</b>\n" f"<b>{field}:</b> {new_value}")`
  повідомляє користувачеві про успішне оновлення фільму.
- Рядок `await state.clear()` очищає стан кінцевого автомата.
- Блок `except Exception as e:` обробляє помилки, які можуть виникнути під час виконання функції, та повідомляє
  користувачеві про помилку з інструкцією щодо правильного формату введення.

[Повернутися до змісту](#зміст-уроку)

---

## 6. Реалізація команди `/recommend_film`

Реалізуємо команду `recommend_film`, яка надасть користувачу рекомендацію фільмів з найвищим рейтингом.

Необхідно оновити код в файлі `commands.py`:

```python
# New code
from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

START_COMMAND = Command('start')
FILMS_COMMAND = Command('films')
FILM_CREATE_COMMAND = Command("create_film")
FILM_SEARCH_COMMAND = Command("search_film")
FILM_FILTER_COMMAND = Command("filter_films")
FILM_RECOMMEND_COMMAND = Command("recommend_film")
FILM_EDIT_COMMAND = Command("edit_film")
FILM_DELETE_COMMAND = Command("delete_film")

BOT_COMMANDS = [
    BotCommand(command="start", description="Почати розмову"),
    BotCommand(command="films", description="Перегляд списку фільмів"),
    BotCommand(command="create_film", description="Додати новий фільм"),
    BotCommand(command="search_film", description="Пошук фільму за назвою"),
    BotCommand(command="filter_films", description="Фільтрація фільмів за жанром"),
    BotCommand(command="recommend_film", description="Отримати рекомендацію 🍿 Best ⭐️ Films"),
    BotCommand(command="edit_film", description="Редагування інформації про фільм"),
    BotCommand(command="delete_film", description="Видалення фільму за назвою"),
]
```

Необхідно додати функцію `recommend_film()` в модуль `bot.py`:

```python
# Функція для рекомендацій
@dp.message(Command("recommend_film"))
async def recommend_film(message: Message) -> None:
    films_data = get_films()

    # Фільтруємо фільми з рейтингом та сортуємо за спаданням рейтингу
    rated_films = [film for film in films_data if film.get('rating') is not None]
    if not rated_films:
        await message.reply("<b>На жаль, немає фільмів з рейтингом для рекомендації.</b>")
        return

    # Сортуємо за рейтингом та беремо топ-3
    top_films = sorted(rated_films, key=lambda x: float(x['rating']), reverse=True)[:3]

    # Відправляємо інформацію про кожний рекомендований фільм
    await message.reply("<b>🍿 Best ⭐️ Films:</b>")

    for i, film_data in enumerate(top_films, 1):
        film = Film(**film_data)
        text = (f"<b>#{i} Рекомендований фільм:</b>\n"
                f"<b>Назва:</b> {film.name}\n"
                f"<b>Опис:</b> {film.description}\n"
                f"<b>Рейтинг:</b> ⭐️ {film.rating}/10\n"
                f"<b>Жанр:</b> {film.genre}\n"
                f"<b>Актори:</b> {', '.join(film.actors)}\n")

        await message.answer_photo(
            caption=text,
            photo=URLInputFile(
                film.poster,
                filename=f"{film.name}_poster.{film.poster.split('.')[-1]}"
            ),
            parse_mode="HTML"
        )
```

- Декоратор `@dp.message(Command("recommend_film"))` вказує, що функція `recommend_film` буде викликана, коли користувач
  введе команду `/recommend_film`.
- Асинхронна функція `async def recommend_film(message: Message) -> None:` приймає один параметр: `message` (
  повідомлення від користувача).
- Рядок `films_data = get_films()` отримує дані про фільми, використовуючи функцію `get_films()`.
- Рядок `rated_films = [film for film in films_data if film.get('rating') is not None]` фільтрує фільми, які мають
  рейтинг.
- Умовний блок `if not rated_films:` перевіряє, чи є фільми з рейтингом. Якщо фільмів з рейтингом немає, бот відповідає
  повідомленням `<b>На жаль, немає фільмів з рейтингом для рекомендації.</b>`.
- Рядок `top_films = sorted(rated_films, key=lambda x: float(x['rating']), reverse=True)[:3]` сортує фільми за рейтингом
  у порядку спадання та вибирає топ-3 фільми.
- Рядок `await message.reply("<b>🍿 Best ⭐️ Films:</b>")` повідомляє користувачеві, що будуть надані рекомендації
  фільмів.
- Цикл `for` відправляє інформацію про кожен рекомендований фільм, створюючи об'єкт `Film` з даних та формуючи текст
  повідомлення з деталями про фільм.
- Рядок `await message.answer_photo(...)` відправляє фото з постером фільму та текстом з деталями.

[Повернутися до змісту](#зміст-уроку)

---

## 7. Підведення підсумків 🚀

> На цьому уроці ми вивчили наступні теми:

- Навчилися додавати пошук та фільтрацію фільмів у Телеграм-боті.
- Реалізували функції видалення, редагування фільмів та рекомендації фільмів.

[Повернутися до змісту](#зміст-уроку)

---

## 8. Домашнє завдання 🏠

### 🧩 Завдання 1:

Необхідно додати нову функцію пошуку за актором:

- Реалізуйте команду `/search_by_actor`, яка дозволить користувачам знаходити фільми за іменем актора.
- Використовуйте методи рядків для перевірки, чи є ім'я актора в описі фільму, і поверніть список фільмів, у яких він
  знімається.

<details>
<summary>✅ Code</summary>

```python
@dp.message_handler(commands=['search_by_actor'])
async def search_by_actor(message: types.Message):
    await message.reply("Введіть ім'я актора для пошуку фільмів:")
    await MovieStates.search_query.set()


@dp.message_handler(state=MovieStates.search_query)
async def get_search_query(message: types.Message, state: FSMContext):
    query = message.text.lower()
    results = [film for film in films if query in film['description'].lower()]

    if results:
        for film in results:
            await message.reply(f"Знайдено: {film['name']} - {film['description']}")
    else:
        await message.reply("Фільми з цим актором не знайдено.")

    await state.finish()
```

</details>

### 🧩 Завдання 2

Необхідно покращити фільтрацію фільмів:

- Додайте можливість фільтрації за кількома критеріями одночасно, наприклад, за жанром і роком випуску.
- Це можна зробити за допомогою додаткових умов у функції фільтрації.

<details>
<summary>✅ Code</summary>

```python
@dp.message_handler(commands=['filter_films'])
async def filter_films(message: types.Message):
    await message.reply("Введіть жанр і рік випуску для фільтрації через кому:")
    await MovieStates.filter_criteria.set()


@dp.message_handler(state=MovieStates.filter_criteria)
async def get_filter_criteria(message: types.Message, state: FSMContext):
    criteria = message.text.lower().split(',')
    genre = criteria[0].strip()
    year = criteria[1].strip()

    filtered = list(filter(
        lambda film: genre in film['genre'].lower() and str(film['year']) == year, films
    ))

    if filtered:
        for film in filtered:
            await message.reply(f"Знайдено: {film['name']} - {film['description']}")
    else:
        await message.reply("Фільм не знайдено за цими критеріями.")

    await state.finish()
```

</details>

### 🧩 Завдання 3

Необхідно додати обробку винятків у функціях застосунку:

- Додайте додаткову перевірку в функції видалення та редагування фільмів, щоб обробляти випадки, коли користувач вводить
  некоректні або порожні дані.
- Переконайтеся, що бот надає чіткі та зрозумілі повідомлення про помилки.

### 🧩 Завдання 4

Необхідно написати тест-кейси:

- Напишіть кілька тест-кейсів для перевірки функцій пошуку, фільтрації, видалення та редагування.
- Опишіть, які вхідні дані ви використовували і які результати очікували.

<details>
<summary>✅ Code</summary>

```python
# Тест-кейс 1: Пошук фільму за назвою
# Вхідні дані: Назва фільму "Inception"
# Очікуваний результат: Фільм "Inception" знайдено, виведено опис фільму

# Тест-кейс 2: Фільтрація фільмів за жанром
# Вхідні дані: Жанр "Sci-Fi"
# Очікуваний результат: Виведено список фільмів жанру "Sci-Fi"

# Тест-кейс 3: Видалення фільму за назвою
# Вхідні дані: Назва фільму "Inception"
# Очікуваний результат: Фільм "Inception" видалено з бібліотеки

# Тест-кейс 4: Редагування опису фільму
# Вхідні дані: Назва фільму "Inception", новий опис "A mind-bending thriller"
# Очікуваний результат: Опис фільму "Inception" оновлено на "A mind-bending thriller"
```

</details>

[Повернутися до змісту](#зміст-уроку)

---
