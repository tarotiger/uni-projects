# tests for message functions

import pytest
from component.general import AccessError, ValueError, id_to_channel, num_channel_messages, id_to_message, user_in_channel
from component.auth_register import auth_register
from component.channels_create import channels_create
from component.admin_userpermission_change import admin_userpermission_change
from component.channel_join import channel_join
from component.channel_leave import channel_leave
from component.message_send import message_send
from component.message_edit import message_edit
from component.message_pin import message_pin
from component.message_unpin import message_unpin
from component.message_react import message_react
from component.message_unreact import message_unreact
from component.message_remove import message_remove
from component.message_sendlater import msg_sendlater_data, msg_sendlater_channel
from component.data import get_data, reset_data
from datetime import datetime, timezone, timedelta 
from time import sleep

def count_reacts(message_id, react_id):
    message = id_to_message(message_id)
    count = 0
    for reacts in message['reacts']:
        for users in reacts['u_ids']:
            count += 1
    return count

def test_message_send():
    reset_data()

    ##################################################################################
    #### SETUP 

    # owner user 
    response1 = auth_register("dog@gmail.com", "12345", "Royce", "Huang")
    # ordinary user 
    response2 = auth_register("cat@gmail.com", "12345", "Kenneth", "Lu")

    token1 = response1['token']
    u_id1 = response1['u_id']

    token2 = response2['token']
    u_id2 = response2['u_id']

    channel_response1 = channels_create(token1, 'Channel', True)

    total_messages = num_channel_messages(channel_response1['channel_id'])
    assert total_messages == 0

    #### END
    ##################################################################################


    # authorised user attempts to post to a channel they are not part of
    with pytest.raises(AccessError):
        message_send(token2, channel_response1['channel_id'], "message")
    assert total_messages == 0


    # invalid token
    with pytest.raises(AccessError):
        message_send("notatoken", channel_response1['channel_id'], "message")
    assert total_messages == 0

    # invalid channel id
    with pytest.raises(ValueError):
        message_send(token1, 100, "message")
    assert total_messages == 0
    
    # message more than 1000 characters
    with pytest.raises(ValueError):
        message_send(token1, channel_response1['channel_id'], "this message is longer that 1000 characters  this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters  this message is longer that 1000 characters  this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters  this message is longer that 1000 characters  this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters  this message is longer that 1000 characters  this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters!!")
    assert total_messages == 0

    #successful message
    message_send(token1, channel_response1['channel_id'], 'Hello this is my first message!')
    total_messages = num_channel_messages(channel_response1['channel_id'])
    assert total_messages == 1

# some of sendlater's functionality relies upon contacting the server and starting a serverside flask timer
# this cannot be tested, so we are manually calling msg_sendlater_channel in order to make sure the actual functions are working
def test_message_sendlater():
    reset_data()

    ##################################################################################
    #### SETUP 

    # owner user 
    response1 = auth_register("dog@gmail.com", "12345", "Royce", "Huang")
    # ordinary user 
    response2 = auth_register("cat@gmail.com", "12345", "Kenneth", "Lu")

    token1 = response1['token']
    u_id1 = response1['u_id']

    token2 = response2['token']
    u_id2 = response2['u_id']

    channel_response1 = channels_create(token1, 'Channel', True)

    total_messages = num_channel_messages(channel_response1['channel_id'])
    assert total_messages == 0

    time_now = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    # going to send a message ONE second later
    time_sent = time_now + 1

    #### END
    ##################################################################################


    # authorised user attempts to post to a channel they are not part of
    with pytest.raises(AccessError):
        msg_sendlater_data(token2, channel_response1['channel_id'], "message", time_sent)
    assert total_messages == 0

    # invalid token
    with pytest.raises(AccessError):
        msg_sendlater_data("notatoken", channel_response1['channel_id'], "message", time_sent)
    assert total_messages == 0

    # invalid channel id
    with pytest.raises(ValueError):
        msg_sendlater_data(token1, 100, "message", time_sent)
    assert total_messages == 0
    
    # message more than 1000 characters
    with pytest.raises(ValueError):
        msg_sendlater_data(token1, channel_response1['channel_id'], "this message is longer that 1000 characters  this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters  this message is longer that 1000 characters  this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters  this message is longer that 1000 characters  this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters  this message is longer that 1000 characters  this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters!!", time_sent)
    assert total_messages == 0

    # user 1 attempts to schedule a message in the past Steins Gate style
    with pytest.raises(ValueError):
        msg_sendlater_data(token1, channel_response1['channel_id'], 'Hello this is my first message!', time_sent - 2)
    assert total_messages == 0

    # successful message by user 1
    msg_sendlater_data(token1, channel_response1['channel_id'], 'Hello this is my first message!', time_sent)
    assert total_messages == 0
    sleep(1.2) # kept this at 1.2 to avoid slight variation in timer messing up tests
    assert num_channel_messages(channel_response1['channel_id']) == 1

    # user 2 joins, schedules a message to send later then leaves!
    channel_join(token2, channel_response1['channel_id'])
    assert user_in_channel(u_id2, channel_response1['channel_id'])
    msg_sendlater_data(token2, channel_response1['channel_id'], 'Fuck u kenneth', time_sent + 1)
    # asserting that no NEW messages have been sent (apart from the one in the prev test)
    assert num_channel_messages(channel_response1['channel_id']) == 1
    channel_leave(token2, channel_response1['channel_id'])
    assert user_in_channel(u_id2, channel_response1['channel_id']) == False
    sleep(1.2)
    assert num_channel_messages(channel_response1['channel_id']) == 2

