# general purpose functions for testing purposes

import re
from datetime import datetime, timezone 
import hashlib
import jwt
import random 
import requests
from flask import jsonify
from component.data import get_data, send_success, send_error
from werkzeug.exceptions import HTTPException


# HOW TO WRITE EXCEPTIONS: 
# e.g. BEFORE: raise ValueError("This is an exception")
# e.g. AFTER: raise ValueError(description="This is an exception")

# 'AccessError' returns an exception called AccessError
class AccessError(HTTPException):
    code = 430 
    message = 'AccessError'
# 'ValueError' returns an exception 
class ValueError(HTTPException): 
    code = 400 
    message = 'ValueError'

##################################################################################################
#### GENERAL 

# returns the user object from their given id 
def id_to_user(u_id):
    data = get_data()

    return data["users"][u_id - 1] 

# given a channel_id, return the channel object from get_data
def id_to_channel(channel_id):
    data = get_data()

    return data['channels'][channel_id - 1]

# given a message_id, return the message object from get_data
def id_to_message(message_id):
    data = get_data() 

    return data['messages'][message_id - 1]

# 'user_exists' returns true or false depending on if the user exists
def user_exists(u_id):
    data = get_data()

    for user in data['users']:
        if u_id == user['u_id']:
            return True 

    return False 

# 'user_has_permission' checks if a user is an admin or owner of slackr 
def user_has_permission(u_id):
    user = id_to_user(u_id)

    if user['permission_id'] < 3:
        return True 
    else:
        return False 

# 'less_than_char' returns a boolean if a string is under a certain amount of characters
def less_than_char(text, length):
    if len(text) > length:
        return False 
    else: 
        return True

def is_empty(string):
    if not string:
        return True
    else:
        return False

def email_to_user(email):
    data = get_data()

    for user in data['users']:
        if email == user['email']:
            return user['u_id']

    return False

# 'check_http_status' returns a boolean if the url returns a http status code 200 and if it matches the conventional url format, ending with '.jpg'
def check_http_status(img_url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)' 
        r'\.(?:jpg)$', re.IGNORECASE)
        
    match = re.match(regex, img_url)

    # does not match conventional url format
    if match is None:
        return False
    else:
        response = requests.head(img_url)
        if response.status_code == 200:
            return True
        else: 
            return False

def invalid_dimension(x_start, y_start, x_end, y_end):
    return (x_start > x_end or y_start > y_end or x_start < 0 or y_start < 0)

#### END GENERAL
##################################################################################################

##################################################################################################
#### AUTH FUNCTIONS 

# uses jwt to encode object to return a token  
def generate_token(non_encoded_obj):
    new_object = non_encoded_obj
    # creates a unique token even if one user logs in on multiple devices 
    new_object['extra'] = random.randint(1, 1000000)
    new_object['time'] = str(datetime.now().replace(tzinfo=timezone.utc))

    SECRET = 'happyjuice'
    encoded_object = jwt.encode(non_encoded_obj, SECRET, algorithm='HS256').decode('utf-8')
    return str(encoded_object)

# decodes a user token and returns the user id
# if token does not exist in the database (e.g. if the user logs out)
# decode_token will return a u_id -1 
def decode_token(token):
    SECRET = 'happyjuice'

    if not valid_token(token):
        return -1 
    
    decoded_object = jwt.decode(token, SECRET, algorithms=['HS256'])
    return decoded_object["u_id"]

# similar to decode_token, but doesn't check if its valid
# since that check was already run in auth_passwordreset.py
def decode_reset_code(token):
    SECRET = 'happyjuice'

    decoded_object = jwt.decode(token, SECRET, algorithms=['HS256'])
    return decoded_object["u_id"]

# if the token is not valid (does not exist in the database) 
def valid_token(token): 
    data = get_data()

    if token in data['tokens']:
        return True
    else:
        return False

# encodes password using SHA256 endcoding 
def encode_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 'generate_handle' creates a handle and appends digits if already taken 
def generate_handle(handle_str):
    data = get_data() 
    # number of repeated handles
    count = 0 

    for user in data["users"]:
        if user["handle_str"].startswith(handle_str):
            count += 1
    
    if (count == 0):
        return handle_str

    return handle_str + str(count)

