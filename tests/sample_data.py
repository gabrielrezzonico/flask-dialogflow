sample_request = {
    'id': '91b20aa5-9ccf-498d-8944-5d3a32ab1b37',
    'timestamp': '2018-02-17T11:26:58.76Z',
    'lang': 'en',
    'result': {
        'source': 'agent',
        'resolvedQuery': 'hello',
        'speech': '',
        'action': 'hello',
        'actionIncomplete': False,
        'parameters': {

        },
        'contexts': [

        ],
        'metadata': {
            'intentId': '6e4d06c7-bdd0-4e44-b130-a1169f2920c8',
            'webhookUsed': 'true',
            'webhookForSlotFillingUsed': 'false',
            'intentName': 'hello'
        },
        'fulfillment': {
            'speech': '',
            'messages': [
                {
                    'type': 0,
                    'speech': ''
                }
            ]
        },
        'score': 1.0
    },
    'status': {
        'code': 200,
        'errorType': 'success',
        'webhookTimedOut': False
    },
    'sessionId': '926e72d8-35ee-4640-8a69-a77c87f475f5'
}

sample_context = {
    "name": "some-context",
            "lifespan": 10,
            "parameters": {
                "key": "value"
            }
}
