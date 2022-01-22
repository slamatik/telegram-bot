import logging
from user import User
import helper
from settings.config import *
import pickle
from settings.inline_menu import *
from telegram import Update
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, ConversationHandler, \
    CallbackContext, MessageHandler, Filters
from finviz.screener import Screener

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


class MyTelegramBot:
    def __init__(self):
        self.username = None
        self.user = None
        self.tickers = None
        self.chat_id = None
        # todo watchlist/portfolio perfomance

    def start(self, update: Update, context: CallbackContext):
        self.username = update.effective_user.first_name if update.effective_user.first_name is not None else update.effective_user.username
        self.user = User(update.effective_user.id)
        self.tickers = self.user.tickers
        self.chat_id = update.effective_chat.id

        message = f'✌🏻 {self.username}! '
        if self.user.tickers:
            message += f'I can tell you some info about the market, please select one option below...\nMain Menu'
        else:
            # todo manage first time users
            message += f'Looks like it is your first time using this bot.'
        update.message.reply_text(message, reply_markup=main_menu())
        return CHOOSING_MAIN

    def end(self, update: Update, context: CallbackContext):
        # todo needs checking and looking at
        update.callback_query.answer()
        text = 'See you later'
        update.callback_query.edit_message_text(text=text)
        # del self
        return END

    def back(self, update: Update, context: CallbackContext):
        # check where we are
        # reply markup depending on from where and to where we are moving
        current_level = update.callback_query.data
        if current_level == str(CHOOSING_MAIN):
            keyboard = main_menu()
            return_state = CHOOSING_MAIN
        elif current_level == str(CHOOSING_PORTFOLIO):
            keyboard = portfolio_menu()
            return_state = CHOOSING_PORTFOLIO

        update.callback_query.edit_message_text(text=MAIN_MESSAGE, reply_markup=keyboard)
        return return_state

    def portfolio(self, update: Update, context: CallbackContext):
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=PORTFOLIO_MESSAGE, reply_markup=portfolio_menu())
        return CHOOSING_PORTFOLIO

    def print_tickers(self, update: Update, context: CallbackContext):
        update.callback_query.answer()
        text = 'Tickers...'
        reply_markup = ticker_keyboard(self.tickers)
        update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
        return CHOOSING_TICKERS

    def add_ticker(self, update: Update, context: CallbackContext):
        update.callback_query.message.edit_text('Enter tickers:')
        return ADDING_TICKERS

    def input_tickers(self, update: Update, context: CallbackContext):
        tickers = update.message.text.split(',')
        tickers = [i.strip()[1:].upper() for i in tickers]
        self.user.add_ticker(tickers)
        message = ', '.join(tickers) + ' successfully added'
        update.message.reply_text(message + '\nPlease select option below', reply_markup=portfolio_menu())
        return CHOOSING_PORTFOLIO

    def delete_ticker(self, update: Update, context: CallbackContext):
        update.callback_query.answer()
        text = 'Tickers...'
        reply_markup = ticker_keyboard(self.tickers)
        update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
        return TICKER_TO_DELETE

    def ticker_to_delete(self, update: Update, context: CallbackContext):
        ticker = update.callback_query.data[1:]
        update.callback_query.edit_message_text(text=ticker + ' clicked')
        self.tickers.remove(ticker)
        return self.delete_ticker(update, context)

    def save(self, update: Update, context: CallbackContext):
        self.user.save_user()
        update.callback_query.message.edit_text(text=f'{self.user.id} successfully saved',
                                                reply_markup=portfolio_menu())
        return CHOOSING_PORTFOLIO

    def select_ticker(self, update: Update, context: CallbackContext):
        ticker = update.callback_query.data[1:]
        context.user_data['selected_ticker'] = ticker
        update.callback_query.edit_message_text(f'{ticker} info', reply_markup=ticker_menu())
        return TICKER_MENU

    def info(self, update: Update, context: CallbackContext):
        ticker = context.user_data['selected_ticker']
        # todo print some info about ticker
        update.callback_query.edit_message_text(f'Detailed {ticker} info', reply_markup=ticker_menu())
        return TICKER_MENU

    def daily(self, update: Update, context: CallbackContext):
        ticker = context.user_data['selected_ticker']
        Screener(tickers=[ticker]).get_charts(period='d', chart_type='c', size='l', ta='0')
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(f'charts/{ticker}.png', 'rb'), )
        update.callback_query.edit_message_text(text=TICKER_MESSAGE, reply_markup=ticker_menu())
        return TICKER_MENU

    def weekly(self, update: Update, context: CallbackContext):
        ticker = context.user_data['selected_ticker']
        Screener(tickers=[ticker]).get_charts(period='w', chart_type='c', size='l', ta='0')
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(f'charts/{ticker}.png', 'rb'), )
        update.callback_query.edit_message_text(text=TICKER_MESSAGE, reply_markup=ticker_menu())
        return TICKER_MENU

    def market(self, update: Update, context: CallbackContext):
        update.callback_query.answer()
        text = 'Market...'
        update.callback_query.edit_message_text(text=text, reply_markup=market_menu())
        return CHOOSING_MARKET

    def last(self, update: Update, context: CallbackContext):
        update.callback_query.edit_message_text(text='Downloading tickers data...')
        helper.download_tickers_data(self.tickers)
        context.bot.send_photo(chat_id=self.chat_id, photo=open('test.png', 'rb'), reply_markup=market_menu())
        return CHOOSING_MARKET

    def premarket(self, update: Update, context: CallbackContext):
        update.callback_query.edit_message_text(text='Downloading pre-market data...')
        helper.download_premarket_data(self.tickers)
        context.bot.send_photo(chat_id=self.chat_id, photo=open('test.png', 'rb'), reply_markup=market_menu())
        return CHOOSING_MARKET

    def afterhours(self, update: Update, context: CallbackContext):
        update.callback_query.edit_message_text(text='Downloading after hours data...')
        helper.download_after_hours_data(self.tickers)
        context.bot.send_photo(chat_id=self.chat_id, photo=open('test.png', 'rb'), reply_markup=market_menu())
        return CHOOSING_MARKET

    def main(self):
        updater = Updater(API_KEY_LIVE)
        dispatcher = updater.dispatcher

        portfolio_conversation_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.portfolio, pattern=f'^{PORTFOLIO}$')],
            states={
                CHOOSING_PORTFOLIO: [
                    CallbackQueryHandler(self.print_tickers, pattern=f'^{PRINT_TICKERS}$'),
                    CallbackQueryHandler(self.add_ticker, pattern=f'^{ADD_TICKERS}$'),
                    CallbackQueryHandler(self.delete_ticker, pattern=f'^{DELETE_TICKERS}$'),
                    CallbackQueryHandler(self.save, pattern=f'^{SAVE_PORTFOLIO}$'),
                    CallbackQueryHandler(self.back, pattern=f'^{CHOOSING_MAIN}$'),
                ],
                ADDING_TICKERS: [MessageHandler(Filters.regex('\$[a-zA-Z]{1,4}(?=\,|$)'), self.input_tickers)],
                CHOOSING_TICKERS: [
                    CallbackQueryHandler(self.select_ticker, pattern='\$[A-Z]{1,4}'),
                    CallbackQueryHandler(self.back, pattern=CHOOSING_PORTFOLIO)
                ],
                TICKER_MENU: [
                    CallbackQueryHandler(self.info, pattern=TICKER_INFO),
                    CallbackQueryHandler(self.daily, pattern=TICKER_DAILY),
                    CallbackQueryHandler(self.weekly, pattern=TICKER_WEEKLY),
                    CallbackQueryHandler(self.back, pattern=CHOOSING_PORTFOLIO),
                ],
                TICKER_TO_DELETE: [CallbackQueryHandler(self.ticker_to_delete, pattern='\$[A-Z]{1,4}'),
                                   CallbackQueryHandler(self.back, pattern=f'^{CHOOSING_PORTFOLIO}$')]
            },
            fallbacks=[],
            map_to_parent={
                CHOOSING_MAIN: CHOOSING_MAIN,
                # CHOOSING_PORTFOLIO: CHOOSING_PORTFOLIO
            },
            allow_reentry=True
        )
        market_conversation_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.market, pattern=f'^{MARKET}$')],
            states={
                CHOOSING_MARKET: [
                    CallbackQueryHandler(self.last, pattern=f'^{MARKET_LAST}$'),
                    CallbackQueryHandler(self.premarket, pattern=f'^{MARKET_PM}$'),
                    CallbackQueryHandler(self.afterhours, pattern=f'^{MARKET_AH}$'),
                    CallbackQueryHandler(self.back, pattern=f'^{CHOOSING_MAIN}$'),
                ]
            },
            fallbacks=[],
            map_to_parent={
                CHOOSING_MAIN: CHOOSING_MAIN
            },
            allow_reentry=True
        )

        selection_handlers = [
            portfolio_conversation_handler,
            market_conversation_handler,
            CallbackQueryHandler(self.end, pattern=f'^{END}$')
        ]

        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={CHOOSING_MAIN: selection_handlers},
            fallbacks=[CallbackQueryHandler(self.end, pattern='End')],
            allow_reentry=True)

        dispatcher.add_handler(conversation_handler)
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    MyTelegramBot().main()
