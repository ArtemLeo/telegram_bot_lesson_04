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
