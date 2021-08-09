from telebot import types


class ButtonManager:

    def get_start_keyboard(self):

        eat_btn = '🍼Еда'
        sleep_btn = '😴 Сон'
        walk_btn = '🚶 Прогулка'
        shit_btn = '💩 О мой б-г, это случилось'
        bath_btn = '🛁 Купание'
        stat_btn = '📈 Статистика'

        markup = types.ReplyKeyboardMarkup(row_width=1)

        markup.add(types.KeyboardButton(eat_btn))
        markup.add(types.KeyboardButton(sleep_btn))
        markup.add(types.KeyboardButton(walk_btn))
        markup.add(types.KeyboardButton(shit_btn))
        markup.add(types.KeyboardButton(bath_btn))
        markup.add(types.KeyboardButton(stat_btn))

        return markup