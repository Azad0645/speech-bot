import os
import logging
from dotenv import load_dotenv

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from dialogflow_client import detect_intent


logger = logging.getLogger(__file__)


def main() -> None:
    """Start the bot."""
    load_dotenv()

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.ERROR,
    )
    logger.setLevel(logging.INFO)

    project_id = os.environ["DIALOGFLOW_PROJECT_ID"]
    tg_token = os.environ["TG_TOKEN"]


    def start(update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        user = update.effective_user
        update.message.reply_markdown_v2(
            fr'Hi {user.mention_markdown_v2()}\!',
            reply_markup=ForceReply(selective=True),
        )


    def help_command(update: Update, context: CallbackContext) -> None:
        """Send a message when the command /help is issued."""
        update.message.reply_text('Help!')


    def handle_message(update: Update, context: CallbackContext) -> None:
        user_text = update.message.text
        tg_user_id = update.effective_user.id
        session_id = f"tg-{tg_user_id}"

        result = detect_intent(project_id, session_id, user_text, "ru")
        reply = result.fulfillment_text

        if not reply:
            reply = "Я пока не знаю, что ответить"

        update.message.reply_text(reply)


    updater = Updater(tg_token, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()