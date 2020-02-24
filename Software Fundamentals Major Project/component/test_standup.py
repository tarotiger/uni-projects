from component.standup_start import standup_start
from component.standup_active import standup_active
from component.standup_send import standup_send 
from component.auth_register import auth_register
from component.channels_create import channels_create
from component.admin_userpermission_change import admin_userpermission_change
from component.channel_join import channel_join
from component.channel_leave import channel_leave
from component.channel_messages import channel_messages 
from component.auth_logout import auth_logout
from datetime import datetime, timezone, timedelta
from component.data import reset_data
from time import sleep 
import pytest 
from component.general import AccessError, ValueError

# testing standup for one channel 
def test_standup_start_simple():
	reset_data()

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

	channel_response1 = channels_create(token1, "Public Channel", True)
	channel_id1 = channel_response1['channel_id']
	channel_response2 = channels_create(token2, "Private Channel", False)
	channel_id2 = channel_response2['channel_id']

	channel_join(token2, 1)

    ####
	###### END
    ############################################################################

	# sending a message to a channel which does not have an active standup 
	with pytest.raises(ValueError):
		standup_send(token1, channel_id1, "Should not work")

	# making sure no messages are in the channel
	response_message = channel_messages(token1, channel_id1, 0)
	assert len(response_message['messages']) == 0
	assert response_message['end'] == -1 

	# trying to start a standup in a channel that doesn't exist 
	with pytest.raises(ValueError):
		standup_start(token1, 100, 10)

	response_active = standup_active(token1, channel_id1)
	assert response_active['time_finish'] == None 

	# testing simple case
	# standup should start 
	standup_start(token1, channel_id1, 1)

	response_active = standup_active(token1, channel_id1)

	# standup active an invalid channel 
	with pytest.raises(ValueError):
		standup_active(token1, 100)

	response_active['is_active'] == True 

	# user cannot raise a standup in the same channel 
	with pytest.raises(ValueError):
		standup_start(token1, channel_id1, 10)

	# another user tries to hold a standup in the channel 
	with pytest.raises(AccessError):
		standup_start(token3, channel_id1, 10)

	standup_send(token1, channel_id1, "Hello there") 
	
	# user not in the channel attempts to do a standup send 
	with pytest.raises(AccessError):
		standup_send(token3, channel_id1, "I'm not in the channel")

	# standup sending to a channel that doesn't exist 
	with pytest.raises(ValueError):
		standup_send(token3, 100, "I'm not in the channel")

	# standup sending a message with over 1000 characters 
	with pytest.raises(ValueError) as excinfo:
		standup_send(token1, channel_id1, "this message is longer that 1000 characters  this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters  this message is longer that 1000 characters  this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters  this message is longer that 1000 characters  this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters  this message is longer that 1000 characters  this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters this message is longer that 1000 characters!!")
	assert "1000" in str(excinfo.value)
	
	standup_send(token2, channel_id1, "Hi")

	sleep(1.2)

	response_message = channel_messages(token1, channel_id1, 0)
	assert len(response_message['messages']) == 1
	assert response_message['messages'][0]['message'] == "Royce Huang: Hello there\nKenneth Lu: Hi\n"

# testing standup except one of the sender leaves before message is sent 
def test_standup_start_simple_1():
	reset_data()

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

	channel_response1 = channels_create(token1, "Public Channel", True)
	channel_id1 = channel_response1['channel_id']
	channel_response2 = channels_create(token2, "Private Channel", False)
	channel_id2 = channel_response2['channel_id']

	channel_join(token2, 1)

    ####
	###### END
    ############################################################################

	# making sure no messages are in the channel
	response_message = channel_messages(token1, channel_id1, 0)
	assert len(response_message['messages']) == 0
	assert response_message['end'] == -1 

	# trying to start a standup in a channel that doesn't exist 
	with pytest.raises(ValueError):
		standup_start(token1, 100, 10)

	# testing simple case
	# standup should start 
	standup_start(token1, channel_id1, 1)

	response_active = standup_active(token1, channel_id1)

	response_active['is_active'] == True 

	# user cannot raise a standup in the same channel 
	with pytest.raises(ValueError):
		standup_start(token1, channel_id1, 10)

	# another user tries to hold a standup in the channel 
	with pytest.raises(AccessError):
		standup_start(token3, channel_id1, 10)

	standup_send(token1, channel_id1, "Hello there") 
	
	with pytest.raises(AccessError):
		standup_send(token3, channel_id1, "I'm not in the channel")
	
	standup_send(token2, channel_id1, "Hi")

	channel_leave(token2, channel_id1) 

	sleep(1)

	response_message = channel_messages(token1, channel_id1, 0)
	assert len(response_message['messages']) == 1
	assert response_message['messages'][0]['message'] == "Royce Huang: Hello there\nKenneth Lu: Hi\n"

