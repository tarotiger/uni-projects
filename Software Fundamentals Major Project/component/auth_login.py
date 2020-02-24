# stub function for 'auth_login' 

from component.general import valid_email, valid_password, valid_name, generate_token, email_exists, correct_password, generate_handle, encode_password, ValueError
from component.data import get_data, send_success

def auth_login(email, password):

    data = get_data()

    # encodes the password to compare with database
    password = encode_password(password)

    if not valid_email(email):
        raise ValueError(description="Email is invalid")
    elif not email_exists(email):
        raise ValueError(description="Email does not belong to a user")

    for user in data["users"]:
        if user["email"] == email and user["password"] == password:
            token = generate_token({
                'u_id': user['u_id']
            })

            data['tokens'].append(token)

            return {
                "u_id": user["u_id"],
                "token": token
            }
    
    raise ValueError(description="Password is incorrect")
