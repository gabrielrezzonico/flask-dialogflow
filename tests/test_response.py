import pytest
import json
from flask_dialogflow.response import Response
from flask_dialogflow.messages import TextMessage, MessageEncoder

@pytest.fixture
def response():
    return Response()

MESSAGE="msg"

@pytest.fixture
def message():
    return TextMessage(speech=MESSAGE)

class TestResponse:
    def test_empty(self, response):
        assert len(response.messages) == 0
    
    def test_append(self, response, message):
        response.append(message)
        assert len(response.messages) == 1
        assert response.messages[0].speech == MESSAGE
        response.append(message)
        response.append(message)
        assert len(response.messages) == 3
    
    def test_serializable(self, response, message):
        response.append(message)
        text = json.dumps(response.__dict__ , cls=MessageEncoder)
        assert isinstance(text, str)