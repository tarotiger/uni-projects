# test function for search 

import pytest 
from component.search import search
from component.auth_register import auth_register
from component.admin_userpermission_change import admin_userpermission_change
from component.general import id_to_message
from component.channels_create import channels_create
from component.message_send import message_send
from component.channel_join import channel_join
from component.channel_leave import channel_leave 
from component.general import AccessError, ValueError
from component.data import get_data, reset_data

def test_search():
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

	message_response1 = message_send(token1, channel_id1, 'Hello this is my first message!')
	message1 = id_to_message(message_response1['message_id'])
	message_response2 = message_send(token2, channel_id1, 'Please don\'t remove this message')
	message2 = id_to_message(message_response2['message_id'])

    ####
	###### END
    ############################################################################

	# simple case 
	search_response = search(token1, "this")
	assert len(search_response['messages']) == 2

	# search should be case sensitive 
	search_response = search(token1, 'hello')
	assert len(search_response['messages']) == 0

	# user 2 sends the exact same message 
	message_send(token2, channel_id1, 'Hello this is my first message!')

	search_response = search(token1, "this")
	assert len(search_response['messages']) == 3

	# user 2 sends a message to the second channel 
	message_send(token2, channel_id2, "Please remove this message")

	# user 1 should not find the message user 2 made 
	search_response = search(token1, "this")
	assert len(search_response['messages']) == 3

	# find messages across channels 
	search_response = search(token2, "remove")
	assert len(search_response['messages']) == 2 

	channel_leave(token2, channel_id2)

	search_response = search(token2, "remove")
	assert len(search_response['messages']) == 1

	# searches for an empty string 
	search_response = search(token1, "")
	assert len(search_response['messages']) == 3

	# searching for messages even though user is not a part of any channels 
	search_response = search(token3, "message")
	assert len(search_response['messages']) == 0  

	# invalid token 
	with pytest.raises(AccessError):
		search("not a token", "hello")
