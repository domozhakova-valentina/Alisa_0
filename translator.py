from flask import Flask, request, jsonify
import logging
from deep_translator import MyMemoryTranslator # надо установить модуль deep-translator

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)
    logging.info(f'Response:  {response!r}')
    return jsonify(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет! Я умею переводить слова с русского на английский. ' \
                                  'Для этого напиши: "Переведи слово: *слово*'
        return

    if 'переведи слово:' in req['request']['original_utterance'].lower():
        s = req['request']['original_utterance']
        s = s[s.find(':') + 1:]
        translated = MyMemoryTranslator(source='russian', target='en-IN').translate(s)
        res['response']['text'] = translated
        return

    else:
        res['response']['text'] = 'Не поняла запрос'
        return


if __name__ == '__main__':
    app.run()
