# 'search' Given a query string, return a collection of messages in all of the channels that the 
# user has joined that match the query

from component.general import decode_token, id_to_user, id_to_channel, AccessError, ValueError, user_in_channel, authorise_token
from component.data import get_data

@authorise_token
def search(token, query_str):
    data = get_data()

    messages = {
        'messages': [] 
    }

    user = id_to_user(decode_token(token))

    for channel in data['channels']: 
        # user is in the channel 
        if user_in_channel(user['u_id'], channel['channel_id']):
            for message in channel['messages']:
                # query_str is a substring of message 
                if query_str in message['message']:
                    messages['messages'].append(message)

    return messages 
