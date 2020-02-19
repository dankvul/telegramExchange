from app.model import update_rates, current_rates
import requests
from app.utils import method_link, send_input_error, send_result_of_exchanging, build_and_send, send_error_api_history


def list_of_rates(chat_id: int) -> None:
    print(update_rates())
    rates = current_rates()
    message_body = 'Current rates:\n'
    for i in rates:
        message_body += ('{}: {}\n'.format(i, f"{rates[i]:.{2}f}"))
    params = {'chat_id': chat_id,
              'text': message_body}
    result = requests.get(url=method_link('sendMessage'), params=params)
    print(result)


def exchange(text_message: str, chat_id: int) -> None:
    print(update_rates())
    text_message.strip()
    parsed_text_message: list = text_message.split()
    if len(parsed_text_message) == 5:
        parsed_text_message[2] = parsed_text_message[2].upper()
        parsed_text_message[4] = parsed_text_message[4].upper()
        parsed_text_message[3] = parsed_text_message[3].lower()
        try:
            float(parsed_text_message[1])
        except ValueError:
            return send_input_error(chat_id)
        rates = current_rates()
        if parsed_text_message[2] in rates and parsed_text_message[4] in rates and parsed_text_message[3] == 'to':
            send_result_of_exchanging(_value=parsed_text_message[1], _from=parsed_text_message[2],
                                      _to=parsed_text_message[4], chat_id=chat_id, _rates=rates)
        else:
            return send_input_error(chat_id)
    elif len(parsed_text_message) == 4:
        if parsed_text_message[1][0] == '$':
            parsed_text_message[1] = parsed_text_message[1].replace('$', '', 1)
        else:
            return send_input_error(chat_id)
        parsed_text_message[3] = parsed_text_message[3].upper()
        parsed_text_message[2] = parsed_text_message[2].lower()
        try:
            float(parsed_text_message[1])
        except ValueError:
            return send_input_error(chat_id)
        rates = current_rates()
        if parsed_text_message[3] in rates and parsed_text_message[2] == 'to':
            send_result_of_exchanging(_value=parsed_text_message[1], _from='USD',
                                      _to=parsed_text_message[3], chat_id=chat_id, _rates=rates)
        else:
            return send_input_error(chat_id)
    else:
        return send_input_error(chat_id)


def send_graph_image(text_message: str, chat_id: int) -> None:
    parsed_text_message: list = text_message.split()
    if len(parsed_text_message) == 5:
        parsed_text_message[1] = parsed_text_message[1].replace('/', '', 1)
        if len(parsed_text_message[1]) == 6 and parsed_text_message[2].lower() == 'for' \
                and parsed_text_message[4].lower() == 'days':
            first_cur = parsed_text_message[1][:3]
            second_cur = parsed_text_message[1][3:]
            try:
                int(parsed_text_message[3])
            except ValueError:
                return send_input_error(chat_id)
            if len(parsed_text_message[3]) > 8:
                return send_error_api_history(chat_id)
            build_and_send(first_cur, second_cur, int(parsed_text_message[3]), chat_id)
        else:
            return send_input_error(chat_id)
    else:
        return send_input_error(chat_id)
