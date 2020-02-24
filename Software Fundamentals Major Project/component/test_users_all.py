import pytest 
from component.users_all import users_all
from component.general import AccessError, ValueError
from component.auth_register import auth_register
from component.auth_logout import auth_logout
from component.data import reset_data, get_data

def test_users_all():
    reset_data()

    # logging in 
    response1 = auth_register("email@gmail.com", "12345", "Royce", "Huang")

    token1 = response1['token']

    assert(users_all(token1) == {
        'users': [
            {
                'u_id': 1,
                'email': 'email@gmail.com',
                'name_first': 'Royce',
                'name_last': 'Huang',
                'handle_str': 'Royce_Huang',
                'profile_img_url': "" 
            }
        ]
    })

    # invalid token
    with pytest.raises(AccessError):
        users_all("not a token")

    response2 = auth_register("dog@gmail.com", "12345", "Kenneth", "Lu")

    token2 = response2['token']

    assert(users_all(token2) == {
        'users': [
            {
                'u_id': 1,
                'email': 'email@gmail.com',
                'name_first': 'Royce',
                'name_last': 'Huang',
                'handle_str': 'Royce_Huang',
                'profile_img_url': "" 
            },

            {
                'u_id': 2,
                'email': 'dog@gmail.com',
                'name_first': 'Kenneth',
                'name_last': 'Lu',
                'handle_str': 'Kenneth_Lu',
                'profile_img_url': "" 
            }
        ]
    })
    