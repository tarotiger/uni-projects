"""Flask server"""
import sys
from flask_cors import CORS
from json import dumps
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_mail import Mail, Message
from threading import Timer
from datetime import datetime, timezone 
from PIL import Image
import time 

from werkzeug.exceptions import HTTPException
from component.data import send_success, send_error, get_data
from component.auth_register import auth_register
from component.auth_login import auth_login
from component.auth_logout import auth_logout
from component.channels_create import channels_create
from component.channel_join import channel_join
from component.channel_leave import channel_leave
from component.channel_details import channel_details
from component.channels_listall import channels_listall
from component.channels_list import channels_list
from component.channel_addowner import channel_addowner
from component.channel_removeowner import channel_removeowner
from component.general import AccessError, ValueError, email_to_user, generate_token, id_to_user, update_profile_img
from component.channel_messages import channel_messages
from component.admin_userpermission_change import admin_userpermission_change
from component.message_send import message_send
from component.message_sendlater import msg_sendlater_data, msg_sendlater_channel
from component.user_profile_setname import user_profile_setname
from component.user_profile_setemail import user_profile_setemail
from component.user_profile_sethandle import user_profile_sethandle
from component.user_profiles_uploadphoto import user_profiles_uploadphoto
from component.message_send import message_send
from component.auth_passwordreset import reset_password
from component.message_edit import message_edit
from component.message_pin import message_pin
from component.message_unpin import message_unpin
from component.message_react import message_react
from component.message_unreact import message_unreact
from component.message_remove import message_remove
from component.channel_invite import channel_invite
from component.user_profile import user_profile
from component.standup_start import standup_start, standup_end
from component.standup_active import standup_active
from component.standup_send import standup_send
from component.search import search
from component.users_all import users_all

def defaultHandler(err):
    response = err.get_response()
    response.data = dumps({
        'code': err.code,
        'name': 'System Error',
        'message': err.get_description()
    })
    response.content_type = 'application/json'
    return response 

APP = Flask(__name__)
APP.config['TRAP_HTTP_EXCEPTIONS'] = True 
APP.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
APP.register_error_handler(Exception, defaultHandler)
CORS(APP)
# configuring email settings for pw reset
APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'happyjuice1531@gmail.com',
    MAIL_PASSWORD = "comp1531"
)


@APP.route('/echo/get', methods=['GET'])
def echo1():
    """ Description of function """
    return dumps({
        'echo' : request.args.get('echo'),
    })

@APP.route('/echo/post', methods=['POST'])
def echo2():
    """ Description of function """
    return dumps({
        'echo' : request.args.get('echo'),
    })

@APP.route('/getdata')
def errorcall():
    data = get_data() 
    return dumps(data) 

@APP.route('/auth/register', methods=['POST'])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    name_first = request.form.get("name_first");
    name_last = request.form.get("name_last");

    return dumps(auth_register(email, password, name_first, name_last))

@APP.route('/auth/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    return dumps(auth_login(email, password))

@APP.route('/auth/logout', methods=['POST'])
def logout():
    token = request.form.get('token')
    if (auth_logout(token) == True):
        return dumps({
            'is_success': True
        })
    else:
        return dumps({
            'is_success': False
        })

@APP.route('/channels/create', methods=['POST'])
def create_channel():
    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public')

    if is_public == 'false':
        is_public = False
    else:
        is_public = True
        
    return dumps(channels_create(token, name, is_public))

@APP.route('/channel/join', methods=['POST'])
def join_channel():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))

    return dumps(channel_join(token, channel_id))

@APP.route('/channel/invite', methods=['POST'])
def invite_channel():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))

    return dumps(channel_invite(token, channel_id, u_id))

@APP.route('/channel/leave', methods=['POST'])
def leave_channel():
    data = get_data()
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))

    return dumps(channel_leave(token, channel_id))

@APP.route('/channel/details', methods=['GET'])
def details_channel():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))

    return dumps(channel_details(token, channel_id))

@APP.route('/channels/listall', methods=['GET'])
def listall_channels():
    token = request.args.get('token')

    return dumps(channels_listall(token))

@APP.route('/channels/list', methods=['GET'])
def list_channels():
    token = request.args.get('token')

    return dumps(channels_list(token))


@APP.route('/channel/addowner', methods=['POST'])
def add_owner(): 
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))

    return dumps(channel_addowner(token, channel_id, u_id))

@APP.route('/channel/removeowner', methods=['POST']) 
def remove_owner():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))

    return dumps(channel_removeowner(token, channel_id, u_id))

@APP.route('/channel/messages', methods=['GET'])
def get_message():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))

    return dumps(channel_messages(token, channel_id, start))