# 'email_exists' confirms whether the email belongs to a user
def email_exists(email):
    data = get_data()

    for user in data["users"]:
        if (email == user["email"]):
            return True

    return False

# 'check_password' confirms whether password is linked with an email 
def correct_password(email, password):
    data = get_data()

    for user in data["users"]:
        if email == user["email"] and password == user["password"]:
            return True

    return False        

# 'valid_name' confirms whether 'name' is a name
def valid_name(name):
    regex_no_letter = '[^a-zA-Z]+'
    if re.search(regex_no_letter, name) or len(name) > 50 or len(name) < 1:
        return False
    else:
        return True

# 'valid_password' confirms if the password is at least five characters long
def valid_password(password):
    if len(password) >= 5:
        return True
    else:
        return False

# 'valid_email' confirms whether 'email' is an email
def valid_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):
        return True
    else:
        return False

# args[0] feels a bit hard-coded but seems like the only way to grab "token"
def authorise_token(function):
    def wrapper (*args, **kwargs):
        if decode_token(args[0]) == -1:
            raise AccessError(description="Token is invalid")

        return function(*args, **kwargs)
    return wrapper


#### END AUTH FUNCTIONS 
##################################################################################################

##################################################################################################
#### CHANNEL FUNCTIONS 

# 'user is owner' checks if a user is an owner of given channel using their user id
def user_is_owner(channel_id, u_id):
    channel = id_to_channel(channel_id)

    for owner in channel['owner_members']:
        if u_id == owner['u_id']:
            return True
    
    return False 

# 'user_in_channel' returns True or False if a user is in a given channel 
def user_in_channel(u_id, channel_id):
    # id_to_channel returns theh channel object
    # e.g. {'channel_id': 1, 'owner_members': [], 'all_members': []}
    channel = id_to_channel(channel_id)

    for member in channel['all_members']:
        if u_id == member['u_id']:
            return True 
    
    return False 

# 'valid_channel_id' returns a boolean by checking if channel id exists 
# is_public parameter shows if the current existing channels are public or private
def valid_channel_id(channel_id):
    data = get_data()

    for channel in data['channels']:
        if int(channel_id) == channel['channel_id']:
            return True 
    
    return False 

# 'num_channel_messages' returns the number of messages in the channel 
def num_channel_messages(channel_id):
    channel = id_to_channel(channel_id)
    count = 0 
    
    for message in channel['messages']:
        # adds count to the number of messages is the message isn't removed 
        if not message['is_removed']:
            count = count + 1
    
    return count 

def update_profile_img(u_id, img_url):
    data = get_data()

    user = id_to_user(u_id)
    user['profile_img_url'] = img_url

    for channel in data['channels']:
        if user_in_channel(u_id, channel['channel_id']):
            if user_is_owner(channel['channel_id'], u_id):
                for owner in channel['owner_members']:
                    if owner['u_id'] == u_id:
                        owner['profile_img_url'] = img_url
                        break 
            
            for member in channel['all_members']:
                if member['u_id'] == u_id:
                    member['profile_img_url'] = img_url
                    break 
    
    return 

#### END CHANNEL FUNCTIONS 
##################################################################################################

##################################################################################################
#### MESSAGE FUNCTIONS 

# 'valid_react' checks if a react is valid 
def valid_react(react_id):
    if react_id == 1:
        return True
    else:
        return False

def valid_message(message_id):
    data = get_data()

    for message in data['messages']:
        if message_id == message['message_id'] and not message['is_removed']:
            return True
    
    return False

def is_reacted(u_id, message_id, react_id):
    message = id_to_message(message_id)

    for react in message['reacts']:
        if react_id == react['react_id']:
            if u_id in react['u_ids']:
                return True
                
    return False 

def react_exists(react_id, message_id):
    message = id_to_message(message_id)

    for react in message['reacts']:
        if react_id == react['react_id']:
            return True 
    
    return False
    
#### END MESSAGE FUNCTIONS 
##################################################################################################
