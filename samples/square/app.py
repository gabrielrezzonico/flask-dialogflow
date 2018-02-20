from flask import Flask
from flask_dialogflow import DialogFlow
from flask_dialogflow import Response, TextMessage

app = Flask(__name__)
dialogflow = DialogFlow(app, '/webhook')

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

@dialogflow.action('math.square')
def square(number):
    answer = TextMessage(speech=str(num(number)*num(number)))
    response = Response()
    response.append(answer)
    return response

if __name__ == '__main__':
    PORT = 8090

    app.run(
        debug=True,
        port=PORT,
        host='0.0.0.0'
    )
