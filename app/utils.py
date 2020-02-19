import click
from config import Config
from .extensions import db
from flask.cli import with_appcontext
import requests
from datetime import datetime, timedelta
import matplotlib
import matplotlib.pyplot as plt


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()


def send_input_error(chat_id: int) -> None:
    message_body = 'Incorrect input format\n'\
                   'Examples:\n/exchange 10 USD to CAD or\n' \
                   '/exchange $10 to CAD\n' \
                   '/list or /lst\n' \
                   '/history USD/RUB for 123 days'
    params = {'chat_id': chat_id,
              'text': message_body}
    result = requests.get(url=method_link('sendMessage'), params=params)
    print(result)
    return None


def send_result_of_exchanging(_value: str, _from: str, _to: str, _rates: dict, chat_id: int) -> None:
    value: float = float(_value)
    result: float = (value / _rates[_from]) * _rates[_to]
    message: str = '{} {} in {} is {}'.format(value, _from, _to,
                                              f"{result:.{2}f}")
    req = requests.get(url=method_link('sendMessage'), params={'chat_id': chat_id, 'text': message})
    print(req)
    return None


def method_link(method_name: str) -> str:
    return 'https://api.telegram.org/bot{}/{}'.format(Config.TGBOT_TOKEN, method_name)


def send_error_api_history(chat_id: int) -> None:
    message = 'No exchange rate data or huge number of days for the selected currency.'
    req = requests.get(url=method_link('sendMessage'), params={'chat_id': chat_id, 'text': message})
    print(req)
    return None


def build_and_send(first_cur: str, second_cur: str, days: int, chat_id: int) -> None:
    first_cur = first_cur.upper()
    second_cur = second_cur.upper()
    if days > 10000000:
        return send_error_api_history(chat_id)
    try:
        req = requests.get(url='https://api.exchangeratesapi.io/history?start_at={}&end_at={}&base={}&symbols={}'.format(
            str((datetime.today() - timedelta(days=days)).date()), str(datetime.today().date()), first_cur.upper(),
            second_cur.upper()
        ))
    except requests.exceptions.RequestException as e:
        print(e)
        return send_error_api_history(chat_id)
    data: dict = req.json()
    if 'rates' not in data or not data['rates']:
        return send_error_api_history(chat_id)
    ay: list = []
    ax: list = []
    for i in data['rates']:
        ax.append(datetime.strptime(i, '%Y-%m-%d'))
    ax = sorted(ax)
    for i in range(len(ax)):
        ay.append(data['rates'][str(ax[i].date())][second_cur])
        ax[i] = matplotlib.dates.date2num(ax[i])
    fig, aax = plt.subplots()
    aax.plot(ax, ay, color="r")
    fig.autofmt_xdate()
    plt.title("{}/{}".format(first_cur, second_cur), fontsize=20)
    aax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%d:%m:%Y'))

    plt.grid()

    fig.savefig('./static/graph.png')
    files = {'photo': open('./static/graph.png', 'rb')}
    data = {'chat_id': chat_id}
    r = requests.post(url=method_link('sendPhoto'), files=files, data=data)
    print(r.json())
