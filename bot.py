import logging
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from datetime import datetime
import re
import pandas as pd
import difflib
import warnings
import numpy as np
from difflib import SequenceMatcher


with open('TOKEN', 'r') as f:
    TOKEN = f.readline().replace('\n', '')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class Distraction:
    def __init__(self):
        self.current_word = None
        with open('words.txt', 'r') as f:
            self.all_words = f.read().split('\n')

    @staticmethod
    def similarity(a, b):
        return SequenceMatcher(None, a, b).ratio()


    def ask_question(self, update: Update, context: CallbackContext) -> int:
        logger.info("%s set users %s", update.message.from_user.first_name, update.message.text)
        self.current_word = np.random.choice(self.all_words)
        values = np.array([self.similarity(sorted(self.current_word), sorted(w)) for w in self.all_words])
        candidate_words = np.random.permutation(
            np.array(words)[np.argsort(values)[-10:]]
        ).reshape(-1, 2).tolist()
        cw_random = ''.join(np.random.permutation(list(current_word)))
        update.message.reply_text(
            'What is the original word of: ' + cw_random,
            reply_markup=ReplyKeyboardMarkup(
                all_options,
                one_time_keyboard=True,
                resize_keyboard=True,
            ),
        )
        return 'answer'

    def answer(self, update: Update, context: CallbackContext) -> str:
        logger.info("%s set users %s", update.message.from_user.first_name, update.message.text)
        if self.similarity(self.current_word, update.message.text) == 1:
            update.message.reply_text('Congratulations!')
        return 'question'

distraction = Distraction()


def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    text_non_command = Filters.text & ~Filters.command
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', distraction.ask_question),
        ],
        states={
            'question': [MessageHandler(text_non_command, distraction.ask_question)],
            'answer': [MessageHandler(text_non_command, distraction.answer)],
        },
        fallbacks=[
            CommandHandler('cancel', cancel),
            CommandHandler('start', start),
        ],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
