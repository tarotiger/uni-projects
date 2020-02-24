# tests for userprofile functions 

import pytest 
import pathlib
import os
from component.general import AccessError, ValueError, id_to_channel
from component.user_profile import user_profile
from component.user_profile_setname import user_profile_setname
from component.user_profile_setemail import user_profile_setemail
from component.user_profile_sethandle import user_profile_sethandle
from component.user_profiles_uploadphoto import user_profiles_uploadphoto
from component.users_all import users_all
from component.auth_register import auth_register
from component.auth_logout import auth_logout
from component.data import reset_data, get_data
from component.channels_create import channels_create
from component.channel_details import channel_details
from component.channel_join import channel_join
from component.channel_addowner import channel_addowner
from component.channel_details import channel_details

def test_user_profile(): 
	# resets data in the database
	reset_data()

	# logging in 
	response1 = auth_register("email@gmail.com", "12345", "Royce", "Huang")

	token1 = response1['token']
	u_id1 = response1['u_id']

	profile_response = user_profile(token1, u_id1)

	assert profile_response['u_id'] == 1
	assert profile_response['handle_str'] == "Royce_Huang"
	assert profile_response['email'] == "email@gmail.com"
	assert profile_response['name_first'] == "Royce"
	assert profile_response['name_last'] == "Huang"
	assert profile_response['profile_img_url'] == ""

	# invalid token
	with pytest.raises(AccessError):
		user_profile("not a token", u_id1)

	# invalid id
	with pytest.raises(ValueError):
		user_profile(token1, 100)

def test_user_profile_setname():
	# resets data in the database
	reset_data()

	# registering 
	response1 = auth_register("email@gmail.com", "12345", "Royce", "Huang")
	# registering 
	response2 = auth_register("cat@gmail.com", "12345", "Haley", "Gu")

	token1 = response1['token']
	u_id1 = response1['u_id']

	token2 = response2['token']
	u_id2 = response2['u_id']

	profile_response = user_profile(token1, u_id1)

	assert profile_response['u_id'] == 1
	assert profile_response['handle_str'] == "Royce_Huang"
	assert profile_response['email'] == "email@gmail.com"
	assert profile_response['name_first'] == "Royce"
	assert profile_response['name_last'] == "Huang"
	assert profile_response['profile_img_url'] == ""

	channel_response = channels_create(token1, 'First Channel', True)
	channel_id = channel_response['channel_id']

	channel_response2 = channels_create(token2, 'Second Channel', False)

	channel_join(token2, channel_id)

	channel_addowner(token1, channel_id, u_id2)

	# returns a channel object from the database 
	channel = id_to_channel(channel_id) 

	# confirms Royce's name is currently the same 
	assert channel['owner_members'][0]['name_first'] == "Royce"
	assert channel['owner_members'][0]['name_last'] == "Huang"
	assert channel['all_members'][0]['name_first'] == "Royce"
	assert channel['all_members'][0]['name_last'] == "Huang"
	
	user_profile_setname(token1, "Kenneth", "Lu")

	profile_response = user_profile(token1, u_id1)

	assert profile_response['handle_str'] == "Royce_Huang"
	assert profile_response['email'] == "email@gmail.com"
	assert profile_response['name_first'] == "Kenneth"
	assert profile_response['name_last'] == "Lu"
	assert profile_response['u_id'] == 1

	# confirms Royce's name has been changed in the channel 
	assert channel['owner_members'][0]['name_first'] == "Kenneth"
	assert channel['owner_members'][0]['name_last'] == "Lu"
	assert channel['all_members'][0]['name_first'] == "Kenneth"
	assert channel['all_members'][0]['name_last'] == "Lu"

	# invalid token 
	with pytest.raises(AccessError):
		user_profile_setname("not a token", "Kenneth", "Lu")

	# attempting to enter no name 
	with pytest.raises(ValueError):
		user_profile_setname(token1, "", "")

	# first name is over fifty characters long 
	with pytest.raises(ValueError):
		user_profile_setname(token1, "Thisnameisoverfiftycharacterslongwellalmostoverfiftycharacterslong", "Lastname")

	# last name is over fifty characters long 
	with pytest.raises(ValueError):
		user_profile_setname(token1, "Firstname", "Thisnameisoverfiftycharacterslongwellalmostoverfiftycharacterslong")

