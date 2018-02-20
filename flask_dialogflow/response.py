from .helpers import TypedList
from .messages import Message

class Response:
    """Flask-DialogFlow response. Just a list of Messages.

    Example:

        hello = TextMessage(speech="Hi!")
        response = Response()
        response.append(hello)
    """

    def __init__(self):
        self.messages = TypedList(Message)

    def append(self, msg):
        self.messages.append(msg)