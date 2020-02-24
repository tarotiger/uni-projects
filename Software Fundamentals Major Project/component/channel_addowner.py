# 'channel_addowner' Make user with user id u_id an owner of this channel

from component.general import AccessError, decode_token, valid_channel_id, id_to_channel, id_to_user, user_is_owner, ValueError, authorise_token

@authorise_token
def channel_addowner(token, channel_id, u_id):
    if not valid_channel_id(channel_id):
        raise ValueError(description="Channel ID does not exist")
    else: 
        owner_user = id_to_user(decode_token(token))

        # user who is trying to add owner is not an owner 
        if not user_is_owner(channel_id, owner_user['u_id']) and owner_user['permission_id'] == 3:
            raise AccessError(description="Authorised user does not have permission")
        # user is trying to add a user who is already an owner
        elif user_is_owner(channel_id, u_id):
            raise ValueError(description="User u_id is already an owner")

        channel = id_to_channel(channel_id)
        user = id_to_user(u_id)

        # new owner object to be added to the channel 
        new_owner = {
            'u_id': u_id,
            'name_first': user['name_first'],
            'name_last': user['name_last'],
            'profile_img_url': user['profile_img_url']
        }
        
        channel['owner_members'].append(new_owner)

        return {}