def test_user_profile_setemail():
	# resets data in the database
	reset_data()

	# registering 
	response1 = auth_register("dog@gmail.com", "12345", "Royce", "Huang")

	# registering 
	response2 = auth_register("snake@gmail.com", "12345", "Kenneth", "Lu")

	token1 = response1['token']
	u_id1 = response1['u_id']

	token2 = response2['token']
	u_id2 = response2['u_id']

	# present the original output of user_profile of the user1
	profile_response = user_profile(token1, u_id1)

	assert profile_response['u_id'] == 1
	assert profile_response['handle_str'] == "Royce_Huang"
	assert profile_response['email'] == "dog@gmail.com"
	assert profile_response['name_first'] == "Royce"
	assert profile_response['name_last'] == "Huang"
	assert profile_response['profile_img_url'] == ""

	# updating the email of the user with token1 ie. Royce Huang
	user_profile_setemail(token1, "kfc@gmail.com")

	profile_response2 = user_profile(token1, u_id1)

	# present the output after the email has changed
	assert profile_response2['handle_str'] == "Royce_Huang"
	assert profile_response2['email'] == "kfc@gmail.com"
	assert profile_response2['name_first'] == "Royce"
	assert profile_response2['name_last'] == "Huang"
	
	# testing that even updating the name after updating the email produces valid output
	user_profile_setname(token1, "Kevin", "Wu")

	profile_response3 = user_profile(token1, u_id1)
	assert profile_response3['handle_str'] == "Royce_Huang"
	assert profile_response3['email'] == "kfc@gmail.com"
	assert profile_response3['name_first'] == "Kevin"
	assert profile_response3['name_last'] == "Wu"


	# present the original output of user_profile of the user2
	profile_response4 = user_profile(token2, u_id2)

	assert profile_response4['handle_str'] == "Kenneth_Lu"
	assert profile_response4['email'] == "snake@gmail.com"
	assert profile_response4['name_first'] == "Kenneth"
	assert profile_response4['name_last'] == "Lu"

	# updating the email of the user with token1 ie. Royce Huang
	user_profile_setemail(token2, "imhungry@gmail.com")

	profile_response5 = user_profile(token2, u_id2)

	# present the output after the email has changed
	assert profile_response5['handle_str'] == "Kenneth_Lu"
	assert profile_response5['email'] == "imhungry@gmail.com"
	assert profile_response5['name_first'] == "Kenneth"
	assert profile_response5['name_last'] == "Lu"
	
	# testing that even updating the name after updating the email produces valid output
	user_profile_setname(token2, "Haley", "Gu")

	profile_response6 = user_profile(token2, u_id2)
	assert profile_response6['handle_str'] == "Kenneth_Lu"
	assert profile_response6['email'] == "imhungry@gmail.com"
	assert profile_response6['name_first'] == "Haley"
	assert profile_response6['name_last'] == "Gu"


	# invalid token 
	with pytest.raises(AccessError):
		user_profile_setemail("not a token", "maccas@gmail.com")
	
	# invalid email
	with pytest.raises(ValueError):
		user_profile_setemail(token1, "aidsemail")
		
	with pytest.raises(ValueError):
		user_profile_setemail(token2, "aidsemail")

	# email already taken by a current user
	with pytest.raises(ValueError):
		user_profile_setemail(token1, "imhungry@gmail.com")

	with pytest.raises(ValueError):
		user_profile_setemail(token2, "kfc@gmail.com")


