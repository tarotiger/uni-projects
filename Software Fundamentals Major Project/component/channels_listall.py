from component.general import valid_token, AccessError, authorise_token
from component.data import get_data

@authorise_token
def channels_listall(token):
    data = get_data()
    listall_channel = []

    #   returning all channels in slackr with their respective channel_id and name ONLY
    for channel in data['channels']:  
        all_channels = {
            'name': channel['name'],
            'channel_id': channel['channel_id']
        }
        listall_channel.append(all_channels)

    return {
        'channels': listall_channel
    }
