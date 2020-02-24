#   basic stub function for channel_join.py
from component.general import AccessError, valid_token, decode_token, valid_channel_id, user_in_channel, id_to_user, id_to_channel, ValueError, authorise_token
from component.data import get_data

'''
Given a channel_id of a channel that the authorised user can join, adds them to that channel
ValueError - Channel (based on ID) does not exist
AccessError - channel_id refers to a channel that is private (when the authorised user is not an admin)
'''

@authorise_token
def channel_join(token, channel_id):
    data = get_data()
    user_id = decode_token(token)
    user_object = id_to_user(user_id)
    
    if not valid_channel_id(channel_id):
        #   channel_id does not exist
        raise ValueError(description="Channel does not match channel_id of existing channels")
    # silently fail if user is already part of the channel
    elif user_in_channel(user_id, channel_id):
        pass 
    else: 
        channel = id_to_channel(channel_id)

        if channel['is_public'] or user_object['permission_id'] < 3:
            user = {
                'name_first': user_object['name_first'],
                'name_last': user_object['name_last'],
                'u_id': user_object['u_id'],
                'profile_img_url': user_object['profile_img_url']
            }
            
            # if the user is a slackr admin or owner they are automatically made 
            # an owner 
            if user_object['permission_id'] < 3: 
                channel['all_members'].append(user)
                channel['owner_members'].append(user)
            else:
                channel['all_members'].append(user)
        else:
            #   if the channel_id of the channel intending to join is not PUBLIC, raise an AccessError
            raise AccessError(description="Channel_id provided is currently a private channel")
            
        return {}