def test_user_profile_sethandle():
	# resets data in the database
	reset_data()

	# registering 
	response1 = auth_register("dog@gmail.com", "12345", "Royce", "Huang")

	# registering 
	response2 = auth_register("maccas@gmail.com", "12345", "Donald", "Dog")

	token1 = response1['token']
	u_id1 = response1['u_id']

	token2 = response2['token']
	u_id2 = response2['u_id']

	# invalidating a valid token
	auth_logout(token2)

	# present the original output of user_profile of the user1
	profile_response = user_profile(token1, u_id1)

	assert profile_response['handle_str'] == "Royce_Huang"
	assert profile_response['email'] == "dog@gmail.com"
	assert profile_response['name_first'] == "Royce"
	assert profile_response['name_last'] == "Huang"

	# changing the handle_name
	user_profile_sethandle(token1, "Kevin_Wu")

	profile_response2 = user_profile(token1, u_id1)

	# show out the changes in the updated handle_str
	assert profile_response2['handle_str'] == "Kevin_Wu"
	assert profile_response2['email'] == "dog@gmail.com"
	assert profile_response2['name_first'] == "Royce"
	assert profile_response2['name_last'] == "Huang"

	# changing the handle_name again
	user_profile_sethandle(token1, "Haley_Gu")

	profile_response3 = user_profile(token1, u_id1)

	# show out the changes in the updated handle_str
	assert profile_response3['handle_str'] == "Haley_Gu"
	assert profile_response3['email'] == "dog@gmail.com"
	assert profile_response3['name_first'] == "Royce"
	assert profile_response3['name_last'] == "Huang"

	# attempt to change the handle string with a logged out token
	with pytest.raises(AccessError):
		user_profile_sethandle(token2, "Donald_Dog")

	with pytest.raises(AccessError):
		user_profile_sethandle("not a token", "Kenneth_Lu")

	with pytest.raises(ValueError):
		user_profile_sethandle(token1, "Thishandleisovertwentycharacterslongwellnowdefinitelyovertwentycharacterslong")
	
	with pytest.raises(ValueError):
		user_profile_sethandle(token1, "")


##############################################################################	TESTING FOR ALL THE USER FUNCTIONS
#	registering two users into a channel and showing the ouput 
# 	with comparision to the following changes:
#	-	changing everyones names 
#		* show that not only users[] changes, but if the users' details 
# 		  to be changed is an owner, it should also change.
#	- 	changing everyones handle_str
#	-	changing everyones email
#############################################################################
def test_all_user_profile():
	# resets data in the database
	reset_data()

	# registering 
	response1 = auth_register("dog@gmail.com", "12345", "Royce", "Huang")

	# registering 
	response2 = auth_register("snake@gmail.com", "12345", "Kenneth", "Lu")

	token1 = response1['token']
	u_id1 = response1['u_id']

	token2 = response2['token']
	u_id2 = response2['u_id']

	# create channel 
	channels_create(token1, "First Channel", True)
	channel_join(token2, 1)

	details1 = channel_details(token1, 1)

	assert details1 == {
		'name': 'First Channel', 
		'owner_members': [
			{
				'u_id': 1, 
				'name_first': 'Royce', 
				'name_last': 'Huang',
				'profile_img_url': ''
			}], 
		'all_members': [
			{
				'u_id': 1, 
				'name_first': 'Royce', 
				'name_last': 'Huang',
				'profile_img_url': ''
			}, 
			{
				'u_id': 2, 
				'name_first': 'Kenneth', 
				'name_last': 'Lu',
				'profile_img_url': ''
			}]
		}

# START CHANGING NAME
	profile_response = user_profile(token1, u_id1)

	assert profile_response['handle_str'] == "Royce_Huang"
	assert profile_response['email'] == "dog@gmail.com"
	assert profile_response['name_first'] == "Royce"
	assert profile_response['name_last'] == "Huang"

	# update the name of user with u_id1
	user_profile_setname(token1, "Kevin", "Wu")

	profile_response2 = user_profile(token1, u_id1)

	assert profile_response2['handle_str'] == "Royce_Huang"
	assert profile_response2['email'] == "dog@gmail.com"
	assert profile_response2['name_first'] == "Kevin"
	assert profile_response2['name_last'] == "Wu"

	profile_response3 = user_profile(token2, u_id2)

	assert profile_response3['handle_str'] == "Kenneth_Lu"
	assert profile_response3['email'] == "snake@gmail.com"
	assert profile_response3['name_first'] == "Kenneth"
	assert profile_response3['name_last'] == "Lu"

	# update the name of user with u_id1
	user_profile_setname(token2, "Haley", "Gu")

	profile_response4 = user_profile(token2, u_id2)

	assert profile_response4['handle_str'] == "Kenneth_Lu"
	assert profile_response4['email'] == "snake@gmail.com"
	assert profile_response4['name_first'] == "Haley"
	assert profile_response4['name_last'] == "Gu"

