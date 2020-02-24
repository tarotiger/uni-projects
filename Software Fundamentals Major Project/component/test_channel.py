# tests for channel functions 

import pytest
from component.general import AccessError, ValueError, num_channel_messages
from component.auth_login import auth_login
from component.auth_register import auth_register
from component.channels_create import channels_create
from component.channels_list import channels_list
from component.channels_listall import channels_listall
from component.channel_invite import channel_invite
from component.channel_join import channel_join 
from component.channel_leave import channel_leave
from component.channel_details import channel_details
from component.admin_userpermission_change import admin_userpermission_change
from component.channel_addowner import channel_addowner
from component.channel_removeowner import channel_removeowner
from component.data import get_data, reset_data
from component.message_send import message_send
from component.channel_messages import channel_messages
from component.message_react import message_react
from component.message_remove import message_remove


# FULL COVERAGE FOR: 
# - channel_join 
# - channels_create
# - channels_list 
# - channels_listall
# - channel_messages
def test_channel_create():
    reset_data()

    ##################################################################################
    #### SETUP 

    # owner user 
    response1 = auth_register("dog@gmail.com", "12345", "Royce", "Huang")
    # admin user
    response2 = auth_register("cat@gmail.com", "12345", "Kenneth", "Lu")
    # ordinary user 
    response3 = auth_register("duck@gmail.com", "12345", "Haley", "Gu")
    response4 = auth_register("bunny@gmail.com", "12345", "Kevin", "Wu")

    token1 = response1['token']
    u_id1 = response1['u_id']

    token2 = response2['token']
    u_id2 = response2['u_id']

    admin_userpermission_change(token1, u_id2, 2)

    token3 = response3['token']
    u_id3 = response3['u_id']

    token4 = response4['token']
    u_id4 = response4['u_id']

    #### END
    ##################################################################################

    channel_response1 = channels_create(token1, "Public Channel", True)
    channel_response2 = channels_create(token1, "Private Channel", False)

    # inputting an invalid token when creating a channel
    with pytest.raises(AccessError):
        channels_create("not a token", "Channel", True)

    # creating a channel name longer than 20 characters 
    with pytest.raises(ValueError):
        channels_create(token1, "This channel name is longer than twenty characters", True)
    
    # list all channels, check amount of channels
    all_channels = channels_listall(token1)
    assert len(all_channels['channels']) == 2, "There should be two channels since the user created them both"

    # invalid token 
    with pytest.raises(AccessError):
        channel_join("notatoken", channel_response1['channel_id'])
    
    # invalid channel id 
    with pytest.raises(ValueError):
        channel_join(token2, 100)
    
    # admin user joins a private channel
    channel_join(token2, channel_response2['channel_id'])

    # nothing will happen when the user tries to join the channel again
    channel_join(token2, channel_response2['channel_id'])

    # a normal user tries to join a private channel
    with pytest.raises(AccessError):
        channel_join(token3, channel_response2['channel_id'])

    # a normal user joins a public channel
    channel_join(token4, channel_response1['channel_id'])

    # listing channels with invalid tokens 
    with pytest.raises(AccessError): 
        channels_listall("not a token")

    # listing channels with invalid tokens 
    with pytest.raises(AccessError): 
        channels_list("not a token")

    # list channels users are part of 
    channel_list1 = channels_list(token1)
    channel_list2 = channels_list(token2)
    channel_list3 = channels_list(token3)
    channel_list4 = channels_list(token4)

    assert len(channel_list1['channels']) == 2
    assert len(channel_list2['channels']) == 1
    assert len(channel_list3['channels']) == 0
    assert len(channel_list4['channels']) == 1

def test_channel_invite():
    reset_data()

    ##################################################################################
    #### SETUP 

    # owner user 
    response1 = auth_register("dog@gmail.com", "12345", "Royce", "Huang")
    # admin user
    response2 = auth_register("cat@gmail.com", "12345", "Kenneth", "Lu")
    # ordinary user 
    response3 = auth_register("duck@gmail.com", "12345", "Haley", "Gu")
    response4 = auth_register("bunny@gmail.com", "12345", "Kevin", "Wu")

    token1 = response1['token']
    u_id1 = response1['u_id']

    token2 = response2['token']
    u_id2 = response2['u_id']

    admin_userpermission_change(token1, u_id2, 2)

    token3 = response3['token']
    u_id3 = response3['u_id']

    token4 = response4['token']
    u_id4 = response4['u_id']

    #### END
    ##################################################################################

    channel_response1 = channels_create(token1, "Public Channel", True)
    channel_response2 = channels_create(token4, "Private Channel", False)

    channel_list1 = channels_list(token1)
    channel_list3 = channels_list(token3)

    assert len(channel_list1['channels']) == 1
    assert len(channel_list3['channels']) == 0

    # owner user attempts to invite a user to a channel they're not part of 
    with pytest.raises(AccessError):
        channel_invite(token1, channel_response2['channel_id'], u_id2)
     
    # token is invalid 
    with pytest.raises(AccessError):
        channel_invite("not a token", channel_response1['channel_id'], u_id2)

    # user does not exist 
    with pytest.raises(ValueError):
        channel_invite(token4, channel_response2['channel_id'], 100)

    channel_invite(token4, channel_response2['channel_id'], u_id2)

    channel_list2 = channels_list(token2);

    assert len(channel_list2['channels']) == 1

    # channel owner attempts to invite a user who's already in the channel 
    with pytest.raises(AccessError):
        channel_invite(token4, channel_response2['channel_id'], u_id2)

    channel_invite(token4, channel_response2['channel_id'], u_id3)

    channel_list3 = channels_list(token3)

    assert len(channel_list3['channels']) == 1

