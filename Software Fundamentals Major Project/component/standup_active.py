# 'standup active' For a given channel, return whether a standup is active in 
# it, and what time the standup finishes. If no standup is active, then 
# time_finish returns None

from datetime import datetime 
import time 

from component.general import decode_token, AccessError, ValueError, valid_channel_id, id_to_channel, authorise_token

@authorise_token
def standup_active(token, channel_id): 
	if not valid_channel_id(channel_id): 
		raise ValueError(description="channel_id is invalid")

	channel = id_to_channel(channel_id)
	
	standup = {
		'is_active': channel['standup']['is_running'],
		'time_finish': None
	}

	if channel['standup']['time_finish'] == None:
		return standup 

	time_finish = channel['standup']['time_finish'][:19]
	
	standup['time_finish'] = time.mktime(datetime.strptime(time_finish, "%Y-%m-%d %H:%M:%S").timetuple())

	return standup 