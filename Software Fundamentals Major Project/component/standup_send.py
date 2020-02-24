# 'standup_send' Sending a message to get buffered in the standup queue, 
# assuming a standup is currently active

from component.general import decode_token, id_to_channel, AccessError, ValueError, valid_channel_id, user_in_channel, id_to_user, authorise_token

@authorise_token
def standup_send(token, channel_id, message):
	if not valid_channel_id(channel_id):
		raise ValueError(description="Channel based on id does not exist")
	elif not user_in_channel(decode_token(token), channel_id):
		raise AccessError(description="Authorised user is not a member in the channel")
	elif len(message) > 1000:
		raise ValueError(description="Message is over 1000 characters long")
	else: 
		channel = id_to_channel(channel_id)
		user = id_to_user(decode_token(token))

		if channel['standup']['is_running'] == False: 
			raise ValueError(description="An active standup is not running in the channel")
		
		buffered_message = user['name_first'] + ' ' + user['name_last'] + ': ' + message + '\n'

		# adds the message to the message buffer key in the channel 
		channel['messages_buffer'] += buffered_message

		return {} 