def test_message_edit():
    reset_data()

    ##################################################################################
    #### SETUP 

    # owner user 
    response1 = auth_register("dog@gmail.com", "12345", "Royce", "Huang")
    # ordinary user 
    response2 = auth_register("cat@gmail.com", "12345", "Kenneth", "Lu")

    token1 = response1['token']
    u_id1 = response1['u_id']

    token2 = response2['token']
    u_id2 = response2['u_id']

    channel_response1 = channels_create(token1, 'Channel', True)

    channel_join(token2, channel_response1['channel_id'])

    message_response1 = message_send(token1, channel_response1['channel_id'], 'Hello this is my first message!')
    message_response2 = message_send(token2, channel_response1['channel_id'], 'Please don\'t remove this message')
    
    total_messages = num_channel_messages(channel_response1['channel_id'])
    assert total_messages == 2


    #### END
    ##################################################################################

    # Testing invalid token
    with pytest.raises(AccessError):
        message_edit("invalid token", message_response2['message_id'], "new message")
    assert id_to_message(message_response2['message_id'])['message'] == "Please don't remove this message"

    # Testing invalid message_id
    with pytest.raises(ValueError):
        message_edit(token1, "not a valid message_id", "new message")
    assert id_to_message(message_response2['message_id'])['message'] == "Please don't remove this message"

    # Kenneth tries to edit a message Royce sent
    with pytest.raises(AccessError):
        message_edit(token2, message_response1['message_id'], "new message")
    assert id_to_message(message_response2['message_id'])['message'] == "Please don't remove this message"

    # asserts the message stored in channel is not changed
    assert id_to_channel(id_to_message(message_response2['message_id'])['channel_id'])['messages'][1]['message'] == "Please don't remove this message"

    # Royce edits his own message
    message_edit(token1, message_response1['message_id'], "Hello this is my first edited message!")
    assert id_to_message(message_response1['message_id'])['message'] == "Hello this is my first edited message!"
    assert id_to_channel(id_to_message(message_response1['message_id'])['channel_id'])['messages'][0]['message'] == "Hello this is my first edited message!"

    # Kenneth edits his own message with an empty string, which deletes the message
    message_edit(token2, message_response2['message_id'], "")
    assert id_to_message(message_response2['message_id'])['is_removed'] == True 
    assert id_to_channel(id_to_message(message_response2['message_id'])['channel_id'])['messages'][1]['is_removed'] == True 

