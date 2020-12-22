import requests
import logging
import os

BOT_TOKEN = '1470632683:AAFCBt3J2WfI4XoxsyabUVkFNWAKnD6FWAk'
BOT_CHATID = '-499896050'


def telegram_bot_sendtext(bot_token, bot_chatid, bot_message):
    send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatid}&parse_mode=Markdown&text={bot_message}'
    response = requests.get(send_text)

    return response.json()


class TelegramHandler(logging.Handler):
    def __init__(self, *args, bot_token, bot_chatid, app_name, **kwargs):
        logging.Handler.__init__(self, *args, **kwargs)
        self.bot_token = bot_token
        self.bot_chatid = bot_chatid
        self.app_name = app_name

    def emit(self, record):
        text = f'*{self.app_name}*: {record.msg}'
        telegram_bot_sendtext(self.bot_token, self.bot_chatid, text)


def get_logger(bot_token=BOT_TOKEN, channel=BOT_CHATID, app_name='Default'):
    if channel is None:
        raise ValueError('Please declare the target channel at Telegram!')

    telegram_handler = TelegramHandler(bot_token=bot_token, bot_chatid=channel, app_name=app_name, level=logging.DEBUG)

    # Create logger
    logger = logging.getLogger()
    logger.addHandler(telegram_handler)

    return logger


# decorator for catching exceptions and throwing errors
def report(logger, terminate=True):
    def real_decorator(method):
        def wrapper(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except Exception as e:
                logger.error(str(e))
                if terminate:
                    exit()

        return wrapper

    return real_decorator
