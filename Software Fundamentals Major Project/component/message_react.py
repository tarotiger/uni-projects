# message_react marks the message as reacted
from component.general import decode_token, valid_message, user_in_channel, user_is_owner, AccessError, id_to_user, id_to_channel, id_to_message, valid_react, is_reacted, react_exists, ValueError, authorise_token

@authorise_token
def message_react(token, message_id, react_id):
    # provided message_id is invalid
    if not valid_message(message_id):
        raise ValueError(description="Message_id is invalid")
    
    # setup to get necessary parameters
    u_id = decode_token(token)
    message = id_to_message(message_id)
    channel_id = message['channel_id']
    
    # user is not part of the channel
    if not user_in_channel(u_id, channel_id):
        raise AccessError(description="User is not a member of the channel")
    # message react is invalid
    elif not valid_react(react_id):
        raise ValueError(description="Message react is invalid")
    # user has already reacted
    #elif is_reacted(u_id, message_id, react_id):
     #  raise ValueError(description="User has already reacted to message")

    # if the react_id already exists in the message dictionary
    if react_exists(react_id, message_id):
        # print("calling message_react")
        for react in message['reacts']:
            if react_id == react['react_id']:
                react['u_ids'].append(u_id)
                react['is_this_user_reacted'] = is_reacted(u_id, message_id, react_id)
    
    return {}
