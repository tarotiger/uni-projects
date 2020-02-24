from component.general import less_than_char, is_empty, decode_token, id_to_user, AccessError, ValueError, user_exists, user_in_channel, authorise_token
from component.data import get_data

'''
Stub function for user_profile_setname
Updates the authorised user's first and last name

ValueError when:
    name_first is more than 50 characters
    name_last is more than 50 characters

Takes in:
    (token, name_first, name_last)

Outputs:
    {} (nothing)
'''

@authorise_token
def user_profile_setname(token, name_first, name_last):
    data = get_data()

    if is_empty(name_first) or is_empty(name_last):
        raise ValueError(description="You must have both a first and last name")
    elif not less_than_char(name_first, 50):
        raise ValueError(description="First name cannot be over 50 characters in length")
    elif not less_than_char(name_last, 50):
        raise ValueError(description="Last name cannot be over 50 characters in length")
    
    user = id_to_user(decode_token(token))  
    
    user['name_first'] = name_first
    user['name_last'] = name_last 

    for channel in data['channels']:
        if user_in_channel(user['u_id'], channel['channel_id']):
            # loops through the members in a channel and sets the 
            # users name to their new name 
            for member in channel['all_members']:
                if member['u_id'] == user['u_id']:
                    member['name_first'] = name_first
                    member['name_last'] = name_last 
            
            for member in channel['owner_members']:
                if member['u_id'] == user['u_id']:
                    member['name_first'] = name_first
                    member['name_last'] = name_last 

    return {}
                

    




