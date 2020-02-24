# tests for auth functions

import pytest
from component.auth_register import auth_register
from component.auth_login import auth_login
from component.auth_logout import auth_logout
from component.user_profile import user_profile
from component.general import AccessError, ValueError
from component.data import reset_data

# tests for user_profile as well 
def test_auth_register():
	# resets data in the database
	reset_data()

	# testing simple case
	response1 = auth_register("email@gmail.com", "admin", "Royce", "Huang")

	token1 = response1['token']
	u_id1 = response1['u_id']

	profile_response = user_profile(token1, u_id1)

	assert profile_response['handle_str'] == "Royce_Huang"
	assert profile_response['email'] == "email@gmail.com"
	assert profile_response['name_first'] == "Royce"
	assert profile_response['name_last'] == "Huang"

	# same first name and last name should produce another handle_str
	response2 = auth_register("differentemail@gmail.com", "12345", "Royce", "Huang")

	token2 = response2['token']
	u_id2 = response2['u_id']

	profile_response = user_profile(token2, u_id2)

	assert profile_response['handle_str'] == "Royce_Huang1"
	assert profile_response['email'] == "differentemail@gmail.com"
	assert profile_response['name_first'] == "Royce"
	assert profile_response['name_last'] == "Huang"

	# same first name and last name should produce another handle_str
	response3 = auth_register("cat@gmail.com", "12345", "Royce", "Huang")

	token3 = response3['token']
	u_id3 = response3['u_id']

	profile_response = user_profile(token2, u_id3)

	assert profile_response['handle_str'] == "Royce_Huang2"
	assert profile_response['email'] == "cat@gmail.com"
	assert profile_response['name_first'] == "Royce"
	assert profile_response['name_last'] == "Huang"

	# invalid token
	with pytest.raises(AccessError):
		user_profile("not a token", u_id1)

	# invalid id
	with pytest.raises(ValueError):
		user_profile(token1, 100)

    # invalid email
	with pytest.raises(ValueError) as excinfo:
		auth_register("notanemail", "admin", "Royce", "Huang")
	assert "Email is invalid" in str(excinfo.value), "Exception should return 'Email is taken'"

	# first name not given
	with pytest.raises(ValueError) as excinfo:
		auth_register("email@gmail.com", "admin", "", "Huang")
	assert "Name is invalid" in str(excinfo.value), "Exception should return 'Name is invalid'"

	# last name not given
	with pytest.raises(ValueError) as excinfo:
		auth_register("email@gmail.com", "admin", "Royce", "")
	assert "Name is invalid" in str(excinfo.value), "Exception should return 'Name is invalid'"

	# email already taken
	with pytest.raises(ValueError) as excinfo:
		auth_register("email@gmail.com", "admin", "Royce", "Huang")
	assert "Email is taken" in str(excinfo.value), "Exception should return 'Email is invalid'"

	# password is less than 5 characters
	with pytest.raises(ValueError) as excinfo:
		auth_register("dog@gmail.com", "1234", "Royce", "Huang")
	assert "Password is too short" in str(excinfo.value), "Exception should return 'Password is too short'"

	# first_name/last_name is not all characters
	with pytest.raises(ValueError) as excinfo:
		auth_register("dog@gmail.com", "admin", "Royc1", "Hu@ng")
	assert "Name is invalid" in str(excinfo.value), "Exception should return 'Name is invalid'"

	#   register with incorrect name_first
	with pytest.raises(ValueError) as excinfo:
		auth_register("royce@cse.unsw.edu.au", "12345", "123", "Huang")
	assert "Name is invalid" in str(excinfo.value), "Exception should return 'Name is invalid'"

	#   register with incorrect name_last
	with pytest.raises(ValueError) as excinfo:
		auth_register("royce@cse.unsw.edu.au", "12345", "Royce", "123")
	assert "Name is invalid" in str(excinfo.value), "Exception should return 'Name is invalid'"

