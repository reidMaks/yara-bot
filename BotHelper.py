from telebot import types


class ButtonManager:

    @staticmethod
    def get_start_keyboard() -> types.ReplyKeyboardMarkup:
        eat_btn = types.KeyboardButton('🍼Еда')
        sleep_btn = types.KeyboardButton('😴 Сон')
        walk_btn = types.KeyboardButton('🚶 Прогулка')
        shit_btn = types.KeyboardButton('💩 О мой б-г, это случилось')
        bath_btn = types.KeyboardButton('🛁 Купание')
        stat_btn = types.KeyboardButton('📈 Статистика')

        markup = types.ReplyKeyboardMarkup(selective=True, resize_keyboard=True)

        markup.add(walk_btn, bath_btn, sleep_btn)
        markup.add(shit_btn, eat_btn)
        markup.add(stat_btn)

        return markup
