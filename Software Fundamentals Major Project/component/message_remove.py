# 'message_remove' given a message_id for a message, this message is removed from the channel

from component.general import AccessError, id_to_message, id_to_user, decode_token, user_is_owner, ValueError, valid_message, authorise_token
from component.data import get_data

@authorise_token
def message_remove(token, message_id):
    data = get_data()

    # message no longer exists and does not exist
    if not valid_message(message_id): 
        raise ValueError(description="Message based on id does not exist")

    user = id_to_user(decode_token(token))
    message = id_to_message(message_id)

    allowed_permission = [1, 2]

    if message['u_id'] == user['u_id'] or user['permission_id'] in allowed_permission or user_is_owner(message['channel_id'], user['u_id']):
        message['is_removed'] = True 
    else:
        raise AccessError(description="Authorised user does not have permission")

    # go through the database and tag the message as removed  
    for channel in data['channels']:
        for channel_message in channel['messages']:
            if channel_message['message_id'] == message_id:
                channel_message['is_removed'] = True
                
    return {}
        