import pytest
import json
from flask import Flask
from flask_dialogflow.dialogflow import DialogFlow
from flask_dialogflow.response import Response
from flask_dialogflow.messages import TextMessage
from sample_data import sample_request, sample_context

WEBHOOK_ENDPOINT = '/webhook'

response = Response()
text_msg = TextMessage(speech="Hi there!")
response.append(text_msg)

@pytest.fixture
def app():
    app = Flask(__name__)
    app.testing = True
    # create dialogflow
    dialogflow = DialogFlow(app, WEBHOOK_ENDPOINT)
    # attach a view function to an action
    @dialogflow.action('hello')
    def hello():
        dialogflow.context_out = sample_context
        return response

    return app

class TestMessages:

    def test_response(self, app):
        app_response = app.test_client().post(WEBHOOK_ENDPOINT, 
                        data=json.dumps(sample_request),
                        content_type='application/json')
        json_data = json.loads(app_response.data)
        assert "messages" in json_data
        assert "speech" in json_data["messages"][0]
        assert "type" in json_data["messages"][0]

    def test_context_out(self, app):
        app_response = app.test_client().post(WEBHOOK_ENDPOINT, 
                        data=json.dumps(sample_request),
                        content_type='application/json')
        json_data = json.loads(app_response.data)
        assert 'contextOut' in json_data
        assert json_data['contextOut'] == sample_context
        