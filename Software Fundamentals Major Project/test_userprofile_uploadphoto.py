# tests for userprofile functions 

import pytest 
import pathlib
import os
from component.general import AccessError, ValueError
from component.user_profile import user_profile
from component.user_profiles_uploadphoto import user_profiles_uploadphoto
from component.users_all import users_all
from component.auth_register import auth_register
from component.data import reset_data, get_data
from component.channels_create import channels_create
from component.channel_details import channel_details



# START UPLOADING PROFILE IMAGE
def test_profiles_uploadphoto():
	# resets data in the database
	reset_data()

	# registering 
	response1 = auth_register("dog@gmail.com", "12345", "Royce", "Huang")

	# user1 data 
	token1 = response1['token']
	u_id1 = response1['u_id']

	# creating new channel 
	channel_response = channels_create(token1, "Public Channel", True)
	channel_id1 = channel_response['channel_id']

	# profile_url_image should contain an empty string
	assert(users_all(token1) == {
		'users': [
			{
				'u_id': 1, 
				'email': 'dog@gmail.com', 
				'name_first': 'Royce', 
				'name_last': 'Huang', 
				'handle_str': 'Royce_Huang', 
				'profile_img_url': ''
			}
		]
	})

	# check the profile_url_image value in the channel details 
	details1 = channel_details(token1, channel_id1)
	assert(details1 == {
		'name': 'Public Channel', 
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
			}]
		})
	
	# file of the jpg is to be saved locally
	img_url = "https://i.kym-cdn.com/entries/icons/original/000/029/000/imbaby.jpg"
	user_profiles_uploadphoto(token1, img_url, 300, 200, 600, 400)
	filename = "./imgurl/" + img_url.split("/")[-1]
	assert(pathlib.Path(filename).exists() == True)

	# testing with invalid token
	with pytest.raises(AccessError):
		user_profiles_uploadphoto("not a token", img_url, 0, 0, 200, 200)

	#testing with invalid dimensions or dimensions outside of the range of the original image
	with pytest.raises(ValueError):
		user_profiles_uploadphoto(token1, img_url, -10, 0, 100, 100)
	with pytest.raises(ValueError):
		user_profiles_uploadphoto(token1, img_url, 0, -10, 100, 100)
	with pytest.raises(ValueError):
		user_profiles_uploadphoto(token1, img_url, 100, 100, 0, 50)
	with pytest.raises(ValueError):
		user_profiles_uploadphoto(token1, img_url, 100, 100, 50, 0)

	# testing with invalid url
	with pytest.raises(ValueError):
		user_profiles_uploadphoto(token1, "not_url", 0, 0, 100, 100)

	invalid_url = "https://i.kym-cdn.com/entries/icons/original/000/029/000/non-existent/imbaby.jpg/"
	# testing with a url that does not return 200
	with pytest.raises(ValueError):
		user_profiles_uploadphoto(token1, invalid_url, 0, 0, 100, 100)
	
	not_jpg_url = "http://www.google.com"
	with pytest.raises(ValueError):
		user_profiles_uploadphoto(token1, not_jpg_url, 0, 0, 100, 100)

	not_url1 = "comp1531"
	with pytest.raises(ValueError):
		user_profiles_uploadphoto(token1, not_url1, 0, 0, 100, 100)

	not_url2 = "dog.jpg"
	with pytest.raises(ValueError):
		user_profiles_uploadphoto(token1, not_url2, 0, 0, 100, 100)
# FINISH UPLOADING PROFILE IMAGE
