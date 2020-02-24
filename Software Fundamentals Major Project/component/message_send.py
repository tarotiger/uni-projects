# 'message_send' Send a message from authorised_user to the channel specified by channel_id

from component.general import AccessError, id_to_user, decode_token, valid_channel_id, user_in_channel, id_to_channel, ValueError, authorise_token
from datetime import datetime, timezone
from component.data import get_data

@authorise_token
def message_send(token, channel_id, message):
    data = get_data()

    if not valid_channel_id(channel_id):
        raise ValueError(description="channel_id does not exist")
    elif not user_in_channel(decode_token(token), channel_id):
        raise AccessError(description="User is not in channel")
    elif len(message) > 1000:
        raise ValueError(description="Message is more than 1000 characters")

    user = id_to_user(decode_token(token))
    channel = id_to_channel(channel_id)

    # initialise new message object 
    new_message = {
        'message_id': len(data['messages']) + 1, 
        'channel_id': channel_id,
        'message': message, 
        'is_pinned': False, 
        'u_id': user['u_id'],
        'time_created': datetime.utcnow().replace(tzinfo=timezone.utc).timestamp(), 
        'is_removed': False, 
        'reacts': [{
            'react_id': 1,
            'u_ids': [],
            'is_this_user_reacted': False
        }] 
    }

    # add the messages to the database
    data['messages'].append(new_message)
    channel['messages'].append(new_message)

    return { 'message_id': new_message['message_id'] }
