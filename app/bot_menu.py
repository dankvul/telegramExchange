from app.utils import method_link
from config import Config
import requests

def start_bot():
    # set webhook:
    req = requests.get(url=method_link('setWebhook?url=' + Config.SERVER_URL))

    # getting status about current webhook
    req = requests.get(url=method_link('getWebhookInfo'))
    data = req.json()
    print('Current webhook info:\n{}'.format(data))