def test_message_remove():
    reset_data()

    ##################################################################################
    #### SETUP 

    # owner user 
    response1 = auth_register("dog@gmail.com", "12345", "Royce", "Huang")
    # ordinary user 
    response2 = auth_register("cat@gmail.com", "12345", "Kenneth", "Lu")

    token1 = response1['token']
    u_id1 = response1['u_id']

    token2 = response2['token']
    u_id2 = response2['u_id']

    channel_response1 = channels_create(token1, 'Channel', True)

    channel_join(token2, channel_response1['channel_id'])

    message_response1 = message_send(token1, channel_response1['channel_id'], 'Hello this is my first message!')
    message_response2 = message_send(token2, channel_response1['channel_id'], 'Please don\'t remove this message')
    
    total_messages = num_channel_messages(channel_response1['channel_id'])
    assert total_messages == 2

    #### END
    ##################################################################################

    # Testing invalid token
    with pytest.raises(AccessError):
        message_remove("invalid token", message_response2['message_id'])
    assert total_messages == 2

    # Testing invalid message_id
    with pytest.raises(ValueError):
        message_remove(token1, "not a valid message_id")
    assert total_messages == 2

    # Royce removes the message sent by Kenneth 
    message_remove(token1, message_response2['message_id'])
    total_messages = num_channel_messages(channel_response1['channel_id'])
    assert total_messages == 1

    # Kenneth attempts to remove Royce's message 
    with pytest.raises(AccessError):
        message_remove(token2, message_response1['message_id'])
    total_messages = num_channel_messages(channel_response1['channel_id'])
    assert total_messages == 1

    # Royce attempts to remove Kenneth's message again 
    with pytest.raises(ValueError):
        message_remove(token1, message_response2['message_id'])
    total_messages = num_channel_messages(channel_response1['channel_id'])
    assert total_messages == 1

    # Royce removes his own message 
    message_remove(token1, message_response1['message_id'])
    total_messages = num_channel_messages(channel_response1['channel_id'])
    assert total_messages == 0

def test_message_pin():
    reset_data()

    ##################################################################################
    #### SETUP 

    # owner user 
    response1 = auth_register("dog@gmail.com", "12345", "Royce", "Huang")
    # ordinary user 
    response2 = auth_register("cat@gmail.com", "12345", "Kenneth", "Lu")

    token1 = response1['token']
    u_id1 = response1['u_id']

    token2 = response2['token']
    u_id2 = response2['u_id']

    channel_response1 = channels_create(token1, "Channel", True)

    channel_join(token2, channel_response1['channel_id'])

    message_response1 = message_send(token1, channel_response1['channel_id'], 'Hello this is my first message!')
    message1 = id_to_message(message_response1['message_id'])
    message_response2 = message_send(token2, channel_response1['channel_id'], 'Please don\'t remove this message')
    message2 = id_to_message(message_response2['message_id'])

    total_messages = num_channel_messages(channel_response1['channel_id'])
    assert total_messages == 2
    
    #### END
    ##################################################################################

    # Testing invalid token
    with pytest.raises(AccessError):
        message_pin("invalid token", message_response2['message_id'])
    assert message1["is_pinned"] == False

    # Testing invalid message_id
    with pytest.raises(ValueError):
        message_pin(token1, "invalid message_id")
    assert message1["is_pinned"] == False

    # Royce pins message sent by Kenneth
    message_pin(token1, message_response2['message_id'])
    assert message2["is_pinned"] == True

    # Royce attempts to pin the message he already pinned
    with pytest.raises(ValueError):
        message_pin(token1, message_response2['message_id'])
    assert message2["is_pinned"] == True

    # Kenneth (who is not an owner) attempts to pin a message
    with pytest.raises(ValueError):
        message_pin(token2, message_response1['message_id'])
    assert message1["is_pinned"] == False

    channel_leave(token2, channel_response1['channel_id'])

    # Kenneth (who is not a member of the channel) attempts to pin a message
    with pytest.raises(AccessError):
        message_pin(token2, message_response1['message_id'])
    assert message1["is_pinned"] == False

