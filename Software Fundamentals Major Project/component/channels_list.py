# Provide a list of all channels (and their associated details) that the authorised user is part of
from component.data import get_data
from component.general import decode_token, AccessError, authorise_token

# for each channel the user is part of, print the channel's name and channel_id
@authorise_token
def channels_list(token):
    data = get_data()
    
    # with the token given by the user and decode the token and check if that specific u_id belongs in any channel
    # if the u_id belonging in the channel is True, add it to a temporary return database and return the list

    channel_with_user = []
    user_id = decode_token(token)

    for channel_details in data['channels']:
        for channel in channel_details['all_members']:
            #   if the u_id of the user is present within the database
            if user_id == channel['u_id']:
                user_channels = {
                    'name': channel_details['name'],
                    'channel_id': channel_details['channel_id']
                }
                channel_with_user.append(user_channels)

    return {
            'channels': channel_with_user
        }

