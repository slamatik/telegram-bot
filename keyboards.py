from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler

END = ConversationHandler.END
# Main Menu
MARKET, PORTFOLIO, CHOOSING_MAIN, CHOOSING_MARKET, CHOOSING_PORTFOLIO = map(chr, range(5))
# Portfolio Menu
MARKET_LAST, MARKET_PM, MARKET_AH = map(chr, range(5, 8))
# Market Menu
PRINT_TICKERS, ADD_TICKERS, DELETE_TICKERS, SAVE_PORTFOLIO = map(chr, range(8, 12))


def main_menu():
    buttons = [
        [
            InlineKeyboardButton(text='Mange Portfolio', callback_data=str(PORTFOLIO))
        ],
        [
            InlineKeyboardButton(text='Market', callback_data=str(MARKET)),
            InlineKeyboardButton(text='End', callback_data=str(END))
        ]
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