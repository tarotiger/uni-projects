from component.general import AccessError, decode_token, id_to_user, authorise_token
from component.data import get_data

@authorise_token
def users_all(token):
    data = get_data()
    user_list = dict()
    user_list['users'] = []

    for user in data['users']:
        user_list['users'].append({
            'u_id': user['u_id'],
            'email': user['email'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
            'handle_str': user['handle_str'],
            'profile_img_url': user['profile_img_url']
        })

    return user_list