def test_message_unpin():
    reset_data()

    ##################################################################################
    #### SETUP 

    # owner user 
    response1 = auth_register("dog@gmail.com", "12345", "Royce", "Huang")
    # ordinary user 
    response2 = auth_register("cat@gmail.com", "12345", "Kenneth", "Lu")

    token1 = response1['token']
    u_id1 = response1['u_id']

    token2 = response2['token']
    u_id2 = response2['u_id']

    channel_response1 = channels_create(token1, "Channel", True)

    channel_join(token2, channel_response1['channel_id'])

    message_response1 = message_send(token1, channel_response1['channel_id'], 'Hello this is my first message!')
    message1 = id_to_message(message_response1['message_id'])
    message_response2 = message_send(token2, channel_response1['channel_id'], 'Please don\'t remove this message')
    message2 = id_to_message(message_response2['message_id'])

    total_messages = num_channel_messages(channel_response1['channel_id'])
    assert total_messages == 2
    
    #### END
    ##################################################################################

    # Testing invalid token
    with pytest.raises(AccessError):
        message_unpin("invalid token", message_response2['message_id'])
    assert message1["is_pinned"] == False

    # Testing invalid message_id
    with pytest.raises(ValueError):
        message_unpin(token1, "invalid message_id")
    assert message1["is_pinned"] == False

    # Royce attempts to unpin the message he already unpinned
    with pytest.raises(ValueError):
        message_unpin(token1, message_response2['message_id'])
    assert message2["is_pinned"] == False  

    # Kenneth (who is not an owner) attempts to unpin a message
    with pytest.raises(ValueError):
        message_unpin(token2, message_response1['message_id'])
    assert message1["is_pinned"] == False

    # Royce pins message sent by Kenneth
    message_pin(token1, message_response2['message_id'])
    assert message2["is_pinned"] == True

    channel_leave(token2, channel_response1['channel_id'])

    # Kenneth (who is not a member of the channel) attempts to unpin a message
    with pytest.raises(AccessError):
        message_unpin(token2, message_response1['message_id'])
    assert message1["is_pinned"] == False

    # Royce unpins message sent by Kenneth
    message_unpin(token1, message_response2['message_id'])
    assert message2["is_pinned"] == False

def test_message_react():
    reset_data()

    ##################################################################################
    #### SETUP 

    # owner user 
    response1 = auth_register("dog@gmail.com", "12345", "Royce", "Huang")
    # ordinary user 
    response2 = auth_register("cat@gmail.com", "12345", "Kenneth", "Lu")
    response3 = auth_register("duck@gmail.com", "12345", "Haley", "Gu")

    token1 = response1['token']
    u_id1 = response1['u_id']

    token2 = response2['token']
    u_id2 = response2['u_id']

    token3 = response3['token']
    u_id3 = response3['u_id']

    channel_response1 = channels_create(token1, "Channel", True)

    channel_join(token2, channel_response1['channel_id'])

    message_response1 = message_send(token1, channel_response1['channel_id'], 'Hello this is my first message!')
    message1 = id_to_message(message_response1['message_id'])
    message_response2 = message_send(token2, channel_response1['channel_id'], 'Please don\'t remove this message')
    message2 = id_to_message(message_response2['message_id'])

    react_id = 1

    total_reacts = count_reacts(message_response1["message_id"], react_id)
    assert total_reacts == 0

    #### END
    ##################################################################################

    ##################################################################################
    #### Invalid parameters tests

    # Testing invalid token
    with pytest.raises(AccessError):
        message_react("not a valid token", message_response2['message_id'], react_id)
    total_reacts = count_reacts(message_response1["message_id"], react_id)
    assert total_reacts == 0

    # Testing invalid message_id
    with pytest.raises(ValueError):
        message_react(token1, 1000, react_id)
    total_reacts = count_reacts(message_response1["message_id"], react_id)
    assert total_reacts == 0
    
    # Testing invalid react_id
    with pytest.raises(ValueError):
        message_react(token1, message_response2['message_id'], "not a valid react_id")
    total_reacts = count_reacts(message_response1["message_id"], react_id)
    assert total_reacts == 0

    #### END Invalid parameters tests
    ################################################################################

    # Royce reacts to message1
    message_react(token1, message_response1['message_id'], react_id)
    total_reacts = count_reacts(message_response1["message_id"], react_id)
    assert total_reacts == 1
    
    # Haley attempts to react, without being in the channel
    with pytest.raises(AccessError):
        message_react(token3, message_response1['message_id'], react_id)
    total_reacts = count_reacts(message_response1["message_id"], react_id)
    assert total_reacts == 1
    
    # Kenneth reacts to message1
    message_react(token2, message_response1['message_id'], react_id)
    total_reacts = count_reacts(message_response1["message_id"], react_id)
    assert total_reacts == 2

    # Royce unreacts from the message
    message_unreact(token1, message_response1['message_id'], react_id)
    total_reacts = count_reacts(message_response1["message_id"], react_id)
    assert total_reacts == 1

