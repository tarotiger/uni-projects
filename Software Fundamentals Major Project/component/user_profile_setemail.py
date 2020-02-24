# stub function for user_profile_setemail

from component.data import get_data
from component.general import ValueError, email_exists, valid_email, decode_token, id_to_user, authorise_token

'''
Updates the authorised user's email address

ValueError when:
Email entered is not valid
Email address is already being used by another user
'''

@authorise_token
def user_profile_setemail(token, email):
    data = get_data()
    user_id = decode_token(token)

    if not valid_email(email):
        raise ValueError(description="Email entered is invalid")
    elif email_exists(email):
        raise ValueError(description="Email has already been taken by an existing user")
    
    user_object = id_to_user(user_id)

    user_object['email'] = email
    return {}
    
