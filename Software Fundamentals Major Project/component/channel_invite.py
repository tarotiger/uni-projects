# 'channel_invite' Invites a user (with user id u_id) to join a channel with ID channel_id. Once 
# invited the user is added to the channel immediately

from component.general import AccessError, ValueError, decode_token, id_to_user, valid_channel_id, valid_token, user_exists, user_in_channel, id_to_channel, authorise_token

'''
Invites a user (with user id u_id) to join a channel with ID channel_id. Once invited the user is added to the channel immediately
'''

@authorise_token
def channel_invite(token, channel_id, u_id):
    if not user_exists(u_id): 
        raise ValueError(description="u_id does not exist")
    else:
        channel_user = id_to_user(decode_token(token))
        channel = id_to_channel(channel_id)

        # authorised user is not part of the channel 
        if not user_in_channel(channel_user['u_id'], channel_id):
            raise AccessError(description="Authorised user is not a member of the channel")
        elif user_in_channel(u_id, channel_id):
            raise AccessError(description="User u_id is already a member of the channel")

        user = id_to_user(u_id)

        new_user = {
            'u_id': user['u_id'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
            'profile_img_url': user['profile_img_url'] 
        }

        # the user to be added is an admin and owner of slackr 
        if user['permission_id'] < 3: 
            channel['owner_members'].append(new_user)
            channel['all_members'].append(new_user)
        else:
            channel['all_members'].append(new_user)

        return {}
