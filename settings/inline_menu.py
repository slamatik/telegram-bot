from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler

i = 5
MARKET, PORTFOLIO, CHOOSING_MAIN, CHOOSING_MARKET, CHOOSING_PORTFOLIO = map(chr, range(i))
MARKET_LAST, MARKET_PM, MARKET_AH = map(chr, range(i, i + 3))
PRINT_TICKERS, ADD_TICKERS, DELETE_TICKERS, SAVE_PORTFOLIO = map(chr, range(i + 3, i + 7))
TYPING_TICKERS = map(chr, range(i+7, i+9))
TYPING, TEST = map(chr, range(100, 102))
DUMMY_BUTTON, ASD = map(chr, range(200, 202))
BACK_TO_PORTFOLIO, BACK_TO_MARKET, TICKER_MENU, TICKER_TO_DELETE = map(chr, range(300, 304))
TICKER_INFO, TICKER_DAILY, TICKER_WEEKLY, ADDING_TICKERS, CHOOSING_TICKERS = map(chr, range(400, 405))

END = ConversationHandler.END


def main_menu():
    buttons = [
        [
            InlineKeyboardButton(text='Mange Portfolio', callback_data=str(PORTFOLIO))
        ],
        [
            InlineKeyboardButton(text='Market', callback_data=str(MARKET)),
            InlineKeyboardButton(text='End', callback_data=str(END))
        ]
        # InlineKeyboardButton(text='Market', callback_data='market'),
    ]

    return InlineKeyboardMarkup(buttons)


def market_menu():
    buttons = [
        [InlineKeyboardButton(text='Last', callback_data=str(MARKET_LAST))],
        [InlineKeyboardButton(text='Pre Market', callback_data=str(MARKET_PM))],
        [InlineKeyboardButton(text='After Hours', callback_data=str(MARKET_AH))],
        [InlineKeyboardButton(text='Back', callback_data=str(CHOOSING_MAIN))],
    ]
    return InlineKeyboardMarkup(buttons)


def portfolio_menu():
    buttons = [
        [InlineKeyboardButton('Print', callback_data=str(PRINT_TICKERS))],
        [InlineKeyboardButton('Add', callback_data=str(ADD_TICKERS))],
        [InlineKeyboardButton('Delete', callback_data=str(DELETE_TICKERS))],
        [InlineKeyboardButton('Save', callback_data=str(SAVE_PORTFOLIO))],
        [InlineKeyboardButton('Back', callback_data=str(CHOOSING_MAIN))],
    ]
    return InlineKeyboardMarkup(buttons)


def ticker_menu():
    buttons = [
        [InlineKeyboardButton('Info', callback_data=str(TICKER_INFO))],
        [InlineKeyboardButton('Daily Chart', callback_data=str(TICKER_DAILY))],
        [InlineKeyboardButton('Weekly Chart', callback_data=str(TICKER_WEEKLY))],
        # [InlineKeyboardButton('Back', callback_data=str(BACK_TO_PORTFOLIO))],
        [InlineKeyboardButton('Back', callback_data=str(CHOOSING_PORTFOLIO))],
    ]
    return InlineKeyboardMarkup(buttons)


def ticker_keyboard(tickers):
    n = len(tickers)
    n_col = round(n ** 0.5)
    keyboard = []
    row = []
    for idx, ticker in enumerate(tickers):
        row.append(InlineKeyboardButton(ticker, callback_data='$' + ticker))
        if len(row) == n_col:
            keyboard.append(row)
            row = []
    while 0 < len(row) < n_col:
        row.append(InlineKeyboardButton(' ', callback_data=DUMMY_BUTTON))
    keyboard.append(row)
    keyboard.append([InlineKeyboardButton('Back', callback_data=CHOOSING_PORTFOLIO)])
    return InlineKeyboardMarkup(keyboard)