def test_channel_owner():
    reset_data()

    ##################################################################################
    #### SETUP 

    # owner user 
    response1 = auth_register("dog@gmail.com", "12345", "Royce", "Huang")
    # admin user
    response2 = auth_register("cat@gmail.com", "12345", "Kenneth", "Lu")
    # ordinary user 
    response3 = auth_register("duck@gmail.com", "12345", "Haley", "Gu")
    response4 = auth_register("bunny@gmail.com", "12345", "Kevin", "Wu")
    # ordinary user that is not going to part of a channel
    response5 = auth_register("imhungry@gmail.com", "12345", "Fatty", "Hungry")

    token1 = response1['token']
    u_id1 = response1['u_id']

    token2 = response2['token']
    u_id2 = response2['u_id']

    admin_userpermission_change(token1, u_id2, 2)

    token3 = response3['token']
    u_id3 = response3['u_id']

    token4 = response4['token']
    u_id4 = response4['u_id']

    token5 = response5['token']
    u_id5 = response5['u_id']

    #### END
    ##################################################################################
 
    channel_response = channels_create(token1, "Public Channel", True)
    channel_id = channel_response['channel_id']

    channel_join(token3, channel_id)

    # a member is trying to make a user the owner of the channel even though they're 
    # not in the channel 
    with pytest.raises(AccessError):
        channel_addowner(token4, channel_id, u_id3)

    # invalid channel id 
    with pytest.raises(ValueError):
        channel_addowner(token1, 100, u_id3)

    # invalid token
    with pytest.raises(AccessError):
        channel_addowner("not a token", channel_id, u_id3)

    channel_join(token4, channel_id)

    # owner is trying to make himself the owner again 
    with pytest.raises(ValueError):
        channel_addowner(token1, channel_id, u_id1)
    
    # makes a user who is not part of the channel an owner of the channel 
    channel_addowner(token1, channel_id, u_id4)

    # new owner makes the member of the channel an owner 
    channel_addowner(token4, channel_id, u_id3)

    # invalid channel id 
    with pytest.raises(ValueError):
        channel_removeowner(token1, 100, u_id3)

    # invalid token
    with pytest.raises(AccessError):
        channel_removeowner("not a token", channel_id, u_id3)

    # user not part any channels in slackr attempts to removes another member from ownership 
    with pytest.raises(AccessError):
        channel_removeowner(token5, channel_id, u_id3)

    # a member of the channel removes another member from ownership 
    channel_removeowner(token3, channel_id, u_id4)

    # a member of the channel attmepts to remove the actual owner from the channel
    with pytest.raises(AccessError):
        channel_removeowner(token3, channel_id, u_id1)

    # the member who has just been removed tries to remove ownership from the user who removed 
    # him 
    with pytest.raises(AccessError):
        channel_removeowner(token4, channel_id, u_id3)
    
    # removes ownership from a user who already isn't an owner 
    with pytest.raises(ValueError):
        channel_removeowner(token3, channel_id, u_id4)

    # owner removes ownership from admin/owner of slackr 
    with pytest.raises(AccessError):
        channel_removeowner(token3, channel_id, u_id1)

    channel_removeowner(token1, channel_id, u_id1) 

    # admin/owner of slackr removes ownership from the other owner 
    channel_removeowner(token1, channel_id, u_id3)

    # admin/owner of slackr adds themselves as the owner again 
    channel_addowner(token1, channel_id, u_id1)