# testing standup for two channels 
def test_standup_start_simple_2():
	reset_data()

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

	channel_response1 = channels_create(token1, "Public Channel", True)
	channel_id1 = channel_response1['channel_id']
	channel_response2 = channels_create(token2, "Private Channel", False)
	channel_id2 = channel_response2['channel_id']

	channel_join(token2, 1)
	channel_join(token1, 2)

    ####
	###### END
    ############################################################################

	# making sure no messages are in the channel
	response_message1 = channel_messages(token1, channel_id1, 0)
	assert len(response_message1['messages']) == 0
	assert response_message1['end'] == -1 

	# making sure no messages are in the channel
	response_message2 = channel_messages(token1, channel_id2, 0)
	assert len(response_message2['messages']) == 0
	assert response_message2['end'] == -1 

	# trying to start a standup in a channel that doesn't exist 
	with pytest.raises(ValueError):
		standup_start(token1, 100, 10)

	# testing simple case
	# standup should start 
	standup_start(token1, channel_id1, 1)
	standup_start(token2, channel_id2, 1) 

	response_active1 = standup_active(token1, channel_id1)
	response_active2 = standup_active(token1, channel_id2) 

	response_active1['is_active'] == True 
	response_active2['is_active'] == True 

	# user cannot raise a standup in the same channel 
	with pytest.raises(ValueError):
		standup_start(token1, channel_id1, 10)

	# another user tries to hold a standup in the channel 
	with pytest.raises(AccessError):
		standup_start(token3, channel_id1, 10)

	standup_send(token1, channel_id1, "Hello there") 
	
	with pytest.raises(AccessError):
		standup_send(token3, channel_id1, "I'm not in the channel")
	
	standup_send(token2, channel_id1, "Hi")
	standup_send(token1, channel_id2, "New channel who this")
	standup_send(token1, channel_id2, "Oh wait it's private")

	sleep(1)

	response_message1 = channel_messages(token1, channel_id1, 0)
	assert len(response_message1['messages']) == 1
	assert response_message1['messages'][0]['message'] == "Royce Huang: Hello there\nKenneth Lu: Hi\n"

	response_message2 = channel_messages(token1, channel_id2, 0) 
	assert len(response_message2['messages']) == 1
	assert response_message2['messages'][0]['message'] == "Royce Huang: New channel who this\nRoyce Huang: Oh wait it's private\n"

# testing standup except the user who started the standup logs out 
def test_standup_logout():
	reset_data()

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

	channel_response1 = channels_create(token1, "Public Channel", True)
	channel_id1 = channel_response1['channel_id']
	channel_response2 = channels_create(token2, "Private Channel", False)
	channel_id2 = channel_response2['channel_id']

	channel_join(token2, 1)

    ####
	###### END
    ############################################################################

	# making sure no messages are in the channel
	response_message = channel_messages(token1, channel_id1, 0)
	assert len(response_message['messages']) == 0
	assert response_message['end'] == -1 

	# trying to start a standup in a channel that doesn't exist 
	with pytest.raises(ValueError):
		standup_start(token1, 100, 10)

	# testing simple case
	# standup should start 
	standup_start(token1, channel_id1, 1)

	response_active = standup_active(token1, channel_id1)

	response_active['is_active'] == True 

	# user cannot raise a standup in the same channel 
	with pytest.raises(ValueError):
		standup_start(token1, channel_id1, 10)

	# another user tries to hold a standup in the channel 
	with pytest.raises(AccessError):
		standup_start(token3, channel_id1, 10)

	standup_send(token1, channel_id1, "Hello there") 
	
	with pytest.raises(AccessError):
		standup_send(token3, channel_id1, "I'm not in the channel")
	
	standup_send(token2, channel_id1, "Hi")

	auth_logout(token1)

	sleep(1)

	response_message = channel_messages(token2, channel_id1, 0)
	assert len(response_message['messages']) == 0

# testing standup except the user who started the standup leaves the channel
def test_standup_leave():
	reset_data()

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

	channel_response1 = channels_create(token1, "Public Channel", True)
	channel_id1 = channel_response1['channel_id']
	channel_response2 = channels_create(token2, "Private Channel", False)
	channel_id2 = channel_response2['channel_id']

	channel_join(token2, 1)

    ####
	###### END
    ############################################################################

	# making sure no messages are in the channel
	response_message = channel_messages(token1, channel_id1, 0)
	assert len(response_message['messages']) == 0
	assert response_message['end'] == -1 

	# trying to start a standup in a channel that doesn't exist 
	with pytest.raises(ValueError):
		standup_start(token1, 100, 10)

	# testing simple case
	# standup should start 
	standup_start(token1, channel_id1, 1)

	response_active = standup_active(token1, channel_id1)

	response_active['is_active'] == True 

	# user cannot raise a standup in the same channel 
	with pytest.raises(ValueError):
		standup_start(token1, channel_id1, 10)

	# another user tries to hold a standup in the channel 
	with pytest.raises(AccessError):
		standup_start(token3, channel_id1, 10)

	standup_send(token1, channel_id1, "Hello there") 
	
	with pytest.raises(AccessError):
		standup_send(token3, channel_id1, "I'm not in the channel")
	
	standup_send(token2, channel_id1, "Hi")

	channel_leave(token1, channel_id1)

	sleep(1)

	response_message = channel_messages(token2, channel_id1, 0)
	assert len(response_message['messages']) == 0