# FINISH CHANGING NAME

# CHANGING EMAIL

#USER1:
	profile_response5 = user_profile(token1, u_id1)

	assert profile_response5['handle_str'] == "Royce_Huang"
	assert profile_response5['email'] == "dog@gmail.com"
	assert profile_response5['name_first'] == "Kevin"
	assert profile_response5['name_last'] == "Wu"

	user_profile_setemail(token1, "kfc@gmail.com")

	profile_response6 = user_profile(token1, u_id1)

	assert profile_response6['handle_str'] == "Royce_Huang"
	assert profile_response6['email'] == "kfc@gmail.com"
	assert profile_response6['name_first'] == "Kevin"
	assert profile_response6['name_last'] == "Wu"

#USER2:
	profile_response7 = user_profile(token2, u_id2)
	assert profile_response7['handle_str'] == "Kenneth_Lu"
	assert profile_response7['email'] == "snake@gmail.com"
	assert profile_response7['name_first'] == "Haley"
	assert profile_response7['name_last'] == "Gu"

	user_profile_setemail(token2, "haley@gmail.com")

	profile_response8 = user_profile(token2, u_id2)
	assert profile_response8['handle_str'] == "Kenneth_Lu"
	assert profile_response8['email'] == "haley@gmail.com"
	assert profile_response8['name_first'] == "Haley"
	assert profile_response8['name_last'] == "Gu"

# FINISH CHANGING EMAIL

# START CHANGING HANDLE STRING
	profile_response9 = user_profile(token1, u_id1)

	assert profile_response9['handle_str'] == "Royce_Huang"
	assert profile_response9['email'] == "kfc@gmail.com"
	assert profile_response9['name_first'] == "Kevin"
	assert profile_response9['name_last'] == "Wu"

	user_profile_sethandle(token1, "Kevin_Wu")

	profile_response10 = user_profile(token1, u_id1)

	assert profile_response10['handle_str'] == "Kevin_Wu"
	assert profile_response10['email'] == "kfc@gmail.com"
	assert profile_response10['name_first'] == "Kevin"
	assert profile_response10['name_last'] == "Wu"


	profile_response11 = user_profile(token2, u_id2)

	assert profile_response11['handle_str'] == "Kenneth_Lu"
	assert profile_response11['email'] == "haley@gmail.com"
	assert profile_response11['name_first'] == "Haley"
	assert profile_response11['name_last'] == "Gu"

	user_profile_sethandle(token2, "Haley_Gu")
	
	profile_response12 = user_profile(token2, u_id2)
	assert profile_response12['handle_str'] == "Haley_Gu"
	assert profile_response12['email'] == "haley@gmail.com"
	assert profile_response12['name_first'] == "Haley"
	assert profile_response12['name_last'] == "Gu"

	# the names, email and handle_str have all changed
	details2 = channel_details(token1, 1)
	assert details2 == {
		'name': 'First Channel', 
		'owner_members': [
			{'u_id': 1, 
			'name_first': 'Kevin', 
			'name_last': 'Wu',
			'profile_img_url': ""
			}], 
		'all_members': [
			{
				'u_id': 1, 
				'name_first': 'Kevin', 
				'name_last': 'Wu',
				'profile_img_url': ""
			}, 
			{
				'u_id': 2, 
				'name_first': 'Haley', 
				'name_last': 'Gu',
				'profile_img_url': ""
			}]
		}
# FINISH CHANGING HANDLE STRING