def test_channel_leave():
    reset_data()

    ##################################################################################
    #### SETUP 

    # owner user 
    response1 = auth_register("dog@gmail.com", "12345", "Royce", "Huang")
    # admin user
    response2 = auth_register("cat@gmail.com", "12345", "Kenneth", "Lu")
    # ordinary user 
    response3 = auth_register("duck@gmail.com", "12345", "Haley", "Gu")
    response4 = auth_register("bunny@gmail.com", "12345", "Kevin", "Wu")
    response5 = auth_register("snake@gmail.com", "12345", "Snakes", "Lol")

    token1 = response1['token']
    u_id1 = response1['u_id']

    token2 = response2['token']
    u_id2 = response2['u_id']

    admin_userpermission_change(token1, u_id2, 2)

    token3 = response3['token']
    u_id3 = response3['u_id']

    token4 = response4['token']
    u_id4 = response4['u_id']

    token5 = response5['token']
    u_id5 = response5['u_id']

    #### END
    ##################################################################################

    channel_response = channels_create(token1, "Public Channel", True)
    channel_id = channel_response['channel_id']

    channel_join(token3, channel_id)
    
    # invalid channel id 
    with pytest.raises(ValueError):
        channel_leave(token1, 100)

    # invalid token
    with pytest.raises(AccessError):
        channel_leave("not a token", channel_id)

    # invalid token
    with pytest.raises(AccessError):
        channel_details("not a token", channel_id)
    
    # invalid channel id 
    with pytest.raises(ValueError):
        channel_details(token1, 100)

    detail_response = channel_details(token1, channel_id)

    assert len(detail_response['all_members']) == 2
    assert len(detail_response['owner_members']) == 1 

    # member leaves the channel 
    channel_leave(token3, channel_id)

    detail_response = channel_details(token1, channel_id)

    assert len(detail_response['all_members']) == 1
    assert len(detail_response['owner_members']) == 1 

    # owner leaves the channel 
    channel_leave(token1, channel_id)

    # user no longer part of the channel and is unable to see channel_details 
    with pytest.raises(AccessError):
        channel_details(token3, channel_id)

    # nothing happens if a member tries to leave again
    channel_leave(token3, channel_id)

    # user that was never part of the channel calls channel_leave()
    # this should silently fail, since the user was never part of the channel
    channel_leave(token5, channel_id)

    channels_list_response1 = channels_list(token3)
    channels_list_response2 = channels_list(token1)
    
    # confirms the users have left the channels 
    assert len(channels_list_response1['channels']) == 0 
    assert len(channels_list_response2['channels']) == 0

def test_channel_messages():
    reset_data()
    data = get_data()

    ##################################################################################
    #### SETUP 

    # owner user 
    response1 = auth_register("dog@gmail.com", "12345", "Royce", "Huang")
    # admin user
    response2 = auth_register("cat@gmail.com", "12345", "Kenneth", "Lu")
    # ordinary user 
    response3 = auth_register("duck@gmail.com", "12345", "Haley", "Gu")

    token1 = response1['token']
    u_id1 = response1['u_id']

    token2 = response2['token']
    u_id2 = response2['u_id']

    admin_userpermission_change(token1, u_id2, 2)

    token3 = response3['token']
    u_id3 = response3['u_id']

    # create some messages!
    channel_response = channels_create(token1, "Public Channel", True)
    channel_id = channel_response['channel_id']
    message1 = 'You the real MVP'
    message2 = 'I love python!'

    for i in range(0, 20):
        message_send(token1, channel_id, message1)

    #### END
    ##################################################################################

    channel_join(token3, channel_id)
    
    # invalid channel id 
    with pytest.raises(ValueError):
        channel_messages(token1, 100, 0)

    # invalid token
    with pytest.raises(AccessError):
        channel_messages("not a token", channel_id, 0)

    # invalid token
    with pytest.raises(AccessError):
        channel_messages("not a token", channel_id, 0)

    # user is not part of the channel
    with pytest.raises(AccessError):
        channel_messages(token2, channel_id, 0)

    # start value is greater than number of actual messages in channel
    with pytest.raises(ValueError):
        channel_messages(token3, channel_id, 9001)

    assert channel_messages(token3, channel_id, 0)['end'] == -1
    assert len(channel_messages(token3, channel_id, 0)['messages']) == 20

    # TODO: test if after a message is removed it returns correct end?
    message_remove(token1, 1)
    assert len(channel_messages(token3, channel_id, 0)['messages']) == 19
    assert num_channel_messages(channel_id) == 19

    # generating more messages (now more than 50 total in channel)
    for i in range(0, 50):
        message_send(token3, channel_id, message2)

    assert num_channel_messages(channel_id) == 69
    # test if start return value is correct
    assert channel_messages(token3, channel_id, 10)['end'] == 60
    assert len(channel_messages(token3, channel_id, 10)['messages']) == 50 

    assert channel_messages(token3, channel_id, 60)['end'] == -1
    assert len(channel_messages(token3, channel_id, 60)['messages']) == 9

    for i in range (0, 100):
        message_send(token3, channel_id, message2)

    message_react(token3, 10, 1)

    # accumulates all the messages in a channel 
    start = 0
    loops = 0 
    count = 0
    while start != -1: 
        message_response = channel_messages(token3, channel_id, start)
        count += len(message_response['messages'])
        loops = loops + 1 
        start = message_response['end']

    # ensures that 169 messages read
    assert count == 169
    # ensures that it took four iterations to grab all the messages
    assert loops == 4 
    # if start is now -1 at the end, it means that we are finished looping the while loop 
    assert start == -1