def test_auth_logout():
	# resets data in the database
	reset_data()

	# testing simple case
	response1 = auth_register("email@gmail.com", "admin", "Royce", "Huang")

	token1 = response1['token']
	u_id1 = response1['u_id']

	profile_response = user_profile(token1, u_id1)

	assert profile_response['handle_str'] == "Royce_Huang"
	assert profile_response['email'] == "email@gmail.com"
	assert profile_response['name_first'] == "Royce"
	assert profile_response['name_last'] == "Huang"

	# same first name and last name should produce another handle_str
	response2 = auth_register("differentemail@gmail.com", "12345", "Royce", "Huang")

	token2 = response2['token']
	u_id2 = response2['u_id']

	profile_response = user_profile(token2, u_id2)

	assert profile_response['handle_str'] == "Royce_Huang1"
	assert profile_response['email'] == "differentemail@gmail.com"
	assert profile_response['name_first'] == "Royce"
	assert profile_response['name_last'] == "Huang"

	# same first name and last name should produce another handle_str
	response3 = auth_register("cat@gmail.com", "12345", "Royce", "Huang")

	token3 = response3['token']
	u_id3 = response3['u_id']

	profile_response = user_profile(token2, u_id3)

	assert profile_response['handle_str'] == "Royce_Huang2"
	assert profile_response['email'] == "cat@gmail.com"
	assert profile_response['name_first'] == "Royce"
	assert profile_response['name_last'] == "Huang"

	assert auth_logout(token1) == True 
	# logging out twice should result in a false return statement 
	assert auth_logout(token1) == False 

def test_auth_login():
	# resets data in the database
	reset_data()

	# testing simple case
	response1 = auth_register("email@gmail.com", "admin", "Royce", "Huang")

	token1 = response1['token']
	u_id1 = response1['u_id']

	profile_response = user_profile(token1, u_id1)

	assert profile_response['handle_str'] == "Royce_Huang"
	assert profile_response['email'] == "email@gmail.com"
	assert profile_response['name_first'] == "Royce"
	assert profile_response['name_last'] == "Huang"

	# same first name and last name should produce another handle_str
	response2 = auth_register("differentemail@gmail.com", "12345", "Royce", "Huang")

	token2 = response2['token']
	u_id2 = response2['u_id']

	profile_response = user_profile(token2, u_id2)

	assert profile_response['handle_str'] == "Royce_Huang1"
	assert profile_response['email'] == "differentemail@gmail.com"
	assert profile_response['name_first'] == "Royce"
	assert profile_response['name_last'] == "Huang"

	# same first name and last name should produce another handle_str
	response3 = auth_register("cat@gmail.com", "12345", "Royce", "Huang")

	token3 = response3['token']
	u_id3 = response3['u_id']

	profile_response = user_profile(token2, u_id3)

	assert profile_response['handle_str'] == "Royce_Huang2"
	assert profile_response['email'] == "cat@gmail.com"
	assert profile_response['name_first'] == "Royce"
	assert profile_response['name_last'] == "Huang"

	# user can login on two different devices and are given two different tokens 
	login_response1 = auth_login("email@gmail.com", "admin")
	assert login_response1['token'] != token1  

	# incorrect password 
	with pytest.raises(ValueError) as excinfo:
		auth_login("email@gmail.com", "wrongpword")
	assert "Password is incorrect" in str(excinfo.value), "Exception should return 'Password is incorrect'"

	# invalid email
	with pytest.raises(ValueError) as excinfo: 
		auth_login("greg", "12345")
	assert "Email is invalid" in str(excinfo.value), "Exception should return 'Email is invalid'"

	# valid but non-existent email 
	with pytest.raises(ValueError) as excinfo:
		auth_login("fake@email.com", "admin")
	assert "Email does not belong to a user" in str(excinfo.value), "Exception should return 'Email does not belong to a user'"
