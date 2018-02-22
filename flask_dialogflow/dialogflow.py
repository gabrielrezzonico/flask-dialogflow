import inspect
import json
from functools import wraps, partial
from flask import jsonify, make_response, request, Response as FlaskResponse

from .messages import MessageEncoder

# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as _app_stack
except ImportError:
    from flask import _request_ctx_stack as _app_stack

class DialogFlow:
    """
    The main entry point for the application.
    You need to initialize it with a Flask Application: ::

    >>> app = Flask(__name__)
    >>> dialogflow = DialogFlow(app, '/webhook')

    Flask-DialogFlow help you setup a webhook to be used with Google DialogFlow.
    It setups a flask route to be used as the fulfillment webhook route of your agent.
    It also maps actions your function to proccess that actions, this is done with a docorator (@dialogflow.action).

    Keyword Arguments:
        app {flask.Flask} -- the Flask application object (default: {None})
        route {str} -- Route at which DialogFlow is going to listen (default: {None})
        basic_auth_user {str} -- Username to use for basic auth. Basic auth is enabled if this is set (default: {None})
        basic_auth_pass {str} -- Password to use for basic auth. (default: {None})
    """
    def __init__(self, app=None, route=None, basic_auth_user=None,
            basic_auth_pass=None):
        self.app = app
        self._route = route
        self._action_to_function_map = {}
        self._basic_auth_user = basic_auth_user
        self._basic_auth_pass = basic_auth_pass
        self._default_view_func = None

        if app is not None:
            self.init_app(app, route, basic_auth_user, basic_auth_pass)

    def init_app(self, app, route=None, basic_auth_user=None,
                 basic_auth_pass=None):
        """
        The function that really init the app. Setups a flask route for the webhook.

        See also:
            Why an init_app function? See: http://flask.pocoo.org/docs/0.12/extensiondev/
        """

        self._route = route
        self.basic_auth_user = basic_auth_user
        self.basic_auth_user = basic_auth_pass
        app.add_url_rule(
            self._route, view_func=self._flask_view_func, methods=['POST'])

    @property
    def context_in(self):
        """This contains the context received from Google DialogFlow
        
        Returns:
            [list[context]] -- List of contexts
        """
        return getattr(_app_stack.top, '_dialogflow_context_in', [])

    @context_in.setter
    def context_in(self, value):
        _app_stack.top._dialogflow_context_in = value

    @property
    def original_request(self):
        """Contains the original request (1-click integrations providers data) received from Google DialogFlow
        
        Returns:
            [originalRequest -- originalRequest object
        """
        return getattr(_app_stack.top, '_dialogflow_original_request', [])

    @original_request.setter
    def original_request(self, value):
        _app_stack.top._dialogflow_original_request = value

    @property
    def intent(self):
        return getattr(_app_stack.top, '_dialogflow_intent', [])

    @intent.setter
    def intent(self, value):
        _app_stack.top._dialogflow_intent = value

    @property
    def context_out(self):
        return getattr(_app_stack.top, '_dialogflow_context_out', None)

    @context_out.setter
    def context_out(self, value):
        """Set the the output context that is going to be present in the response back to Google DialogFlow

        Arguments:
            value {context} -- The context to be sent

        Example:
            dialogflow.context_out = {
                "name": "some-context",
                "lifespan": 10,
                "parameters": {
                    "key": "value"
                }
            }
        """
        _app_stack.top._dialogflow_context_out = value

    def _flask_view_func(self, *args, **kwargs):
        """
        This is the internal Flask-DialogFlow view function that handles the flask route configured in init_app

        This function is called every time the "Webhook" flask route is fired.

        If basic_auth_user and _basic_auth_pass are set in Flask-Dialogflow, this function
        is going to perform a Basic Http Auth.

        It also parses the request object sent by Google Dialog FLow and create the intent and context_in objects 
        to be used by view functions.

        Finally it calls the decorated view function with the parameters received in the intent fired.

        """
        is_basic_auth_enabled = (self._basic_auth_user is not None)
        if (is_basic_auth_enabled and
            (request.authorization.username != self._basic_auth_user or
                request.authorization.password != self._basic_auth_pass)):
            return "", 401

        data_json = request.get_json(silent=True, force=True)

        action = data_json['result']['action']
        try:
            view_func = self._action_to_function_map[action]
        except KeyError:
            if self._default_view_func:
                view_func = self._default_view_func
            else:
                raise NotImplementedError('No registered view_func for action: "{}" and no default action specified.'.format(action))
        # update incoming information
        self.intent = data_json['result']['metadata']['intentName']
        self.context_in = data_json['result'].get('contexts', [])
        self.original_request = data_json.get('originalRequest', None)
        
        argspec = inspect.getargspec(view_func)
        arg_names = argspec.args
        arg_values = []
        params = data_json['result']['parameters']
        for arg_name in arg_names:
            value = params.get(arg_name)
            arg_values.append(value)

        view_func_with_args = partial(view_func, *arg_values)

        result = view_func_with_args()

        if result is not None:

            if self.context_out is not None:
                result.contextOut = self.context_out

            response = FlaskResponse(
                response=json.dumps(result.__dict__, cls=MessageEncoder),
                status=200,
                mimetype='application/json'
            )
            return response
        return "", 400

    def action(self, action_name):
        """ Decorator that registers an action's view function.

        Arguments:
            action_name {str} -- The name of the action to map with the decorated function.

        Example::
            >>> app = Flask(__name__)
            >>> dialogflow = DialogFlow(app, 'webhook/')
            >>> 
            >>> @dialogflow.action('core.onboarding')
            >>> def onboarding():
            >>>     answer = TextMessage(speech='Hello, World!')
            >>>     response = Response()
            >>>     response.append(answer)
            >>>     return response
        """

        def decorator(f):
            self._action_to_function_map[action_name] = f

            # see: https://docs.python.org/2/library/functools.html#functools.wraps
            @wraps(f)
            def wrapper(*args, **kw):
                self._flask_view_func(*args, **kw)
            return f
        return decorator


    def default(self, f):
        """
        Register a default function to be used when an unknown action is received.
        
        Arguments:
             {function} -- Function to be decorated
        Example::
            >>> app = Flask(__name__)
            >>> dialogflow = DialogFlow(app, 'webhook/')
            >>> 
            >>> @dialogflow.default
            >>> def default():
            >>>     answer = TextMessage(speech='Something happened!')
            >>>     response = Response()
            >>>     response.append(answer)
            >>>     return response
        """

        self._default_view_func = f

        @wraps(f)
        def wrapper(*args, **kw):
            self._flask_view_func(*args, **kw)
        return f