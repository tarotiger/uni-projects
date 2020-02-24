from json import dumps

data = {
    'users': [],
    'channels': [],
    'tokens': [],
    'messages': []
}

def get_data():
    global data 
    return data

def send_success(data):
    dumps(data)

def send_error(message):
    return dumps({
        '_error': message 
    })

def reset_data():
    global data 
    data = {
        'users': [],
        'channels': [],
        'tokens': [],
        'messages': []
    }
    return data 