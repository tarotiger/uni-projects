# message_pin marks the message as unpinned
from component.general import decode_token, valid_message, user_in_channel, user_is_owner, AccessError, id_to_user, id_to_channel, id_to_message, ValueError, authorise_token

@authorise_token
def message_unpin(token, message_id):
    # unable to find message_id in database
    if not valid_message(message_id):
        raise ValueError(description="Message_id is invalid")
    
    # setup to get necessary parameters
    u_id = decode_token(token)
    message = id_to_message(message_id)
    channel_id = message['channel_id']
    channel = id_to_channel(channel_id)

    print("message id is ")
    print(message_id)
    
    # user not a member of the channel
    if not user_in_channel(u_id, channel_id):
        raise AccessError(description="User is not a member of the channel")
    # user is not an admin
    elif not user_is_owner(channel_id, u_id):
        raise ValueError(description="User does not have permission")
    # message already pinned
    elif message['is_pinned'] == False:
        raise ValueError(description="User has not currently pinned message")
    else:
        message['is_pinned'] = False
        for msg in channel['messages']:
            if msg['message_id'] == message_id:
                msg['is_pinned'] = False
        

        return {}