# 'message_edit' update it's the text of a given message with new text

from component.general import decode_token, id_to_message, user_is_owner, user_has_permission, id_to_channel, AccessError, ValueError, valid_message, authorise_token
from component.data import get_data

@authorise_token
def message_edit(token, message_id, message):
    data = get_data()

    if not valid_message(message_id):
        raise ValueError(description="Message is invalid")

    u_id = decode_token(token)
    message_object = id_to_message(message_id)
    channel_id = message_object['channel_id']
    channel = id_to_channel(channel_id)

    if u_id == message_object["u_id"] or user_is_owner(channel_id, u_id) or user_has_permission(u_id):
        # updates message in the two locations message is stored
        
        # message is deleted if it is replaced with an empty string 
        if message == "":
            message_object['is_removed'] = True
        else :
            message_object['message'] = message

        for channel_message in channel['messages']:
            if message_id == channel_message['message_id']:
                # if string is empty, delete message
                if message == "":
                    channel_message['is_removed'] = True
                    break
                # replaces message with new message
                channel_message['message'] = message 

        return {}
    else:
        raise AccessError(description="User does not have suitable permission")
