# 'standup_start' For a given channel, start the standup period whereby for the 
# next 15 minutes if someone calls "standup_send" with a message, it is 
# buffered during the 15 minute window then at the end of the 15 minute window 
# a message will be added to the message queue in the channel from the user who 
# started the standup.

from component.general import ValueError, AccessError, decode_token, id_to_user, valid_channel_id, user_in_channel, id_to_channel, authorise_token
from datetime import datetime, timezone, timedelta
from component.message_send import message_send
from threading import Timer 

@authorise_token
def standup_start(token, channel_id, length):
    if not valid_channel_id(channel_id):
        raise ValueError(description="Channel does not exist")
    else: 
        u_id = decode_token(token)
        channel = id_to_channel(channel_id)

        if not user_in_channel(u_id, channel_id):
            raise AccessError(description="User is not a member of the channel")
        elif channel['standup']['is_running'] == True: 
            raise ValueError(description="Standup is currently running")
        else:
            time_finish = str((datetime.now() + timedelta(seconds=length)).replace(tzinfo=timezone.utc))
            channel['standup']['is_running'] = True
            channel['standup']['time_finish'] = time_finish

            timer = Timer(length, standup_end, args=[token, channel_id])
            timer.start()

            return {"time_finish": time_finish}

def standup_end(token, channel_id):
    channel = id_to_channel(channel_id)

    # user is logged out so when the standup ends the buffer is cleared and 
    # the standup is resetted 
    if decode_token(token) == -1:
        channel['standup']['is_running'] = False
        channel['standup']['time_finish'] = None 
        # resets the message buffer 
        channel['messages_buffer'] = '' 
        return 
    elif not user_in_channel(decode_token(token), channel_id):
        channel['standup']['is_running'] = False
        channel['standup']['time_finish'] = None 
        # resets the message buffer 
        channel['messages_buffer'] = '' 
        return 

    # sends the message buffer to the channel 
    message_send(token, channel_id, channel['messages_buffer'])

    # resets the message buffer 
    channel['messages_buffer'] = ''

    channel['standup']['is_running'] = False
    channel['standup']['time_finish'] = None  

    return {} 
