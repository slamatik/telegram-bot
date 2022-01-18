import logging
from keyboards import *
from api_key import API_KEY
from telegram import Update
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, ConversationHandler, \
    CallbackContext, MessageHandler, Filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(text='Main Menu', reply_markup=main_menu())
    return CHOOSING_MAIN


def end(update: Update, context: CallbackContext):
    update.callback_query.answer()
    update.callback_query.edit_message_text(text='Bye')
    return END


def portfolio(update: Update, context: CallbackContext):
    update.callback_query.answer()
    update.callback_query.edit_message_text(text='Portfolio Menu', reply_markup=portfolio_menu())
    return CHOOSING_PORTFOLIO


def market(update: Update, context: CallbackContext):
    update.callback_query.answer()
    update.callback_query.edit_message_text(text='Market Menu', reply_markup=market_menu())
    return CHOOSING_MARKET


def main():
    updater = Updater(API_KEY)
    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING_MAIN: [
                CallbackQueryHandler(portfolio, pattern=f'^{PORTFOLIO}$'),
                CallbackQueryHandler(market, pattern=f'^{MARKET}$'),
            ],

        },
        fallbacks=[CallbackQueryHandler(end, pattern='End')],
        allow_reentry=True)

    dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
