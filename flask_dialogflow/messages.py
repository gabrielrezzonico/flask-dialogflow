from enum import Enum
import json

class Platform(Enum):
    """Possible values of platform that Google DialogFlow (formerly Api.ai) supports
    """

    FACEBOOK = "facebook"
    KIK = "kik"
    LINE = "line"
    SKYPE = "skype"
    SLACK = "slack"
    TELEGRAM = "telegram"
    VIBER = "viber"

class MessageType(Enum):
    """Possible types of messages allowed by Google DialogFlow (formerly Api.ai)
    """
    TEXT = 0
    CARD = 1
    QUICK_REPLY = 2
    IMAGE = 3
    CUSTOM = 4
    
class Message:
    """Base class of all messages supported by Flask-Dialogflow. 

    See also: 
        https://docs.python.org/3/tutorial/classes.html#odds-and-ends
    """
    pass

class MessageEncoder(json.JSONEncoder):
    """ Custom Python JSON serializers for a Message object.

    Just call the __dict_ member of a Message object when serializing.

    Example:
        json.dumps(res.__dict__, cls=MessageEncoder)
    """
    def default(self, obj): # pylint: disable=E0202
        if isinstance(obj, Message):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class TextMessage(Message):
    """A Google Dialog Flow text message. 

    Arguments:
        speech {str} -- Text to be sent in the message.
    
    Keyword Arguments:
        platform {Platform} -- Specifies the target platform of the message (default: {None})
        
    See also: 
        https://dialogflow.com/docs/reference/agent/message-objects#text_response_2
    """
    def __init__(self, speech, platform=None):
        self.type = MessageType.TEXT.value
        self.speech = speech
        if platform is not None:
            self.platform = platform

class ImageMessage(Message):
    """A Google Dialog Flow image message. 

    Arguments:
        image_url {str} -- Url of the image
    
    Keyword Arguments:
        platform {Platform} -- Specifies the target platform of the message (default: {None})
    
    See also:
        https://dialogflow.com/docs/reference/agent/message-objects#image_message_object
    """
    def __init__(self, image_url, platform=None):
        self.type = MessageType.IMAGE.value
        self.imageUrl = image_url
        if platform is not None:
            self.platform = platform

class QuickReplyMessage(Message):
    """A Google Dialog Flow quick reply  message

    Arguments:
        title {str} -- Title of the quick reply
        replies {List[str]} -- List of strings corresponding to quick replies.
    
    Keyword Arguments:
        platform {Platform} -- Specifies the target platform of the message (default: {None})

    See also:
        https://dialogflow.com/docs/reference/agent/message-objects#quick_replies_message_object
    """
    def __init__(self, title, replies, platform=None):
        self.type = MessageType.QUICK_REPLY.value
        self.title = title
        self.replies = replies
        if platform is not None:
            self.platform = platform

class CardMessage(Message):
    """A Google Dialog Flow card message

    Arguments:
        buttons {list[str, str]} -- A list of buttons composed by text and postback string
        image_url {str} -- Url of the image to be used in the card
        title {str} -- Title of the card
        subtitle {str} -- Subtitle of the card
    
    Keyword Arguments:
        platform {Platform} -- Specifies the target platform of the message (default: {None})

    """
    def __init__(self, buttons, image_url, title, subtitle, platform=None):
        self.type = MessageType.QUICK_REPLY.value
        self.buttons = buttons
        self.imageUrl = image_url
        self.title = title
        self.subtitle = subtitle
        if platform is not None:
            self.platform = platform
