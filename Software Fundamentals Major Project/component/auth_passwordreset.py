from component.general import email_to_user, ValueError, id_to_user, encode_password, valid_password, decode_reset_code
from component.data import get_data

def reset_password(reset_code, new_password):
    # check pw is a valid one, if not raise ValueError
    if not valid_password(new_password):
        raise ValueError(description="New password is invalid")

    # find reset_code in database, if not found raise ValueError
    # if found, get u_id from it, delete it and proceed
    # then, modify password in database
    data = get_data()
    success = 0
    for codes in data['reset_codes']:
        if reset_code == codes:
            success = 1
            data['reset_codes'].remove(codes)
            break

    if success == 0:
        print("the token was an invalid one")
        raise ValueError(description="Token supplied was not found in database")

    u_id = decode_reset_code(reset_code)
    user = id_to_user(u_id)
    encoded_pw = encode_password(new_password)
    user['password'] = encoded_pw

    return({})
    
    
