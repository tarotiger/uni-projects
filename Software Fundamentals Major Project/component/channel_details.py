# stub function for 'channel_details'
from component.general import decode_token, valid_channel_id, user_in_channel, id_to_channel, AccessError, ValueError, authorise_token
from component.data import get_data

'''
Given a Channel with ID channel_id that the authorised user is part of, provide basic details about the channel

return { name, owner_members, all_members }
'''

# if the channel_invite is true, therefore the user is part of the channel and thus is an authorised user of the channel
@authorise_token
def channel_details(token, channel_id):
    data = get_data()

    u_id = decode_token(token)

    if not valid_channel_id(channel_id):
        raise ValueError(description="Channel id does not exist")
    # user is not in channel
    elif not user_in_channel(u_id, channel_id):
        raise AccessError(description="User does not have access to channel")
    else:
        # if the channel id and user has an authorised token to enter channel
        # allow them to have access to the details fo the channel

        #   return a channel object from which we can access
        channel = id_to_channel(channel_id)
        #   create the channel with the data we need to return
        returned_channel = {
            'name': channel['name'],
            'owner_members': [],
            'all_members': []
        }
        
        #   going through the returned channel_object and append the relevant data
        for owner in channel['owner_members']:
            user = {
                'u_id': owner['u_id'],
                'name_first': owner['name_first'],
                'name_last': owner['name_last'],
                'profile_img_url': owner['profile_img_url']
            }

            returned_channel['owner_members'].append(user)

        for member in channel['all_members']:
            user = {
                'u_id': member['u_id'],
                'name_first': member['name_first'],
                'name_last': member['name_last'],
                'profile_img_url': member['profile_img_url']
            }

            returned_channel['all_members'].append(user)

        return returned_channel