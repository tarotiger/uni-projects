# 'channel_create' creates a channel given a token and name 
from component.general import decode_token, AccessError, id_to_user, ValueError, authorise_token
from component.data import get_data

'''
Creates a new channel with that name that is either a public or private channel
ValueError - name is more than 20 characters long
'''

'''
---  Maybe missing testing for if the parameter 'is_public' is anything other than a boolean ---
'''

@authorise_token
def channels_create(token, name, is_public):
    data = get_data() 
    # returns the user id from the given token 
    u_id = decode_token(token)

    if len(name) > 20: 
        raise ValueError(description="Channel name is over 20 characters")

    # returns the user object from the database based on the id 
    user = id_to_user(u_id)

    # details for user in the channel
    channel_user = {
        'u_id': u_id,
        'name_first': user['name_first'],
        'name_last': user['name_last'],
        'profile_img_url': user['profile_img_url']
    }

    # initialise channel object 
    new_channel = {
        'name': name, 
        'channel_id': len(data["channels"]) + 1, 
        'is_public': is_public, 
        'owner_members': [],
        'all_members': [],
        'messages': [],
        'standup': {
            'is_running': False, 
            'time_finish': None 
        },
        'messages_buffer': '' 
    }

    # add user creating the channels as the owner 
    new_channel['owner_members'].append(channel_user)
    new_channel['all_members'].append(channel_user)

    # adds the channel to the database 
    data["channels"].append(new_channel)

    return {
        'channel_id': new_channel['channel_id']
    }
        