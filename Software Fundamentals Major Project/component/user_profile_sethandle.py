# stub function for user_profile_sethandle

from component.general import valid_token, decode_token, id_to_user, less_than_char, is_empty, ValueError, AccessError, authorise_token
from component.data import get_data

'''
This function updates an authorised user's handle

ValueError when handle_str is more than 20 characters
'''

@authorise_token
def user_profile_sethandle(token, handle_str):
    data = get_data()

    if not less_than_char(handle_str, 20):
        raise ValueError(description="Handle_str is greater than 20 characters")
    elif is_empty(handle_str):
        raise ValueError(description="User has supplied an empty string")

    user_object = id_to_user(decode_token(token))
    
    user_object['handle_str'] = handle_str
    return {}




