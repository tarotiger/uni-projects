# 'admin_userpermission_change.py' Given a User by their user ID, set their permissions to new 
# permissions described by permission_id

from component.general import decode_token, id_to_user, user_exists, AccessError, ValueError, authorise_token
from component.data import get_data

@authorise_token
def admin_userpermission_change(token, u_id, permission_id):
    data = get_data() 

    permission_id_list = [1, 2, 3]

    # permission_id does not refer to a valid id
    if not permission_id in permission_id_list:
        raise ValueError(description="permission_id does not refer to a valid id")
    # u_id provided cannot be found in the database 
    elif not user_exists(u_id):
        raise ValueError(description="u_id does not exist")

    # auth_user refers to the user who the token refers to 
    auth_user = id_to_user(decode_token(token))
    # user refers to the user who's permission is being changed
    user = id_to_user(u_id)

    # auth_user is a member
    if auth_user['permission_id'] == 3:
        raise AccessError(description="Authorised user is not an admin or owner")
    # auth_user is an admin and admins cannot change the permission of owners 
    elif auth_user['permission_id'] == 2 and user['permission_id'] == 1: 
        raise AccessError(description="Admin cannot change permission of owners")
    # authorised user cannot give the user a lower permission_id than their own 
    elif auth_user['permission_id'] > permission_id:
        raise AccessError(description="Authorised user cannot give another user a lower permission_id than their own")

    # authorised user has the permission to change the users permission_id
    for user in data['users']:
        if u_id == user['u_id']:
            user['permission_id'] = permission_id

    return {}
