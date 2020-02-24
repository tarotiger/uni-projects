# function for 'channel_messages', allowing users to view up to last 50 messages in a channel

from component.general import AccessError, ValueError, decode_token, valid_channel_id, num_channel_messages, id_to_channel, user_in_channel, is_reacted, id_to_message, authorise_token

@authorise_token
def channel_messages(token, channel_id, start):
    # channel does not exit or start > total number of messages
    if not valid_channel_id(channel_id):
        raise ValueError(description="Channel does not exist ")
    # user is not part of the channel
    elif not user_in_channel(decode_token(token), channel_id):
        raise AccessError(description="User is not a member of the channel")
    
    u_id = decode_token(token)
    channel = id_to_channel(channel_id)

    # start is greater than the number of messages in the channel 
    if start > num_channel_messages(channel_id):
        raise ValueError(description="No more messages left in the channel")

    channel_message = {
        'messages': [], 
        'start': 0, 
        'end': 0 
    }

    # intialises the values of channel_messages 
    channel_message['start'] = start
    count = 0 
    message_list = channel['messages'][::-1]

    # loops through the reverse chronological messages and adds them to the list 
    for message in message_list: 
        # message is removed so will ignore it 
        if message['is_removed']:
            continue

        # ONLY VALID REACT_ID IS 1 (AS THE SPEC SAYS)
        if not is_reacted(u_id, message['message_id'], 1):
            message['reacts'][0]['is_this_user_reacted'] = False
            data_msg = id_to_message(message['message_id'])
            data_msg['reacts'][0]['is_this_user_reacted'] = False

        if count < start + 50 and count >= start and not message['is_removed']: 
            channel_message['messages'].append(message) 
        
        count = count + 1 

    # less than 50 messages have been returned 
    if len(channel_message['messages']) != 50:
        channel_message['end'] = -1 
    else: 
        channel_message['end'] = start + 50 

    return channel_message
