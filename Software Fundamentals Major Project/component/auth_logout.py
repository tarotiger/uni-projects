# function for 'auth_logout'
# will invalidate the token for a logged-in user, by making it NULL

from component.data import get_data
from component.general import decode_token

def auth_logout(token):

    data = get_data()

    for t in data['tokens']:
        if t == token:
            print("Logging out user")
            data['tokens'].remove(t)
            return True    
        
    # if a valid token has not been given
    return False
