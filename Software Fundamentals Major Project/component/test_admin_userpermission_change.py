# move outside of component to run tests 

from component.admin_userpermission_change import admin_userpermission_change
from component.auth_register import auth_register
from component.general import AccessError, ValueError
from component.data import get_data, reset_data
import pytest

def test_admin_userpermission_change():
    reset_data()
    
    ### SETUP ###
    # user who is the owner of slackr
    user1 = auth_register("dog@gmail.com", "12345", "Royce", "Huang")
    # user who is a member of slackr 
    user2 = auth_register("cat@gmail.com", "12345", "Kenneth", "Lu")
    # another user who is a member of a slackr 
    user3 = auth_register("duck@gmail.com", "12345", "Kevin", "Gu")

    token1 = user1['token']
    u_id1 = user1['u_id'] 

    token2 = user2['token']
    u_id2 = user2['u_id']

    token3 = user3['token']
    u_id3 = user3['u_id']

    ### SETUP END ###

    # Royce changes the permission of Kenneth to be an admin 
    admin_userpermission_change(token1, u_id2, 2)

    # Kenneth tries to change Royce's permissions 
    with pytest.raises(AccessError) as excinfo:
        admin_userpermission_change(token2, u_id1, 3)
    assert "Admin cannot change permission of owners" in str(excinfo.value)

    # Member tries to change the permission_id of Kenneth 
    with pytest.raises(AccessError) as excinfo:
        admin_userpermission_change(token3, u_id2, 2)
    assert "Authorised user is not an admin or owner" in str(excinfo.value)

    # Kenneth tries changes the permission of Kevin to an owner 
    with pytest.raises(AccessError) as excinfo:
        admin_userpermission_change(token2, u_id3, 1)
    assert "lower" in str(excinfo.value)

    # Kenneth changes the permission_id of Kevin Gu to 2 
    admin_userpermission_change(token2, u_id3, 2)

    # invalid token
    with pytest.raises(AccessError) as excinfo:
        admin_userpermission_change("1", u_id1, 3)
    assert "Token is invalid" in str(excinfo.value)

    # u_id does not exist in the server
    with pytest.raises(ValueError) as excinfo:
        admin_userpermission_change(token1, 10, 3)
    assert "u_id" in str(excinfo.value)

    # permission_id is not a valid id 
    with pytest.raises(ValueError) as excinfo:
        admin_userpermission_change(token1, 10, 4)
    assert "permission_id" in str(excinfo.value)
