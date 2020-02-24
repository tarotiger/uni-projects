# This has two functions
# One to append to data['messages'] as soon as message/sendlater/ is called and,
# Another to append to the channel messages list to actually display after.

from component.general import AccessError, id_to_user, decode_token, valid_channel_id, user_in_channel, id_to_channel, ValueError, authorise_token
from datetime import datetime, timezone, timedelta
from component.data import get_data
from threading import Timer 

# function to check if parameters are valid 
# for message/sendlater
# it also appends to data['messages'] for msg_sendlater_channel
@authorise_token
def msg_sendlater_data(token, channel_id, message, time_to_send):
    data = get_data()

    if not valid_channel_id(channel_id):
        raise ValueError(description="channel_id does not exist")
    elif not user_in_channel(decode_token(token), channel_id):
        raise AccessError(description="User is not in channel")
    elif len(message) > 1000:
        raise ValueError(description="Message is more than 1000 characters")

    sec_until_send = time_to_send - datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()

    if sec_until_send < 0:
        raise ValueError(description="You can only schedule messages to send in the future")

    user = id_to_user(decode_token(token))
    channel = id_to_channel(channel_id)
    new_message = {
        'message_id': len(data['messages']) + 1, 
        'channel_id': channel_id,
        'message': message, 
        'is_pinned': False, 
        'u_id': user['u_id'],
        'time_created': (datetime.now() + timedelta(seconds=sec_until_send)).replace(tzinfo=timezone.utc).timestamp(), 
        'is_removed': False, 
        'reacts': [{
                'react_id': 1,
                'u_ids': [],
                'is_this_user_reacted': False
            }] 
    }

    data['messages'].append(new_message)

    print(sec_until_send)

    # starting a timer
    timer = Timer(sec_until_send, msg_sendlater_channel, args=[channel_id, message])
    timer.start() # after time_to_send seconds, msg_sendlater_channel will be called

    return { 'message_id': new_message['message_id'] }

def msg_sendlater_channel(channel_id, message):
    data = get_data()
    channel = id_to_channel(channel_id)        

    # loop thru list from start, take from data['messages'] if msg_id and
    # if the channel_id matches the message's id and channel_id
    for msg in data['messages']:
        # verify that the message stored in the array is the message that was sent
        if channel_id == msg['channel_id'] and message == msg['message']:
            # add the messages to the channel database
            channel['messages'].append(msg)
            return { 'message_id': msg['message_id'] }
        