#   function for channel_leave.py
'''
Given a channel ID, the user removed as a member of this channel
ValueError - Channel_id does not exist
'''
from component.general import valid_channel_id, decode_token, user_in_channel, AccessError, id_to_channel, ValueError, authorise_token

@authorise_token
def channel_leave(token, channel_id):
    user_id = decode_token(token)

    #   if the channel_id does not exist
    if not valid_channel_id(channel_id):
        raise ValueError(description="Channel id does not exist")
    #   if user is not in channel
    elif not user_in_channel(user_id, channel_id):
        pass
    #   if the token is valid and the channel_id exists,
    else:
        #   go into the database and into all_members key of that specific channel
        channel = id_to_channel(channel_id)
        #   loop through all_members of the channel and deletes the user
        for i in range(len(channel['all_members'])):
            if channel['all_members'][i]['u_id'] == user_id:
                del channel['all_members'][i]
                break
        
        #   loop through owner_members of the channel and deletes the user 
        for i in range(len(channel['owner_members'])):
            if channel['owner_members'][i]['u_id'] == user_id:
                del channel['owner_members'][i]
                break 
        
        return {}

