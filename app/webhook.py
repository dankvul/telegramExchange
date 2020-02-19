from flask import Blueprint
from flask import request
from .controller import list_of_rates, exchange, send_graph_image
from config import Config
from .controller import send_input_error
import re


webhook = Blueprint('webhook', __name__)


@webhook.route('/{}'.format(Config.TGBOT_TOKEN), methods=['POST'])
def get_updates():
    body = request.get_json()
    print('Json has been got:\n{}'.format(body))

    if 'edited_message' in body:
        send_input_error(body['edited_message']['chat']['id'])
        return 'Another UPDATE read'

    if 'text' not in body['message']:
        send_input_error(body['message']['chat']['id'])
        return 'Another UPDATE read'
    chat_id: int = body['message']['chat']['id']
    text_message = body['message']['text']
    if text_message == '/list' or text_message == '/lst':
        list_of_rates(chat_id)
    elif re.match(r'/exchange', text_message):
        exchange(text_message, chat_id)
    elif re.match(r'/history', text_message):
        send_graph_image(text_message, chat_id)
    else:
        send_input_error(chat_id)
    return 'Another UPDATE read'
