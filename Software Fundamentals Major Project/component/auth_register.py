# stub function for 'auth_register' 

from component.general import valid_email, valid_password, valid_name, generate_token, email_exists, generate_handle, encode_password, ValueError
from component.data import get_data, send_success

def auth_register(email, password, name_first, name_last): 
    data = get_data()

    if not valid_email(email):
        raise ValueError(description="Email is invalid")
    elif not valid_name(name_first) or not valid_name(name_last):
        raise ValueError(description="Name is invalid")
    elif email_exists(email):
        raise ValueError(description="Email is taken")
    elif not valid_password(password):
        raise ValueError(description="Password is too short")

    # by default user permission should be member 
    permission_id = 3 

    # if there are no users in the database the first user who signs up 
    # becomes the owner of slackr
    if len(data["users"]) == 0:
        permission_id = 1

    data["users"].append({
        "email": email,
        "u_id": len(data["users"]) + 1,
        "password": encode_password(password), 
        "name_first": name_first,
        "name_last": name_last,
        "handle_str": generate_handle(name_first + "_" + name_last),
        "permission_id": permission_id,
        "profile_img_url": "" 
    })

    token = generate_token({
        'u_id': len(data["users"])
    })

    data["tokens"].append(token) 

    return {
        "u_id": len(data["users"]),
        "token": token
    }