def test_message_unreact():
    reset_data()

    ##################################################################################
    #### SETUP 

    # owner user 
    response1 = auth_register("dog@gmail.com", "12345", "Royce", "Huang")
    # ordinary user 
    response2 = auth_register("cat@gmail.com", "12345", "Kenneth", "Lu")
    response3 = auth_register("duck@gmail.com", "12345", "Haley", "Gu")

    token1 = response1['token']
    u_id1 = response1['u_id']

    token2 = response2['token']
    u_id2 = response2['u_id']

    token3 = response3['token']
    u_id3 = response3['u_id']

    channel_response1 = channels_create(token1, "Channel", True)

    channel_join(token2, channel_response1['channel_id'])

    message_response1 = message_send(token1, channel_response1['channel_id'], 'Hello this is my first message!')
    message1 = id_to_message(message_response1['message_id'])
    message_response2 = message_send(token2, channel_response1['channel_id'], 'Please don\'t remove this message')
    message2 = id_to_message(message_response2['message_id'])

    react_id = 1

    total_reacts = count_reacts(message_response1["message_id"], react_id)
    assert total_reacts == 0

    #### END
    ##################################################################################

    ##################################################################################
    #### Invalid parameters tests

    # Testing invalid token
    with pytest.raises(AccessError):
        message_unreact("not a valid token", message_response2['message_id'], react_id)
    total_reacts = count_reacts(message_response1["message_id"], react_id)
    assert total_reacts == 0

    # Testing invalid message_id
    with pytest.raises(ValueError):
        message_unreact(token1, 1000, react_id)
    total_reacts = count_reacts(message_response1["message_id"], react_id)
    assert total_reacts == 0
    
    # Testing invalid react_id
    with pytest.raises(ValueError):
        message_unreact(token1, message_response2['message_id'], "not a valid react_id")
    total_reacts = count_reacts(message_response1["message_id"], react_id)
    assert total_reacts == 0

    #### END Invalid parameters tests
    ################################################################################

    # Royce unreacts to message1 without reacting to it first
    with pytest.raises(ValueError):
        message_unreact(token1, message_response1['message_id'], react_id)
    total_reacts = count_reacts(message_response1["message_id"], react_id)
    assert total_reacts == 0

    # Royce reacts to message1
    message_react(token1, message_response1['message_id'], react_id)
    total_reacts = count_reacts(message_response1["message_id"], react_id)
    assert total_reacts == 1
    
    # Haley attempts to unreact, without being in the channel
    with pytest.raises(AccessError):
        message_unreact(token3, message_response1['message_id'], react_id)
    total_reacts = count_reacts(message_response1["message_id"], react_id)
    assert total_reacts == 1
    
    # Kenneth attemps to unreacts to message1
    with pytest.raises(ValueError):
        message_unreact(token2, message_response1['message_id'], react_id)
    total_reacts = count_reacts(message_response1["message_id"], react_id)
    assert total_reacts == 1

    # Royce unreacts from the message
    message_unreact(token1, message_response1['message_id'], react_id)
    total_reacts = count_reacts(message_response1["message_id"], react_id)
    assert total_reacts == 0

    # Royce attempts to unreact from message1 again
    with pytest.raises(ValueError):
        message_unreact(token2, message_response1['message_id'], react_id)
    total_reacts = count_reacts(message_response1["message_id"], react_id)
    assert total_reacts == 0

    # Royce attempts to unreact from message1 with a different react_id
    react_id = 2
    with pytest.raises(ValueError):
        message_unreact(token2, message_response1['message_id'], react_id)
    total_reacts = count_reacts(message_response1["message_id"], react_id)
    assert total_reacts == 0