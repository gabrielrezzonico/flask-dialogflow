# Flask-DialogFlow

Flask-DialogFlow is a Flask extension that helps you to build DialogFlow fulfillment webhooks.


## Installation

```bash
pip install flask-dialogflow
```

Flask-DialogFLow has the following dependencies:

* Flask version 0.10 or greater


## Minimal example

```python
from flask import Flask
from flask_dialogflow import DialogFlow, Response, TextMessage

app = Flask(__name__)
dialogflow = DialogFlow(app, '/webhook')

@dialogflow.action('hello')
def square(number):
    answer = TextMessage(speech="Hi there!")
    response = Response()
    response.append(answer)
    return response

if __name__ == '__main__':
    app.run(port=PORT)
```


