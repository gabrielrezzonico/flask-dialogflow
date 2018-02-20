import pytest
import json
from flask_dialogflow.messages import MessageEncoder, TextMessage, Message, \
        MessageType, ImageMessage


@pytest.fixture
def txt_msg():
    return TextMessage(speech="Hello!")

@pytest.fixture
def img_msg():
    return ImageMessage(image_url="example.com/1.png")

class TestTextMessages:
    def test_isinstance(self, txt_msg):
        assert isinstance(txt_msg, Message)
    
    def test_serializable(self, txt_msg):
        text = json.dumps(txt_msg , cls=MessageEncoder)
        assert isinstance(text, str)
        assert "Hello!" in text

    def test_type(self, txt_msg):
        assert set(["speech", "type"]).issubset(txt_msg.__dict__.keys())

class TestImageMessages:
    def test_isinstance(self, img_msg):
        assert isinstance(img_msg, Message)
    
    def test_serializable(self, img_msg):
        text = json.dumps(img_msg , cls=MessageEncoder)
        assert isinstance(text, str)

    def test_type(self, img_msg):
        assert set(["imageUrl", "type"]).issubset(img_msg.__dict__.keys())