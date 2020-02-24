# 'user_profile' For a valid user, returns information about their email, first name, last name, and handle

from component.general import id_to_user, valid_token, decode_token, user_exists, AccessError, ValueError, authorise_token

'''
For a valid user, returns information about their email, first name, last name, and handle

user profile will return
{ u_id, email, name_first, name_last, handle_str, profile_img_url }
'''

@authorise_token
def user_profile(token, u_id):
    # user does not exist 
    if not user_exists(u_id):
        raise ValueError(description="No valid user with specified u_id found")
        
    user = id_to_user(u_id)

    display_info = {
        'u_id': u_id,
        'email': user['email'],
        'name_first': user['name_first'],
        'name_last': user['name_last'],
        'handle_str': user['handle_str'],
        'profile_img_url': user['profile_img_url']
    }

    return display_info