@APP.route('/admin/userpermission/change', methods=['POST'])
def change_permission():
    token = request.form.get('token')
    u_id = int(request.form.get('u_id'))
    permission_id = int(request.form.get('permission_id'))

    return dumps(admin_userpermission_change(token, u_id, permission_id))

@APP.route('/user/profile/setname', methods=['PUT'])
def user_setname():
    token = request.form.get('token')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')

    return dumps(user_profile_setname(token, name_first, name_last))

@APP.route('/user/profile/setemail', methods=['PUT'])
def user_setemail():
    token = request.form.get('token')
    email = request.form.get('email')
    return dumps(user_profile_setemail(token, email))

@APP.route('/user/profile/sethandle', methods=['PUT'])
def user_sethandle():
    token = request.form.get('token')
    handle_str = request.form.get('handle_str')

    return dumps(user_profile_sethandle(token, handle_str))

@APP.route('/imgurl/<path:filename>', methods=['GET'])
def display_profile(filename):
    return send_file('./imgurl/' + filename)

@APP.route('/user/profiles/uploadphoto', methods=['POST'])
def user_uploadphoto():
    token = request.form.get('token')
    img_url = request.form.get('img_url')
    x_start = request.form.get('x_start')
    y_start = request.form.get('y_start')
    x_end = request.form.get('x_end')
    y_end = request.form.get('y_end')

    response = user_profiles_uploadphoto(token, img_url, int(x_start), int(y_start), int(x_end), int(y_end))
    filename = response['filename'].split("/")[-1].lower()
    server_img_url = request.host_url + "imgurl/" + filename
    print(server_img_url)
    update_profile_img(response['u_id'], server_img_url)

    return dumps({})

@APP.route('/users/all', methods=['GET'])
def all_users():
    token = request.args.get('token')

    return dumps(users_all(token))

@APP.route('/message/send', methods=['POST'])
def send_msg():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    message = request.form.get('message')

    return dumps(message_send(token, channel_id, message))

@APP.route('/message/edit', methods=['PUT'])
def edit_msg():
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    message = request.form.get('message')

    return dumps(message_edit(token, message_id, message))

@APP.route('/message/pin', methods=['POST'])
def pin_msg():
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))

    return dumps(message_pin(token, message_id))

@APP.route('/message/unpin', methods=['POST'])
def unpin_msg():
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))

    return dumps(message_unpin(token, message_id))

@APP.route('/message/react', methods=['POST'])
def react_msg():
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))

    return dumps(message_react(token, message_id, react_id))

@APP.route('/message/unreact', methods=['POST'])
def unreact_msg():
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))

    return dumps(message_unreact(token, message_id, react_id))

@APP.route('/message/remove', methods=['DELETE'])
def remove_msg():
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    
    return dumps(message_remove(token, message_id,))

@APP.route('/message/sendlater', methods=['POST'])
def sendLater():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    message = request.form.get('message')
    time_sent = float(request.form.get('time_sent'))
    
    message_id = msg_sendlater_data(token, channel_id, message, time_sent)

    return dumps(message_id)

@APP.route('/auth/passwordreset/request', methods=['POST'])
def send_email():
    email = request.form.get('email')
    u_id = email_to_user(email)

    if (u_id != False):
        # generate token based on u_id
        # append token to data['reset_codes']
        data = get_data()
        data['reset_codes'] = []
        reset_code = generate_token({
            'u_id': u_id
        })
        data['reset_codes'].append(reset_code)

        # generate email
        mail = Mail(APP)
        try:
            body = "Hello! Please enter the following reset code along with your new password on Slackr to reset your password: " + reset_code
            msg = Message("Your Slackr password reset",
                sender="happyjuice1531@gmail.com",
                recipients=[email])
            msg.body = body
            mail.send(msg)
            return dumps({})
        except Exception as e:
            return (str(e))
    else:
        raise ValueError(description="Invalid email")

@APP.route('/auth/passwordreset/reset', methods=['POST'])
def pw_reset():
    reset_code = request.form.get('reset_code')
    new_password = request.form.get('new_password')

    return dumps(reset_password(reset_code, new_password))

@APP.route('/user/profile', methods=['GET'])
def profile():
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))

    return dumps(user_profile(token, u_id))

@APP.route('/search', methods=['GET'])
def message_search():
    token = request.args.get('token')
    query_str = request.args.get('query_str')

    return dumps(search(token, query_str))

@APP.route('/standup/start', methods=['POST'])
def start_standup(): 
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    length = int(request.form.get('length'))

    response = standup_start(token, channel_id, length)

    return dumps(response)

@APP.route('/standup/active', methods=['GET'])
def standup_details():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))

    return dumps(standup_active(token, channel_id))


@APP.route('/standup/send', methods=['POST'])
def buffer_message():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    message = request.form.get('message')

    return dumps(standup_send(token, channel_id, message))

if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
