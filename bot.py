# Імпортуємо необхідні модулі
import asyncio  # Для асинхронного програмування
import logging  # Для логування подій
import sys  # Для доступу до деяких змінних та функцій, пов'язаних з інтерпретатором Python

# Імпортуємо токен бота з конфігураційного файлу
from config import BOT_TOKEN as TOKEN

# Імпортуємо необхідні класи та функції з бібліотеки aiogram
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, URLInputFile, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from commands import FILMS_COMMAND, START_COMMAND, FILM_CREATE_COMMAND, BOT_COMMANDS
from data import get_films, add_film, save_films
from keyboards import films_keyboard_markup, FilmCallback
from models import Film

# Ініціалізуємо диспетчер для обробки оновлень
dp = Dispatcher()


# Форма для отримання інформації про фільми від користувача
class FilmForm(StatesGroup):
    name = State()
    description = State()
    rating = State()
    genre = State()
    actors = State()
    poster = State()


class FilmStates(StatesGroup):
    search_query = State()
    filter_criteria = State()
    delete_query = State()
    edit_query = State()
    edit_description = State()
    rate_query = State()
    set_rating = State()


# Обробник для команди /start
@dp.message(Command("start"))
async def start(message: Message) -> None:
    await message.answer(
        f"Hello🖐, {html.bold(message.from_user.full_name)}!\n"
        "I'm your first Telegram Bot 🥳"
    )


# Обробник для команди /films
@dp.message(FILMS_COMMAND)
async def films(message: Message) -> None:
    data = get_films()
    markup = films_keyboard_markup(films_list=data)
    await message.answer(
        f"<b>Список фільмів: 🎬</b>\nОберіть фільм, щоб отримати інформацію про нього.",
        reply_markup=markup
    )


# Обробник зворотного виклику для фільмів
@dp.callback_query(FilmCallback.filter())
async def callback_film(callback: CallbackQuery, callback_data: FilmCallback) -> None:
    # Отримуємо ID фільму з даних зворотного виклику
    film_id = callback_data.id
    # Отримуємо дані про конкретний фільм за його ID
    film_data = get_films(film_id=film_id)
    # Створюємо об'єкт фільму
    film = Film(**film_data)

    # Формуємо текст повідомлення з деталями про фільм
    text = (
        f"<b>Фільм:</b> {film.name}\n"
        f"<b>Опис:</b> {film.description}\n"
        f"<b>Рейтинг:</b> {film.rating}\n"
        f"<b>Жанр:</b> {film.genre}\n"
        f"<b>Актори:</b> {', '.join(film.actors)}\n"
    )

    # Відправляємо фото з постером фільму та текстом з деталями
    await callback.message.answer_photo(
        caption=text,
        photo=URLInputFile(
            film.poster,
            filename=f"{film.name}_poster.{film.poster.split('.')[-1]}"
        )
    )


# Функції-обробники для кожного поля форми отримання інформації від користувача
@dp.message(FILM_CREATE_COMMAND)
async def film_create(message: Message, state: FSMContext) -> None:
    await state.set_state(FilmForm.name)
    await message.answer(
        f"<b>Введіть назву фільму ...</b>",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(FilmForm.name)
async def film_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(FilmForm.description)
    await message.answer(
        f"<b>Введіть опис фільму ...</b>",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(FilmForm.description)
async def film_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(FilmForm.rating)
    await message.answer(
        f"<b>Вкажіть рейтинг фільму (від 0 до 10) ...</b>",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(FilmForm.rating)
async def film_rating(message: Message, state: FSMContext) -> None:
    await state.update_data(rating=float(message.text))
    await state.set_state(FilmForm.genre)
    await message.answer(
        f"<b>Введіть жанр фільму ...</b>",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(FilmForm.genre)
async def film_genre(message: Message, state: FSMContext) -> None:
    await state.update_data(genre=message.text)
    await state.set_state(FilmForm.actors)
    await message.answer(
        text=f"<b>Введіть акторів фільму через `, ` \n⚠️ (Обов'язкова кома та відступ після неї)</b>",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(FilmForm.actors)
async def film_actors(message: Message, state: FSMContext) -> None:
    await state.update_data(actors=[x for x in message.text.split(", ")])
    await state.set_state(FilmForm.poster)
    await message.answer(
        f"<b>Введіть посилання на постер фільму ...</b>",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(FilmForm.poster)
async def film_poster(message: Message, state: FSMContext) -> None:
    data = await state.update_data(poster=message.text)
    film = Film(**data)
    add_film(film.model_dump())
    await state.clear()
    await message.answer(
        f"<b>Фільм {film.name} успішно додано ✅</b>",
        reply_markup=ReplyKeyboardRemove(),
    )


# Пошук фільму за назвою
@dp.message(Command("search_film"))
async def search_film(message: Message, state: FSMContext):
    await state.set_state(FilmStates.search_query)
    await message.reply("<b>Введіть назву фільму для пошуку:</b>")


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


# Фільтрація фільмів за жанром
@dp.message(Command("filter_films"))
async def filter_film(message: Message, state: FSMContext):
    await state.set_state(FilmStates.filter_criteria)
    await message.reply("<b>Введіть жанр фільму для фільтрації:</b>")


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


# Видалення фільму за назвою
@dp.message(Command("delete_film"))
async def delete_film(message: Message, state: FSMContext):
    await message.reply("<b>Введіть назву фільму, який бажаєте видалити:</b>")
    await state.set_state(FilmStates.delete_query)


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


# Редагування інформації про фільм
@dp.message(Command("edit_film"))
async def edit_film(message: Message, state: FSMContext):
    films_data = get_films()
    if not films_data:
        await message.reply("<b>Список фільмів порожній. Немає що редагувати.</b>")
        return

    film_names = "\n".join([f"- {film['name']}" for film in films_data])
    await message.reply(
        "<b>Введіть назву фільму, який бажаєте редагувати:</b>\n"
        f"Доступні фільми:\n{film_names}"
    )
    await state.set_state(FilmStates.edit_query)


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


# Головна асинхронна функція для запуску бота
async def main() -> None:
    # Ініціалізуємо екземпляр бота з токеном та властивостями за замовчуванням
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # Встановлюємо команди бота
    await bot.set_my_commands(BOT_COMMANDS)

    # Запускаємо цикл опитування для отримання оновлень
    await dp.start_polling(bot)


# Перевіряємо, чи скрипт запускається напряму
if __name__ == "__main__":
    # Налаштовуємо базове логування для виведення інформаційних повідомлень у стандартний потік виведення
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # Запускаємо головну асинхронну функцію
    asyncio.run(main())
