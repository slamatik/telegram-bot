from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard():
    keyboard = [
        [KeyboardButton('Market'),
         KeyboardButton('Portfolio'),
         KeyboardButton('End'),
         KeyboardButton('Tickers')],
        # [KeyboardButton('Portfolio'), KeyboardButton('Market Status')], [KeyboardButton('Start Again')]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def portfolio_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton('Print', callback_data='print tickers')],
        [InlineKeyboardButton('Add', callback_data='add')],
        [InlineKeyboardButton('Delete', callback_data='delete')],
        [InlineKeyboardButton('Save', callback_data='save')],
        [InlineKeyboardButton('Back', callback_data='back')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def market_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton('Last', callback_data='last')],
        [InlineKeyboardButton('Pre market', callback_data='premarket')],
        [InlineKeyboardButton('After hours', callback_data='afterhours')],
        [InlineKeyboardButton('Back', callback_data='back')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def ticker_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton('Daily', callback_data='daily')],
        [InlineKeyboardButton('Weekly', callback_data='weekly')],
        [InlineKeyboardButton('Back', callback_data='back')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup
